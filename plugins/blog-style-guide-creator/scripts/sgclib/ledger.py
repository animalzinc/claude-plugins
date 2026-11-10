"""ledger-check: confirm every fact-check excerpt on its saved page, then turn
rows other than `confirmed` into FACT-* findings.

Reads <run>/facts/ledger.json (array of rows, or {"rows": [...]}) and the pages
`sgc fetch` saved in <run>/facts/pages/. Writes <run>/facts/ledger-check.json
and <run>/findings/facts.json. Exit 1 when a row fails its check.
"""
import json
from pathlib import Path

from .common import die, normalize_text, read_json, write_json
from .fetch import normalize_url, rebuild_index
from .prepare import load_run

VERDICTS = ("confirmed", "contradicted", "unsupported", "unverifiable", "link-dead", "link-mismatch")
NEEDS_EXCERPT = ("confirmed", "contradicted")
NEEDS_PAGE = ("confirmed", "contradicted", "unsupported", "link-mismatch")
TRIM_WORDS = 3


def _trim(excerpt):
    parts = excerpt.split()
    if len(parts) <= TRIM_WORDS * 2 + 2:
        return None
    return " ".join(parts[TRIM_WORDS:len(parts) - TRIM_WORDS])


def _page(url, index, pages_dir):
    """(text, meta, note); text is None when the latest fetch did not succeed."""
    sha = index.get(normalize_url(url))
    if not sha:
        return None, {}, "no saved fetch for %s; run `sgc fetch` for it" % url
    meta_path = Path(pages_dir) / ("%s.json" % sha)
    meta = {}
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except ValueError:
            meta = {}
    if meta.get("status") != "ok":
        return None, meta, "the latest fetch of %s did not succeed (%s%s)" % (
            url, meta.get("status") or "unknown", ", " + meta["note"] if meta.get("note") else "")
    text_path = Path(pages_dir) / ("%s.txt" % sha)
    if not text_path.is_file() or not text_path.read_text(encoding="utf-8").strip():
        return None, meta, "the saved page for %s has no text" % url
    return text_path.read_text(encoding="utf-8"), meta, None


def check_rows(rows, pages_dir):
    index = rebuild_index(pages_dir) if Path(pages_dir).is_dir() else {}
    results = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            die("ledger row %d is not an object" % i)
        rid = row.get("id") or "row-%d" % (i + 1)
        verdict = (row.get("verdict") or "").strip().lower()
        if verdict not in VERDICTS:
            die("ledger row %s has verdict %r; use one of %s" % (rid, row.get("verdict"), ", ".join(VERDICTS)))
        url = (row.get("source_url") or "").strip()
        excerpt = (row.get("excerpt") or "").strip()
        res = {"id": rid, "verdict": verdict, "source_url": url or None}

        def done(status, note):
            res.update(status=status, note=note)
            results.append(res)

        if verdict == "unverifiable":
            done("skipped", "unverifiable rows are listed, never checked")
            continue
        if not url:
            done("no_source", "no source_url on a %s row" % verdict)
            continue
        if verdict in NEEDS_EXCERPT and not excerpt:
            done("missing_excerpt", "a %s row needs an excerpt copied from the page" % verdict)
            continue
        text, meta, note = _page(url, index, pages_dir)
        if verdict == "link-dead":
            if text is not None:
                done("link_alive", "the saved fetch of %s succeeded, so the link is not dead" % url)
            elif meta.get("status") == "blocked" or meta.get("blocked"):
                # A site that refuses scripts (a 403, a bot check) says nothing about the link itself.
                res["verdict"] = "unverifiable"
                done("skipped", "the site refused the fetch (%s), so the link could not be checked; "
                     "reported as unverifiable" % (meta.get("note") or "blocked"))
            elif not meta:
                done("no_fetch", note)
            else:
                done("ok", "the latest fetch failed: %s" % (meta.get("note") or meta.get("status")))
            continue
        if text is None:
            done("no_fetch", note)
            continue
        if not excerpt:
            done("ok", "page fetched; no excerpt to check")
            continue
        hay, needle = normalize_text(text), normalize_text(excerpt)
        if needle and needle in hay:
            done("ok", "excerpt found on %s" % url)
            continue
        trimmed = _trim(excerpt)
        if trimmed and normalize_text(trimmed) in hay:
            done("partial", "the excerpt matches only without its first and last %d words" % TRIM_WORDS)
            continue
        done("excerpt_not_found", "the excerpt is not on the saved page %s: %r" % (url, excerpt[:160]))
    return results


def ledger_run(run_dir):
    run, article, paths = load_run(run_dir)
    ledger_path = paths["facts"] / "ledger.json"
    data = read_json(ledger_path, "fact ledger (facts/ledger.json)")
    rows = data.get("rows") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        die("%s must be an array of rows or an object with a rows array" % ledger_path)
    pages = paths["facts"] / "pages"
    results = check_rows(rows, pages)
    by_id = {r["id"]: r for r in results}
    failing = [r for r in results if r["status"] not in ("ok", "skipped")]
    findings = []
    for i, row in enumerate(rows):
        rid = row.get("id") or "row-%d" % (i + 1)
        res = by_id[rid]
        if res["status"] not in ("ok", "skipped") or res["verdict"] == "confirmed":
            continue
        quote = row.get("quote") or ""
        line = row.get("line")
        if not quote or not isinstance(line, int):
            res.update(status="no_anchor", note="a %s row needs the article line and a quote from it" % res["verdict"])
            failing.append(res)
            continue
        comment = "%s: %s" % (res["verdict"].replace("-", " ").capitalize(), row.get("claim") or quote)
        if row.get("source_url"):
            comment += " Source: %s." % row["source_url"]
        if row.get("excerpt"):
            comment += " The page says: %s" % json.dumps(row["excerpt"], ensure_ascii=False)
        if row.get("note"):
            comment += " %s" % row["note"]
        findings.append({"rule_id": "FACT-" + res["verdict"].upper(), "pass": "facts", "line": line,
                         "quote": quote, "replacement": None, "comment": comment,
                         "basis": "explicit", "ledger_id": rid})
    summary = {}
    for r in results:
        summary[r["status"]] = summary.get(r["status"], 0) + 1
    report = {"ledger": str(ledger_path), "pages": str(pages), "rows_total": len(results),
              "summary": summary, "failing_ids": [r["id"] for r in failing], "rows": results}
    write_json(paths["facts"] / "ledger-check.json", report)
    write_json(paths["findings"] / "facts.json", findings)
    report["fact_findings"] = len(findings)
    return report, not failing
