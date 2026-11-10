"""report: report.md from final findings, drops, and the fact-check ledger."""
import json
from pathlib import Path

from .common import read_json, write_text
from .guide import load_rules
from .prepare import load_run

SEV_ORDER = ("must", "should", "prefer")


def _q(s):
    return json.dumps(s, ensure_ascii=False)


def _item(f, titles):
    title = titles.get(f["rule_id"]) or f.get("rule_title") or ""
    head = "- **L%d** %s%s" % (f["line"], f["rule_id"], " (%s)" % title if title else "")
    if f.get("replacement") is not None:
        body = "%s -> %s" % (_q(f["quote"]), _q(f["replacement"]))
    else:
        body = "%s: %s" % (_q(f["quote"]), f.get("comment") or "see the rule")
    tags = [f["id"], f["pass"]]
    if f.get("basis") == "inferred":
        tags.append("inferred")
    if f.get("status") == "revised":
        tags.append("revised by verifier")
    return "%s: %s [%s]" % (head, body, ", ".join(tags))


def report_run(run_dir, guide_path):
    run, article, paths = load_run(run_dir)
    guide = load_rules(guide_path)
    titles = {r["id"]: r.get("title") for r in guide["rules"]}
    final = read_json(paths["findings"] / "final.json", "final findings (run `sgc verdicts` first)")
    drops_path = paths["findings"] / "drops.json"
    drops = read_json(drops_path, "drops.json") if drops_path.is_file() else []
    ledger_path = paths["facts"] / "ledger-check.json"
    ledger = read_json(ledger_path, "ledger check") if ledger_path.is_file() else None

    style = [f for f in final if f["pass"] != "facts"]
    facts = [f for f in final if f["pass"] == "facts"]
    violations = [f for f in style if not f.get("suggestion")]
    suggestions = [f for f in style if f.get("suggestion")]

    out = ["# Style check: %s" % (run.get("article_name") or "article"), ""]
    out.append("- Article: %s" % run.get("article"))
    out.append("- Guide: %s" % guide_path)
    out.append("- Content type: %s" % (run.get("content_type") or "not set"))
    sev_counts = {s: sum(1 for f in violations if f.get("severity") == s) for s in SEV_ORDER}
    out.append("- Violations: %d (%s)" % (len(violations), ", ".join(
        "%d %s" % (sev_counts[s], s) for s in ("must", "should"))))
    out.append("- Suggestions: %d" % len(suggestions))
    if ledger is not None or facts:
        out.append("- Fact issues: %d" % len(facts))
    out.append("- Dropped before the report: %d" % len(drops))
    out.append("")
    if guide.get("schema_version") == 1:
        out += ["This guide uses the v1 format; its rules were read as V1-N.M sections and none is "
                "checked in code. Upgrading with `build-style-guide --upgrade` adds rule IDs and lint checks.", ""]

    out += ["## Violations", ""]
    if not violations:
        out += ["None.", ""]
    for sev in ("must", "should", "prefer"):
        chosen = sorted((f for f in violations if f.get("severity") == sev), key=lambda f: (f["line"], f.get("col", 0)))
        if not chosen:
            continue
        out += ["### %s" % sev.capitalize(), ""]
        out += [_item(f, titles) for f in chosen]
        out.append("")

    out += ["## Suggestions", ""]
    if suggestions:
        out += [_item(f, titles) for f in sorted(suggestions, key=lambda f: (f["line"], f.get("col", 0)))]
    else:
        out.append("None.")
    out.append("")

    if ledger is not None or facts:
        out += ["## Fact check", ""]
        if ledger is not None:
            out.append("Ledger rows: %d; checked against saved pages: %s."
                       % (ledger.get("rows_total", 0), ", ".join(
                           "%d %s" % (n, s) for s, n in sorted((ledger.get("summary") or {}).items()))))
            out.append("")
        if facts:
            out += [_item(f, titles) for f in sorted(facts, key=lambda f: f["line"])]
        else:
            out.append("No fact issues.")
        out.append("")

    out += ["## Dropped findings", ""]
    if not drops:
        out.append("None.")
    else:
        groups = {}
        for d in drops:
            key = (d.get("stage"), d.get("reason"))
            groups[key] = groups.get(key, 0) + 1
        out += ["| Stage | Reason | Count |", "|---|---|---|"]
        for (stage, reason), count in sorted(groups.items(), key=lambda kv: (-kv[1], str(kv[0]))):
            out.append("| %s | %s | %d |" % (stage, (reason or "").replace("|", "\\|"), count))
    out.append("")
    text = "\n".join(out)
    write_text(paths["report"], text)
    return {"report": str(paths["report"]), "violations": len(violations),
            "by_severity": sev_counts, "suggestions": len(suggestions), "fact_issues": len(facts),
            "dropped": len(drops), "guide_schema_version": guide.get("schema_version")}


__all__ = ["report_run", "Path"]
