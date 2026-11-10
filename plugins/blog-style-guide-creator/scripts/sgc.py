#!/usr/bin/env python3
"""sgc: the deterministic layer of blog-style-guide-creator.

Every subcommand prints JSON to stdout unless it writes a named output file
(then it prints a JSON summary), and exits 2 with a message on stderr when an
input is missing or malformed. `guide validate` and `ledger-check` exit 1 when
the check fails; `fetch` exits 1 when the page could not be read.
"""
import argparse
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sgclib import __version__  # noqa: E402
from sgclib.common import SgcError, dumps, read_text, write_json, write_text  # noqa: E402


def _out(data):
    sys.stdout.write(dumps(data) + "\n")


def cmd_brand_path(a):
    from sgclib.guide import brand_path
    _out(brand_path(a.brand, a.guides_dir, a.project_dir, a.guide))


def cmd_extract(a):
    from sgclib.extract import extract
    _out(extract(a.source, a.out))


def cmd_fetch(a):
    from sgclib.fetch import fetch_cmd
    payload, ok = fetch_cmd(a.url, a.out_dir, a.terms)
    _out(payload)
    if not ok:
        sys.stderr.write("sgc: fetch %s: %s (%s)\n" % (payload["status"], a.url, payload["note"]))
        return 1


def cmd_profile(a):
    from sgclib.profile import profile
    data = profile(a.articles)
    write_json(a.out, data)
    _out({"out": a.out, "articles": data["articles"], "totals": data["totals"]})


def cmd_guide_parse(a):
    from sgclib.guide import load_rules
    data = load_rules(a.guide)
    if a.out:
        write_json(a.out, data)
        _out({"out": a.out, "rules": len(data["rules"]), "schema_version": data.get("schema_version")})
    else:
        _out(data)


def cmd_guide_validate(a):
    from sgclib.guide import schema_version_of, validate_guide
    text = read_text(a.guide, "style guide")
    if schema_version_of(text) != 2:
        result = {"valid": False, "rules": 0, "retired": 0,
                  "errors": ["not a v2 guide (no schema_version: 2 in the frontmatter); "
                             "upgrade it with build-style-guide --upgrade"], "warnings": []}
    else:
        result = validate_guide(text, a.guide)
    _out(result)
    return 0 if result["valid"] else 1


def cmd_guide_render(a):
    from sgclib.common import read_json
    from sgclib.guide import render
    proposal = read_json(a.proposal, "proposal")
    existing = read_text(a.existing, "existing guide") if a.existing else None
    text, report = render(proposal, existing)
    write_text(a.out, text)
    report["out"] = a.out
    _out(report)


def cmd_guide_diff(a):
    from sgclib.guide import diff_guides, diff_markdown
    d = diff_guides(read_text(a.old, "old guide"), read_text(a.new, "new guide"))
    if a.markdown:
        sys.stdout.write(diff_markdown(d) + "\n")
    else:
        _out(d)


def cmd_guide_checklist(a):
    from sgclib.guide import write_checklist
    text, added = write_checklist(read_text(a.guide, "style guide"))
    write_text(a.guide, text)
    _out({"guide": a.guide, "markers_added": added})


def cmd_guide_index_v1(a):
    from sgclib.guide import index_v1
    data = index_v1(read_text(a.guide, "v1 guide"))
    if not data["rules"]:
        raise SgcError("no numbered sections (## N. Title) with ### subsections in %s" % a.guide)
    if a.out:
        write_json(a.out, data)
        _out({"out": a.out, "rules": len(data["rules"])})
    else:
        _out(data)


def cmd_kit_candidates(a):
    from sgclib.kit import kit_candidates
    data = kit_candidates(a.kit_dir)
    write_json(a.out, data)
    _out({"out": a.out, "kit_id": data["kit_id"], "kit_updated_at": data["kit_updated_at"], "candidates": len(data["candidates"]),
          "content_types": data["content_types"]})


def cmd_prepare(a):
    from sgclib.prepare import prepare
    _out(prepare(a.article, a.run_dir, a.content_type, a.brand_dir, a.draft))


def cmd_packets(a):
    from sgclib.prepare import packets
    _out(packets(a.guide, a.run_dir, a.content_type, a.split_above))


def cmd_lint(a):
    from sgclib.findings import lint_run
    _out(lint_run(a.guide, a.run_dir, a.content_type))


def cmd_findings(a):
    from sgclib.findings import findings_run
    _out(findings_run(a.run_dir, a.guide, a.decisions))


def cmd_verdicts(a):
    from sgclib.findings import verdicts_run
    _out(verdicts_run(a.run_dir))


def cmd_report(a):
    from sgclib.report import report_run
    _out(report_run(a.run_dir, a.guide))


def cmd_apply(a):
    from sgclib.apply import apply_run
    _out(apply_run(a.run_dir, a.accept, a.in_place))


def cmd_decisions(a):
    from sgclib.findings import decisions_run
    ids = [x.strip() for x in ",".join(a.reject).split(",") if x.strip()]
    if not ids:
        raise SgcError("--reject needs at least one finding id")
    _out(decisions_run(a.run_dir, ids, a.brand_dir, a.reason))


def cmd_diff_pairs(a):
    from sgclib.edits import diff_pairs
    data = diff_pairs(a.edits_dir)
    write_json(a.out, data)
    _out({"out": a.out, "pairs": data["pair_count"], "hunks": data["hunk_count"],
          "unpaired": data["unpaired"]})


