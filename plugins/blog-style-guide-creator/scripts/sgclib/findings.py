"""lint (run step), findings (filter and merge), verdicts, decisions."""
import json
from pathlib import Path

from . import lint as lintmod
from .common import die, normalize_text, now_iso, read_json, read_text, write_json, write_text
from .guide import load_rules
from .prepare import load_run, record_guide, resolve_content_type

NOT_REVIEWER_FILES = {"merged.json", "drops.json", "final.json", "relint.json",
                      "mechanical-confirmed.json"}
PROOF_TEXT = ("Built-in proofreading rule: objective errors only (typos, wrong words, doubled "
              "words, agreement, unbalanced punctuation, inconsistent spellings of a name).")
CODE_CHECKED_PASSES = ("lint", "facts")
ALL_ZONES = ("frontmatter", "code", "blockquote", "url", "quote")
# A typo inside a quote is still the writer's to fix, so proofreading skips only these.
PROOF_ZONES = ("frontmatter", "code", "url")


# ------------------------------------------------------------ lint step


def lint_run(guide_path, run_dir, content_type=None):
    run, article, paths = load_run(run_dir)
    guide = load_rules(guide_path)
    ct, ct_source = resolve_content_type(content_type, run, article, guide["rules"])
    rules = record_guide(run_dir, run, guide_path, guide, ct, ct_source)
    for r in rules:
        if r.get("check"):
            _p, errors = lintmod.normalize_params(r["check"], r.get("params") or {})
            if errors:
                die("rule %s: %s (run `sgc guide validate`)" % (r["id"], "; ".join(errors)))
    found = lintmod.run_lint(rules, article, ct)
    write_json(paths["findings"] / "lint.json", found)
    uncertain = [f["id"] for f in found if f["certainty"] == "uncertain"]
    by_rule = {}
    for f in found:
        by_rule[f["rule_id"]] = by_rule.get(f["rule_id"], 0) + 1
    return {"findings": len(found), "certain": len(found) - len(uncertain),
            "uncertain": len(uncertain), "uncertain_ids": uncertain, "by_rule": by_rule,
            "schema_version": guide.get("schema_version"),
            "out": str(paths["findings"] / "lint.json")}


# ------------------------------------------------------------ helpers


def _load_findings_file(path):
    data = read_json(path, "findings file")
    if isinstance(data, dict):
        data = data.get("findings")
    if not isinstance(data, list):
        die("%s must hold a JSON array of findings or an object with a findings array" % path)
    return data


def _rules_index(run, paths, guide_path=None):
    if guide_path:
        guide = load_rules(guide_path)
        return {r["id"]: r for r in guide["rules"]}, guide
    if paths["rules"].exists():
        data = read_json(paths["rules"], "rules.json")
        index = {r["id"]: r for r in data["rules"]}
        for r in data.get("out_of_scope") or []:
            index.setdefault(r["id"], {"id": r["id"], "scope": r.get("scope"), "title": None})
        return index, data
    if run.get("guide"):
        guide = load_rules(run["guide"])
        return {r["id"]: r for r in guide["rules"]}, guide
    die("no rules for this run: run `sgc lint` or `sgc packets` first, or pass --guide")


def _builtin(rule_id):
    if rule_id.startswith("PROOF-"):
        return {"id": rule_id, "title": "Proofreading", "severity": "should", "kind": "proof",
                "scope": "all", "audience": "all", "text": PROOF_TEXT}
    if rule_id.startswith("FACT-"):
        return {"id": rule_id, "title": "Fact check", "severity": "must", "kind": "fact",
                "scope": "all", "audience": "all", "text": "Built-in fact-check finding from the ledger."}
    return None


def _occurrences(article, quote):
    out = []
    for n in article.numbers():
        line = article.line(n)
        start = line.find(quote)
        while start != -1:
            out.append((n, start))
            start = line.find(quote, start + 1)
    return out


def _malformed(f):
    if not isinstance(f, dict):
        return "not an object"
    if not isinstance(f.get("rule_id"), str) or not f["rule_id"]:
        return "no rule_id"
    if not isinstance(f.get("line"), int) or isinstance(f.get("line"), bool):
        return "line is not a whole number"
    if not isinstance(f.get("quote"), str) or not f["quote"]:
        return "no quote"
    if "\n" in f["quote"]:
        return "quote spans more than one line"
    if f.get("replacement") is not None and not isinstance(f["replacement"], str):
        return "replacement is neither a string nor null"
    if f.get("basis") not in (None, "explicit", "inferred"):
        return "basis must be explicit or inferred"
    return None


