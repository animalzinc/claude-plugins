"""prepare (article into a run folder), packets (rule packets per reviewer),
and the run-folder helpers the later steps share."""
import hashlib
import json
import shutil
from pathlib import Path

from . import lint as lintmod
from .article import Article
from .common import die, dumps, now_iso, read_json, read_text, write_json, write_text
from .guide import load_rules

GENERATED_DIRS = ("packets", "findings", "verify", "facts")
REVIEWERS = ("usage", "structure", "voice")


# ------------------------------------------------------------ run folder


def run_paths(run_dir):
    r = Path(run_dir)
    return {
        "run": r / "run.json",
        "article": r / "article.md",
        "numbered": r / "article.numbered.md",
        "outline": r / "outline.json",
        "rules": r / "rules.json",
        "packets": r / "packets",
        "findings": r / "findings",
        "verify": r / "verify",
        "facts": r / "facts",
        "report": r / "report.md",
    }


def load_run(run_dir):
    paths = run_paths(run_dir)
    if not Path(run_dir).is_dir():
        die("run folder not found: %s (run `sgc prepare` first)" % run_dir)
    run = read_json(paths["run"], "run record (run.json; run `sgc prepare` first)")
    article = Article(read_text(paths["article"], "prepared article (article.md)"))
    return run, article, paths


def save_run(run_dir, run):
    write_json(run_paths(run_dir)["run"], run)


def resolve_content_type(cli_value, run, article, rules):
    """The content type, from the flag, the run record, then the article's
    frontmatter; dies when the guide scopes rules by type and none is known."""
    ct, source = cli_value, "--content-type"
    if not ct and run.get("content_type"):
        ct, source = run["content_type"], run.get("content_type_source") or "run.json"
    if not ct and article.frontmatter:
        for key in ("content_type", "type"):
            if article.frontmatter.get(key):
                ct, source = str(article.frontmatter[key]), "article frontmatter (%s)" % key
                break
    if not ct:
        source = None
        scoped = sorted({t for r in rules for t in (r.get("scope") if isinstance(r.get("scope"), list) else [])})
        if scoped:
            die("the guide scopes rules by content type (%s) and no content type is known; "
                "pass --content-type" % ", ".join(scoped))
    return ct, source


def applicable_rules(guide, content_type):
    return [r for r in guide["rules"] if lintmod.in_scope(r, content_type)]


def record_guide(run_dir, run, guide_path, guide, content_type, ct_source):
    run["guide"] = str(Path(guide_path).resolve())
    run["guide_schema_version"] = guide.get("schema_version")
    run["content_type"] = content_type
    run["content_type_source"] = ct_source
    save_run(run_dir, run)
    rules = applicable_rules(guide, content_type)
    write_json(run_paths(run_dir)["rules"], {
        "guide": run["guide"], "schema_version": guide.get("schema_version"),
        "brand": (guide.get("frontmatter") or {}).get("brand"),
        "content_types": (guide.get("frontmatter") or {}).get("content_types") or [],
        "content_type": content_type, "rules": rules,
        "out_of_scope": [{"id": r["id"], "scope": r.get("scope")} for r in guide["rules"]
                         if not lintmod.in_scope(r, content_type)],
        "retired": guide.get("retired") or []})
    return rules


# ------------------------------------------------------------ prepare


def prepare(article_path, run_dir, content_type=None, brand_dir=None, draft="human"):
    src = Path(article_path)
    raw_bytes = None
    if not src.is_file():
        die("article not found: %s" % src)
    raw_bytes = src.read_bytes()
    text = read_text(src, "article")
    if not text.strip():
        die("the article is empty: %s" % src)
    run = Path(run_dir)
    run.mkdir(parents=True, exist_ok=True)
    cleared = []
    for name in GENERATED_DIRS:
        d = run / name
        if d.exists():
            shutil.rmtree(str(d))
            cleared.append(name)
    for name in ("rules.json", "apply.json"):
        if (run / name).exists():
            (run / name).unlink()
    report = run / "report.md"
    if report.exists():
        report.replace(run / "report.previous.md")
    for name in GENERATED_DIRS:
        (run / name).mkdir(parents=True, exist_ok=True)
    art = Article(text)
    ct, ct_source = content_type, "--content-type" if content_type else None
    if not ct and art.frontmatter:
        for key in ("content_type", "type"):
            if art.frontmatter.get(key):
                ct, ct_source = str(art.frontmatter[key]), "article frontmatter (%s)" % key
                break
    body = "\n".join(art.lines) + "\n"
    paths = run_paths(run)
    write_text(paths["article"], body)
    write_text(paths["numbered"], art.numbered())
    outline = art.outline(ct)
    write_json(paths["outline"], outline)
    record = {
        "article": str(src.resolve()),
        "article_name": src.stem,
        "prepared_at": now_iso(),
        "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "newline": "\r\n" if b"\r\n" in raw_bytes else "\n",
        "bom": raw_bytes.startswith(b"\xef\xbb\xbf"),
        "content_type": ct,
        "content_type_source": ct_source,
        "draft": draft,
        "brand_dir": str(Path(brand_dir).resolve()) if brand_dir else None,
        "guide": None,
        "guide_schema_version": None,
    }
    save_run(run, record)
    return {"run_dir": str(run), "article": str(paths["article"]), "numbered": str(paths["numbered"]),
            "outline": str(paths["outline"]), "lines": outline["lines"],
            "word_count": outline["word_count"], "headings": len(outline["headings"]),
            "links": len(outline["links"]), "content_type": ct, "content_type_source": ct_source,
            "cleared": cleared, "previous_report": (run / "report.previous.md").exists()}


