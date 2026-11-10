"""apply: accepted replacements, bottom-up, overlaps refused, then a re-lint."""
import shutil
from pathlib import Path

from . import lint as lintmod
from .article import Article
from .common import die, read_json, read_text, write_json, write_text
from .prepare import article_sha, load_run


def _accepted(final, accept):
    tokens = [t.strip() for t in accept.split(",") if t.strip()]
    if not tokens:
        die("--accept needs finding ids or auto")
    by_id = {f["id"]: f for f in final}
    chosen, seen = [], set()
    for t in tokens:
        if t == "auto":
            for f in final:
                if (f["pass"] == "lint" and f.get("certainty") == "certain" and f["status"] == "auto"
                        and f.get("replacement") is not None and not f.get("suggestion")
                        and f["id"] not in seen):
                    chosen.append(f)
                    seen.add(f["id"])
        elif t not in by_id:
            die("no finding with id %s in findings/final.json" % t)
        elif t not in seen:
            chosen.append(by_id[t])
            seen.add(t)
    return chosen


def apply_edits(lines, findings):
    """(new lines, applied, refused). Each finding needs line, col or quote, and a replacement."""
    refused, spans = [], []
    for f in findings:
        if f.get("replacement") is None:
            refused.append({"id": f["id"], "reason": "a comment, never applied"})
            continue
        n = f["line"]
        if not 1 <= n <= len(lines):
            refused.append({"id": f["id"], "reason": "line %d is outside the article" % n})
            continue
        line, quote = lines[n - 1], f["quote"]
        col = f.get("col")
        if not (isinstance(col, int) and line[col:col + len(quote)] == quote):
            col = line.find(quote)
        if col < 0:
            refused.append({"id": f["id"], "reason": "quote is no longer on line %d" % n})
            continue
        spans.append((n, col, col + len(quote), f))
    spans.sort(key=lambda s: (s[0], s[1], s[2]))
    def overlap(a, b):
        return a[0] == b[0] and (a[1] < b[2] and b[1] < a[2] or a[1] == b[1])

    ok = []
    for s in spans:
        others = [o[3]["id"] for o in spans if o is not s and overlap(s, o)]
        if others:
            refused.append({"id": s[3]["id"], "reason": "overlaps %s on line %d; accept one of them"
                            % (", ".join(sorted(set(others))), s[0])})
        else:
            ok.append(s)
    out = list(lines)
    for n, start, end, f in sorted(ok, key=lambda s: (s[0], s[1]), reverse=True):
        line = out[n - 1]
        out[n - 1] = line[:start] + f["replacement"] + line[end:]
    return out, [s[3]["id"] for s in ok], refused


def apply_run(run_dir, accept, in_place=False):
    run, article, paths = load_run(run_dir)
    final = read_json(paths["findings"] / "final.json", "final findings (run `sgc verdicts` first)")
    chosen = _accepted(final, accept)
    original = Path(run["article"])
    if not original.is_file():
        die("the original article is gone: %s" % original)
    current = read_text(original, "original article")
    current_norm = current if current.endswith("\n") else current + "\n"
    changed_since = article_sha(current_norm) != run.get("sha256")
    if changed_since and in_place:
        die("the article changed since `sgc prepare`; line numbers no longer match. Prepare and check it again.")
    new_lines, applied, refused = apply_edits(list(article.lines), chosen)
    text = "\n".join(new_lines) + "\n"
    newline = run.get("newline") or "\n"
    disk = text.replace("\n", newline)
    if run.get("bom"):
        disk = "﻿" + disk
    if in_place:
        backup = original.with_name(original.stem + ".bak")
        shutil.copy2(str(original), str(backup))
        target = original
    else:
        backup = None
        target = original.with_name(original.stem + "_edited" + original.suffix)
    with open(str(target), "w", encoding="utf-8", newline="") as handle:
        handle.write(disk)
    relint = []
    rules_path = paths["rules"]
    if rules_path.is_file():
        rules = read_json(rules_path, "rules.json")["rules"]
        relint = lintmod.run_lint(rules, Article(text), run.get("content_type"))
        write_json(paths["findings"] / "relint.json", relint)
    by_rule = {}
    for f in relint:
        by_rule[f["rule_id"]] = by_rule.get(f["rule_id"], 0) + 1
    result = {"accepted": [f["id"] for f in chosen], "applied": applied, "refused": refused,
              "output": str(target), "backup": str(backup) if backup else None,
              "original_changed_since_prepare": changed_since,
              "relint": {"findings": len(relint), "by_rule": by_rule,
                         "out": str(paths["findings"] / "relint.json") if rules_path.is_file() else None}}
    write_json(Path(run_dir) / "apply.json", result)
    return result


__all__ = ["apply_run", "apply_edits", "write_text"]