def load_decisions(path):
    out = []
    p = Path(path)
    if not p.is_file():
        return out
    for i, line in enumerate(read_text(p, "decisions file").split("\n")):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            die("%s line %d is not JSON" % (p, i + 1))
        if isinstance(row, dict) and row.get("rule_id") and row.get("quote"):
            out.append((row["rule_id"], normalize_text(row["quote"])))
    return out


# ------------------------------------------------------------ findings step


def findings_run(run_dir, guide_path=None, decisions_path=None):
    run, article, paths = load_run(run_dir)
    fdir = paths["findings"]
    if not (fdir / "lint.json").is_file():
        die("findings/lint.json is missing: run `sgc lint` first")
    rules, _guide = _rules_index(run, paths, guide_path)
    content_type = run.get("content_type")
    draft = run.get("draft", "human")
    if decisions_path is None and run.get("brand_dir"):
        decisions_path = Path(run["brand_dir"]) / "decisions.jsonl"
    rejected = set(load_decisions(decisions_path)) if decisions_path else set()

    confirm_path = fdir / "mechanical-confirmed.json"
    confirmed = None
    if confirm_path.is_file():
        data = read_json(confirm_path, "mechanical confirmer answers")
        if not isinstance(data, list):
            die("%s must be a JSON array of {\"id\", \"applies\"}" % confirm_path)
        confirmed = {}
        for i, row in enumerate(data):
            if not isinstance(row, dict) or not row.get("id") or not isinstance(row.get("applies"), bool):
                die("%s item %d needs an id and applies: true or false" % (confirm_path, i))
            confirmed[row["id"]] = row

    files = sorted(p for p in fdir.glob("*.json") if p.name not in NOT_REVIEWER_FILES)
    order = sorted(files, key=lambda p: (0 if p.stem == "lint" else 1 if p.stem == "facts" else 2, p.stem))
    kept, drops = [], []

    def drop(f, pass_name, stage, reason):
        drops.append({"pass": pass_name, "stage": stage, "reason": reason, "finding": f})

    for path in order:
        pass_name = path.stem
        for f in _load_findings_file(path):
            problem = _malformed(f)
            if problem:
                drop(f, pass_name, "malformed", problem)
                continue
            f = dict(f)
            f["pass"] = pass_name
            f.setdefault("replacement", None)
            f.setdefault("comment", None)
            f.setdefault("basis", "explicit")
            rule = rules.get(f["rule_id"]) or _builtin(f["rule_id"])
            if rule is None:
                drop(f, pass_name, "rule", "rule %s is not in the guide" % f["rule_id"])
                continue
            if not lintmod.in_scope(rule, content_type):
                drop(f, pass_name, "scope", "rule %s does not apply to content type %s"
                     % (f["rule_id"], content_type))
                continue
            # anchor
            n = f["line"]
            quote = f["quote"]
            on_line = 1 <= n <= len(article.lines) and quote in article.line(n)
            if on_line:
                line = article.line(n)
                col = f.get("col")
                if not (isinstance(col, int) and line[col:col + len(quote)] == quote):
                    f["col"] = line.find(quote)
            else:
                hits = _occurrences(article, quote)
                if len(hits) == 1:
                    f["moved_from"] = n
                    f["line"], f["col"] = hits[0]
                elif not hits:
                    drop(f, pass_name, "anchor", "quote not found in the article")
                    continue
                else:
                    drop(f, pass_name, "anchor", "quote not on line %d and found %d times elsewhere"
                         % (n, len(hits)))
                    continue
            if pass_name not in CODE_CHECKED_PASSES:
                kinds = PROOF_ZONES if pass_name == "proof" else ALL_ZONES
                zone = article.zone_at(f["line"], f["col"], f["col"] + len(quote), kinds)
                if zone:
                    drop(f, pass_name, "protected", "quote is inside a protected zone (%s)" % zone)
                    continue
            if (f["rule_id"], normalize_text(quote)) in rejected:
                drop(f, pass_name, "decision", "matches an earlier rejection in decisions.jsonl")
                continue
            # lint confirmation
            if pass_name == "lint" and f.get("certainty") == "uncertain":
                answer = (confirmed or {}).get(f.get("id"))
                if answer is not None and not answer["applies"]:
                    drop(f, pass_name, "confirm", "mechanical confirmer: does not apply%s"
                         % (" (%s)" % answer["reason"] if answer.get("reason") else ""))
                    continue
                if answer is not None:
                    f["confirmed"] = True
                    if answer.get("reason"):
                        f["confirm_reason"] = answer["reason"]
                else:
                    f["confirmed"] = None
                    f["basis"] = "inferred"
            severity = rule.get("severity") or "should"
            f["severity"] = severity
            f["kind"] = rule.get("kind") or "usage"
            f["rule_title"] = rule.get("title")
            f["suggestion"] = severity == "prefer" or (
                rule.get("audience") == "ai-drafting" and draft != "ai")
            f["status"] = "auto" if pass_name in CODE_CHECKED_PASSES else "pending"
            kept.append(f)

    # merge overlaps of one rule on one line, and the same fix to the same text under two rules
    kept.sort(key=lambda f: (f["line"], f["col"], order_key(f["pass"])))
    merged = []
    for f in kept:
        span = (f["col"], f["col"] + len(f["quote"]))
        twin, why = None, None
        for g in merged:
            if g["line"] != f["line"]:
                continue
            gspan = (g["col"], g["col"] + len(g["quote"]))
            if g["rule_id"] == f["rule_id"] and span[0] < gspan[1] and gspan[0] < span[1]:
                twin, why = g, "overlaps finding %s for the same rule"
                break
            if (span == gspan and f.get("replacement") is not None
                    and f["replacement"] == g.get("replacement")):
                twin, why = g, "makes the same fix to the same text as finding %s"
                break
        if twin is not None:
            twin.setdefault("also_found_by", [])
            if f["pass"] not in twin["also_found_by"] and f["pass"] != twin["pass"]:
                twin["also_found_by"].append(f["pass"])
            drop(f, f["pass"], "merged", why % (twin.get("id") or "from pass %s" % twin["pass"]))
            continue
        merged.append(f)

    n_f = 0
    width = max(4, len(str(len(merged))))
    for f in merged:
        if not (f["pass"] == "lint" and f.get("id")):
            n_f += 1
            f["id"] = "F" + str(n_f).zfill(width)

    write_json(fdir / "merged.json", merged)
    write_json(fdir / "drops.json", drops)

    vdir = paths["verify"]
    vdir.mkdir(parents=True, exist_ok=True)
    for old in vdir.glob("*.md"):
        old.unlink()
    packets = []
    by_pass = {}
    for f in merged:
        if f["status"] == "pending":
            by_pass.setdefault(f["pass"], []).append(f)
    for pass_name, items in sorted(by_pass.items()):
        p = vdir / ("%s.md" % pass_name)
        write_text(p, _verify_packet(pass_name, items, rules, article))
        packets.append({"pass": pass_name, "packet": "verify/%s.md" % pass_name,
                        "output": "verify/%s.verdicts.json" % pass_name, "findings": len(items)})
    counts = {}
    for d in drops:
        counts[d["stage"]] = counts.get(d["stage"], 0) + 1
    return {"merged": len(merged), "pending": sum(len(v) for v in by_pass.values()),
            "auto": sum(1 for f in merged if f["status"] == "auto"),
            "dropped": len(drops), "drops_by_stage": counts,
            "confirmer_file": confirm_path.is_file(), "verify_packets": packets,
            "out": str(fdir / "merged.json")}