# ------------------------------------------------------------ packets


def _route(rule):
    if rule.get("check"):
        return "mechanical"
    kind = rule.get("kind") or "usage"
    return "usage" if kind == "mechanical" else kind if kind in REVIEWERS else "usage"


def _packet_text(reviewer, part, rules, run, guide_meta, output_name):
    head = [
        "# %s rules%s" % (reviewer.capitalize(), " (part %d)" % part if part else ""),
        "",
        "- Brand: %s" % (guide_meta.get("brand") or "unknown"),
        "- Guide: %s (schema version %s)" % (run.get("guide"), run.get("guide_schema_version")),
        "- Content type: %s" % (run.get("content_type") or "not set"),
        "- Draft: %s" % run.get("draft", "human"),
        "- Article with line numbers: article.numbered.md",
        "- Write findings to: findings/%s" % output_name,
        "- Rules: %d" % len(rules),
        "",
    ]
    body = []
    for r in rules:
        body.append(r.get("text") or "### %s: %s" % (r["id"], r["title"]))
        if r.get("audience") == "ai-drafting":
            body.append("")
            body.append("_Audience: ai-drafting. On a human draft, findings for this rule are suggestions._")
        if reviewer == "mechanical":
            params, _errs = lintmod.normalize_params(r["check"], r.get("params") or {})
            body.append("")
            body.append("Check `%s` with parameters: `%s`" % (r["check"], json.dumps(params, ensure_ascii=False)))
        body.append("")
    return "\n".join(head + body).rstrip("\n") + "\n"


def packets(guide_path, run_dir, content_type=None, split_above=60):
    run, article, paths = load_run(run_dir)
    guide = load_rules(guide_path)
    ct, ct_source = resolve_content_type(content_type, run, article, guide["rules"])
    rules = record_guide(run_dir, run, guide_path, guide, ct, ct_source)
    run = read_json(paths["run"])
    meta = {"brand": (guide.get("frontmatter") or {}).get("brand")}
    pdir = paths["packets"]
    pdir.mkdir(parents=True, exist_ok=True)
    for old in pdir.glob("*.md"):
        old.unlink()
    groups = {"usage": [], "structure": [], "voice": [], "mechanical": []}
    for r in rules:
        groups[_route(r)].append(r)
    written = []
    for reviewer in ("usage", "structure", "voice", "mechanical"):
        chosen = groups[reviewer]
        if not chosen:
            continue
        if reviewer != "mechanical" and split_above and len(chosen) > split_above:
            half = (len(chosen) + 1) // 2
            parts = [(1, chosen[:half]), (2, chosen[half:])]
        else:
            parts = [(0, chosen)]
        for part, part_rules in parts:
            stem = "%s-%d" % (reviewer, part) if part else reviewer
            output = "mechanical-confirmed.json" if reviewer == "mechanical" else stem + ".json"
            write_text(pdir / (stem + ".md"), _packet_text(reviewer, part, part_rules, run, meta, output))
            written.append({"reviewer": reviewer, "packet": "packets/%s.md" % stem,
                            "output": output, "output_path": "findings/" + output,
                            "rules": len(part_rules), "rule_ids": [r["id"] for r in part_rules]})
    index = {"guide": run["guide"], "schema_version": guide.get("schema_version"),
             "content_type": ct, "split_above": split_above, "packets": written,
             "proofreader": {"packet": None, "output": "proof.json", "output_path": "findings/proof.json"}}
    write_json(pdir / "index.json", index)
    return index


def article_sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


__all__ = ["prepare", "packets", "load_run", "run_paths", "resolve_content_type",
           "record_guide", "dumps"]