def cmd_ledger_check(a):
    from sgclib.ledger import ledger_run
    report, ok = ledger_run(a.run_dir)
    _out(report)
    if not ok:
        sys.stderr.write("sgc: ledger check failed for %s\n" % ", ".join(report["failing_ids"]))
    return 0 if ok else 1


def build_parser():
    p = argparse.ArgumentParser(prog="sgc", description=__doc__.splitlines()[0])
    p.add_argument("--version", action="version", version="sgc " + __version__)
    sub = p.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    s = sub.add_parser("brand-path", help="resolve the brand folder and guide")
    s.add_argument("brand")
    s.add_argument("--guides-dir")
    s.add_argument("--project-dir")
    s.add_argument("--guide")
    s.set_defaults(func=cmd_brand_path)

    s = sub.add_parser("extract", help="URL, saved HTML, or Markdown into clean Markdown")
    s.add_argument("source")
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_extract)

    s = sub.add_parser("fetch", help="fetch a page and save its text under a hash of the URL")
    s.add_argument("url")
    s.add_argument("--out-dir", required=True)
    s.add_argument("--terms", nargs="*", default=[])
    s.set_defaults(func=cmd_fetch)

    s = sub.add_parser("profile", help="count lint patterns across source articles")
    s.add_argument("articles", nargs="+")
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_profile)

    g = sub.add_parser("guide", help="guide operations").add_subparsers(dest="guide_command", metavar="<guide command>")
    g.required = True
    s = g.add_parser("parse", help="parse a guide (v2, or v1 through index-v1) into rules JSON")
    s.add_argument("guide")
    s.add_argument("--out")
    s.set_defaults(func=cmd_guide_parse)
    s = g.add_parser("validate", help="validate a v2 guide")
    s.add_argument("guide")
    s.set_defaults(func=cmd_guide_validate)
    s = g.add_parser("render", help="write a guide from a proposal")
    s.add_argument("proposal")
    s.add_argument("--out", required=True)
    s.add_argument("--existing")
    s.set_defaults(func=cmd_guide_render)
    s = g.add_parser("diff", help="added, changed, modified, and retired rules")
    s.add_argument("old")
    s.add_argument("new")
    s.add_argument("--markdown", action="store_true", help="print a readable summary instead of JSON")
    s.set_defaults(func=cmd_guide_diff)
    s = g.add_parser("checklist", help="rewrite the checklist between its markers")
    s.add_argument("guide")
    s.set_defaults(func=cmd_guide_checklist)
    s = g.add_parser("index-v1", help="read a v1 guide as V1-N.M rules")
    s.add_argument("guide")
    s.add_argument("--out")
    s.set_defaults(func=cmd_guide_index_v1)

    s = sub.add_parser("kit-candidates", help="saved brand kit JSON into candidate rules")
    s.add_argument("kit_dir")
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_kit_candidates)

    s = sub.add_parser("prepare", help="article into a run folder")
    s.add_argument("article")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--content-type")
    s.add_argument("--brand-dir", help="brand folder whose decisions.jsonl `findings` reads")
    s.add_argument("--draft", choices=("human", "ai"), default="human",
                   help="who wrote the draft; ai-drafting rules are suggestions on a human draft")
    s.set_defaults(func=cmd_prepare)

    s = sub.add_parser("packets", help="one rule packet per reviewer")
    s.add_argument("guide")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--content-type")
    s.add_argument("--split-above", type=int, default=60)
    s.set_defaults(func=cmd_packets)

    s = sub.add_parser("lint", help="run the lint checks")
    s.add_argument("guide")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--content-type")
    s.set_defaults(func=cmd_lint)

    s = sub.add_parser("findings", help="filter, re-anchor, and merge reviewer findings")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--guide", help="guide to read rules from (default: the run's rules.json)")
    s.add_argument("--decisions", help="decisions.jsonl (default: the run's brand folder)")
    s.set_defaults(func=cmd_findings)

    s = sub.add_parser("verdicts", help="apply verifier verdicts")
    s.add_argument("--run-dir", required=True)
    s.set_defaults(func=cmd_verdicts)

    s = sub.add_parser("report", help="write report.md")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--guide", required=True)
    s.set_defaults(func=cmd_report)

    s = sub.add_parser("apply", help="apply accepted replacements")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--accept", required=True, help="comma-separated finding ids, or auto")
    s.add_argument("--in-place", action="store_true")
    s.set_defaults(func=cmd_apply)

    s = sub.add_parser("decisions", help="record rejected findings")
    s.add_argument("--run-dir", required=True)
    s.add_argument("--reject", required=True, nargs="+", help="finding ids, space or comma separated")
    s.add_argument("--brand-dir", required=True)
    s.add_argument("--reason")
    s.set_defaults(func=cmd_decisions)

    s = sub.add_parser("diff-pairs", help="editor edit pairs into word-level hunks")
    s.add_argument("edits_dir")
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_diff_pairs)

    s = sub.add_parser("ledger-check", help="confirm fact-check excerpts on saved pages")
    s.add_argument("--run-dir", required=True)
    s.set_defaults(func=cmd_ledger_check)
    return p


def main(argv=None):
    for stream in ("stdout", "stderr"):
        handle = getattr(sys, stream)
        if hasattr(handle, "reconfigure"):
            try:
                handle.reconfigure(encoding="utf-8")
            except (ValueError, io.UnsupportedOperation):
                pass
    args = build_parser().parse_args(argv)
    try:
        code = args.func(args)
    except SgcError as exc:
        sys.stderr.write("sgc: error: %s\n" % exc)
        return 2
    return code or 0


if __name__ == "__main__":
    sys.exit(main())