def order_key(pass_name):
    return (0 if pass_name == "lint" else 1 if pass_name == "facts" else 2, pass_name)


def _verify_packet(pass_name, items, rules, article):
    out = ["# Findings to verify: %s" % pass_name, "",
           "- Findings: %d" % len(items),
           "- Write verdicts to: verify/%s.verdicts.json" % pass_name,
           "- Verdict shape: [{\"id\", \"verdict\": \"keep\" | \"drop\" | \"revise\", \"reason\", "
           "\"replacement\" (revise only)}]", ""]
    for f in items:
        rule = rules.get(f["rule_id"]) or _builtin(f["rule_id"]) or {}
        out.append("## %s" % f["id"])
        out.append("")
        out.append("- Rule: %s (%s)" % (f["rule_id"], f.get("severity")))
        out.append("- Line: %d" % f["line"])
        out.append("- Quote: %s" % json.dumps(f["quote"], ensure_ascii=False))
        out.append("- Replacement: %s" % json.dumps(f.get("replacement"), ensure_ascii=False))
        if f.get("comment"):
            out.append("- Comment: %s" % f["comment"])
        out.append("- Basis: %s" % f.get("basis"))
        out.append("")
        out.append("Rule text:")
        out.append("")
        out.append("~~~markdown")
        out.append(rule.get("text") or "(no rule text)")
        out.append("~~~")
        out.append("")
        out.append("Context:")
        out.append("")
        out.append("~~~text")
        width = max(4, len(str(len(article.lines))))
        for n in range(max(1, f["line"] - 2), min(len(article.lines), f["line"] + 2) + 1):
            out.append("L%s| %s" % (str(n).zfill(width), article.line(n)))
        out.append("~~~")
        out.append("")
    return "\n".join(out)


# ------------------------------------------------------------ verdicts


def verdicts_run(run_dir):
    run, article, paths = load_run(run_dir)
    merged_path = paths["findings"] / "merged.json"
    merged = read_json(merged_path, "merged findings (run `sgc findings` first)")
    by_id = {f["id"]: f for f in merged}
    verdicts, unknown = {}, []
    for path in sorted(paths["verify"].glob("*.verdicts.json")):
        data = read_json(path, "verdicts file")
        if isinstance(data, dict):
            data = data.get("verdicts")
        if not isinstance(data, list):
            die("%s must be a JSON array of verdicts" % path)
        for i, v in enumerate(data):
            if not isinstance(v, dict) or not v.get("id"):
                die("%s item %d has no id" % (path, i))
            if v.get("verdict") not in ("keep", "drop", "revise"):
                die("%s item %d (%s): verdict must be keep, drop, or revise" % (path, i, v["id"]))
            if v["verdict"] == "revise" and "replacement" not in v:
                die("%s item %d (%s): a revise verdict needs a replacement (null turns it into a comment)"
                    % (path, i, v["id"]))
            if v["id"] not in by_id:
                unknown.append(v["id"])
                continue
            verdicts[v["id"]] = v
    missing = [f["id"] for f in merged if f["status"] == "pending" and f["id"] not in verdicts]
    if missing:
        passes = sorted({by_id[i]["pass"] for i in missing})
        die("no verdict for %d pending finding(s): %s. Expected in: %s"
            % (len(missing), ", ".join(missing[:20]),
               ", ".join("verify/%s.verdicts.json" % p for p in passes)))
    drops_path = paths["findings"] / "drops.json"
    drops = read_json(drops_path, "drops.json") if drops_path.is_file() else []
    drops = [d for d in drops if d.get("stage") != "verify"]
    final = []
    for f in merged:
        if f["status"] != "pending":
            final.append(f)
            continue
        v = verdicts[f["id"]]
        f = dict(f)
        f["verdict_reason"] = v.get("reason")
        if v["verdict"] == "drop":
            drops.append({"pass": f["pass"], "stage": "verify", "reason": v.get("reason") or "dropped by verifier",
                          "finding": f})
            continue
        if v["verdict"] == "revise":
            f["original_replacement"] = f.get("replacement")
            f["replacement"] = v["replacement"]
            if v["replacement"] is None and not f.get("comment"):
                f["comment"] = v.get("reason")
            f["status"] = "revised"
        else:
            f["status"] = "kept"
        final.append(f)
    write_json(paths["findings"] / "final.json", final)
    write_json(drops_path, drops)
    return {"final": len(final), "kept": sum(1 for f in final if f["status"] == "kept"),
            "revised": sum(1 for f in final if f["status"] == "revised"),
            "auto": sum(1 for f in final if f["status"] == "auto"),
            "dropped_by_verifier": sum(1 for d in drops if d["stage"] == "verify"),
            "unknown_verdict_ids": unknown, "out": str(paths["findings"] / "final.json")}


# ------------------------------------------------------------ decisions


def decisions_run(run_dir, reject_ids, brand_dir, reason=None):
    run, _article, paths = load_run(run_dir)
    source = paths["findings"] / "final.json"
    if not source.is_file():
        source = paths["findings"] / "merged.json"
    findings = read_json(source, "findings (run `sgc findings` first)")
    by_id = {f["id"]: f for f in findings}
    missing = [i for i in reject_ids if i not in by_id]
    if missing:
        die("no finding with id %s in %s" % (", ".join(missing), source))
    bdir = Path(brand_dir)
    if not bdir.is_dir():
        die("brand folder not found: %s" % bdir)
    path = bdir / "decisions.jsonl"
    rows = []
    for i in reject_ids:
        f = by_id[i]
        rows.append({"decision": "reject", "at": now_iso(), "rule_id": f["rule_id"],
                     "quote": f["quote"], "replacement": f.get("replacement"),
                     "comment": f.get("comment"), "pass": f.get("pass"), "finding_id": i,
                     "article": run.get("article"), "reason": reason})
    with open(str(path), "a", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return {"appended": len(rows), "decisions": str(path)}
