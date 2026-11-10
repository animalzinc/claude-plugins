"""kit-candidates, diff-pairs, ledger-check, extract, fetch, profile, and the CLI."""
import io
import json
import shutil
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

from helpers import FIXTURES, ROOT, TempDir

import sgc
from sgclib.common import SgcError, read_json
from sgclib.edits import diff_pairs, diff_texts
from sgclib.extract import extract, html_to_markdown
from sgclib.fetch import fetch_text, normalize_url, save_fetch, url_key
from sgclib.kit import kit_candidates
from sgclib.ledger import ledger_run
from sgclib.prepare import prepare
from sgclib.profile import profile


class Kit(unittest.TestCase):
    def test_candidates(self):
        data = kit_candidates(FIXTURES / "kit")
        by = {c["id"]: c for c in data["candidates"]}
        self.assertEqual(data["kit_id"], 4242)
        self.assertEqual(data["kit_updated_at"], "2026-11-10T07:31:04.049Z")
        self.assertEqual(data["content_types"], ["how-to", "essay"])
        self.assertEqual(by["KIT-101"]["text"], "Never promise that a kite cannot break.")
        self.assertEqual((by["KIT-101"]["severity"], by["KIT-101"]["source"]), ("must", "kit:101"))
        self.assertEqual(by["KIT-201"]["scope"], ["how-to"])
        self.assertEqual(by["KIT-PERSONA"]["kind"], "voice")
        heads = by["KIT-HOW-TO-HEADINGS"]
        self.assertEqual((heads["check"], heads["params"]), ("heading-case", {"case": "sentence"}))

    def test_missing(self):
        with self.assertRaises(SgcError):
            kit_candidates(FIXTURES / "nope")


class Edits(unittest.TestCase):
    def test_pairs(self):
        data = diff_pairs(FIXTURES / "edits")
        hunks = data["pairs"][0]["hunks"]
        self.assertEqual([(h["before"], h["after"], h["category"]) for h in hunks],
                         [("", ",", "punctuation"), ("Utilize", "Use", "words"),
                          ("it — it", "it—it", "spacing")])
        self.assertEqual(hunks[0]["original_sentence"], "We tested kites, boats and bikes.")
        self.assertEqual(hunks[0]["edited_sentence"], "We tested kites, boats, and bikes.")

    def test_v1_layout(self):
        data = diff_pairs(FIXTURES / "edits-v1")
        self.assertEqual((data["pair_count"], data["unpaired"]), (1, ["original/b.md"]))
        self.assertEqual(data["pairs"][0]["hunks"][0]["after"], "steady ")

    def test_case_and_wrap(self):
        self.assertEqual(diff_texts("the Plan", "the plan")[0]["category"], "case")
        self.assertEqual(diff_texts("a b\nc", "a b c"), [])


class Ledger(unittest.TestCase):
    def setUp(self):
        self._t = TempDir()
        self.tmp = self._t.__enter__()
        art = self.tmp / "a.md"
        art.write_text("# Kites\n\nThe Breeze 2 weighs 180 grams.\nIt flies in winds up to 40 km/h.\n"
                       "See [the old page](https://example.org/gone).\n", encoding="utf-8")
        self.run = self.tmp / "a.style-check"
        prepare(art, self.run)
        shutil.copytree(str(FIXTURES / "pages"), str(self.run / "facts" / "pages"))

    def tearDown(self):
        self._t.__exit__(None, None, None)

    def ledger(self, rows):
        (self.run / "facts" / "ledger.json").write_text(json.dumps(rows), encoding="utf-8")
        return ledger_run(self.run)

    def test_rows_and_findings(self):
        report, ok = self.ledger([
            {"id": "C1", "claim": "weighs 180 grams", "line": 3, "quote": "weighs 180 grams",
             "verdict": "confirmed", "source_url": "https://example.org/kite-facts",
             "excerpt": "The Breeze 2 kite weighs 180 grams"},
            {"id": "C2", "claim": "up to 40 km/h", "line": 4, "quote": "up to 40 km/h", "verdict": "contradicted",
             "source_url": "http://example.org/kite-facts/", "excerpt": "flies in winds from 8 to 25 km/h"},
            {"id": "C3", "claim": "old page", "line": 5, "quote": "the old page", "verdict": "link-dead",
             "source_url": "https://example.org/gone"},
            {"id": "C4", "claim": "who measured", "line": 3, "quote": "The Breeze 2", "verdict": "unverifiable"}])
        self.assertTrue(ok, report["rows"])
        facts = read_json(self.run / "findings" / "facts.json")
        self.assertEqual([f["rule_id"] for f in facts], ["FACT-CONTRADICTED", "FACT-LINK-DEAD", "FACT-UNVERIFIABLE"])
        self.assertIn("8 to 25 km/h", facts[0]["comment"])

    def test_blocked_fetch_is_unverifiable_not_dead(self):
        pages = self.run / "facts" / "pages"
        save_fetch({"url": "https://www.linkedin.com/posts/x", "final_url": "https://www.linkedin.com/posts/x",
                    "status": "blocked", "http_status": 403, "blocked": True,
                    "note": "HTTP 403, the page refused the fetch", "text": None, "html": None,
                    "content_type": None, "title": None, "fetched_at": "2026-11-10T00:00:00Z", "chars": 0}, pages)
        report, ok = self.ledger([{"id": "B1", "claim": "post", "line": 5, "quote": "the old page",
                                   "verdict": "link-dead", "source_url": "https://www.linkedin.com/posts/x"}])
        self.assertTrue(ok, report["rows"])
        self.assertEqual(report["rows"][0]["verdict"], "unverifiable")
        facts = read_json(self.run / "findings" / "facts.json")
        self.assertEqual([f["rule_id"] for f in facts], ["FACT-UNVERIFIABLE"])

    def test_failures(self):
        report, ok = self.ledger([
            {"id": "X1", "claim": "c", "line": 3, "quote": "weighs", "verdict": "confirmed",
             "source_url": "https://example.org/kite-facts", "excerpt": "weighs 999 grams"},
            {"id": "X2", "claim": "c", "line": 3, "quote": "weighs", "verdict": "confirmed",
             "source_url": "https://example.org/never-fetched", "excerpt": "x"},
            {"id": "X3", "claim": "c", "line": 3, "quote": "weighs", "verdict": "link-dead",
             "source_url": "https://example.org/kite-facts"},
            {"id": "X4", "claim": "c", "verdict": "contradicted", "source_url": "https://example.org/kite-facts",
             "excerpt": "Line length"}])
        self.assertFalse(ok)
        status = {r["id"]: r["status"] for r in report["rows"]}
        self.assertEqual(status, {"X1": "excerpt_not_found", "X2": "no_fetch", "X3": "link_alive", "X4": "no_anchor"})

    def test_normalization(self):
        _r, ok = self.ledger([{"id": "N1", "claim": "c", "verdict": "confirmed",
                               "source_url": "https://example.org/kite-facts?utm_source=x",
                               "excerpt": "THE BREEZE 2 KITE  weighs “180 grams”"}])
        self.assertFalse(ok)  # quotes are not on the page as quote marks, but text is
        _r, ok = self.ledger([{"id": "N2", "claim": "c", "verdict": "confirmed",
                               "source_url": "https://example.org/kite-facts?utm_source=x",
                               "excerpt": "THE BREEZE 2 KITE\n weighs 180   grams"}])
        self.assertTrue(ok)

    def test_bad_verdict(self):
        with self.assertRaises(SgcError):
            self.ledger([{"id": "B", "claim": "c", "verdict": "probably"}])


class ExtractFetch(unittest.TestCase):
    def test_html(self):
        md = html_to_markdown((FIXTURES / "page.html").read_text(encoding="utf-8"))
        self.assertTrue(md.startswith("# Kite facts\n"))
        for part in ("**Breeze 2**", "*180 grams*", "[^1]", "- Beginners use a 30 meter line.",
                     "[60 meters](https://example.org/lines)", "> A kite rises",
                     "![A red kite over a beach](/kite.png)", "[^1]: Measured by the Demo Co test team."):
            self.assertIn(part, md)
        self.assertNotIn("Home", md)
        self.assertNotIn("Copyright", md)

    def test_markdown_passthrough(self):
        with TempDir() as tmp:
            out = extract(FIXTURES / "article-clean.md", tmp / "x.md")
            self.assertEqual(out["kind"], "markdown-file")
            with self.assertRaises(SgcError):
                extract(tmp / "missing.md", tmp / "y.md")

    def test_fetch_save_and_index(self):
        self.assertEqual(normalize_url("HTTPS://Example.org/a/?utm_x=1&b=2"), "example.org/a?b=2")

        class Resp(object):
            status = 200
            headers = {"Content-Type": "text/html"}

            def __init__(self, body):
                self.body = body

            def read(self):
                return self.body

            def geturl(self):
                return "https://example.org/final"

            def getcode(self):
                return 200

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        html = (FIXTURES / "page.html").read_bytes()
        result = fetch_text("https://example.org/start", opener=lambda req, timeout: Resp(html))
        self.assertEqual(result["status"], "ok")
        self.assertIn("weighs 180 grams", result["text"])
        with TempDir() as tmp:
            sha = save_fetch(result, tmp)
            index = json.loads((tmp / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(index["example.org/start"], sha)
            self.assertEqual(index["example.org/final"], sha)
            self.assertEqual(sha, url_key("https://example.org/start"))
            failed = dict(result, status="error", text=None, html=None, note="HTTP 500")
            save_fetch(failed, tmp)
            self.assertFalse((tmp / ("%s.txt" % sha)).exists())


class Profile(unittest.TestCase):
    def test_counts(self):
        data = profile([str(FIXTURES / "article-violations.md"), str(FIXTURES / "article-clean.md")])
        t = data["totals"]
        self.assertEqual(data["articles"], 2)
        self.assertEqual((t["em_dash.spaced"], t["em_dash.closed"]), (1, 1))
        self.assertEqual((t["serial_comma.with"], t["serial_comma.without"]), (1, 1))
        self.assertEqual((t["percent.word"], t["percent.symbol"]), (1, 1))
        self.assertEqual((t["bold_labels.colon"], t["bold_labels.period"]), (3, 1))
        self.assertEqual(t["links.tracking"], 1)
        self.assertEqual(data["per_article"]["article-clean.md"].get("headings.h2.sentence"), 1)

    def test_digit_count_skips_list_numbers_and_times(self):
        with TempDir() as d:
            p = d / "a.md"
            p.write_text("# T\n\n1. Post it at 9 a.m. with 3 tiles.\n2. Raise it 4 percent.\n", encoding="utf-8")
            t = profile([str(p)])["totals"]
        self.assertEqual(t.get("numerals.under_10_digits"), 1)


class Cli(unittest.TestCase):
    def call(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                code = sgc.main(list(argv))
            except SystemExit as exc:
                code = exc.code
        return code, out.getvalue(), err.getvalue()

    def test_validate_and_parse(self):
        code, out, _ = self.call("guide", "validate", str(FIXTURES / "guide-v2.md"))
        self.assertEqual((code, json.loads(out)["valid"]), (0, True))
        code, out, _ = self.call("guide", "validate", str(FIXTURES / "guide-v1.md"))
        self.assertEqual(code, 1)
        code, out, _ = self.call("guide", "parse", str(FIXTURES / "guide-v1.md"))
        self.assertEqual(json.loads(out)["schema_version"], 1)

    def test_missing_input_exits_2(self):
        code, _, err = self.call("guide", "parse", str(FIXTURES / "nope.md"))
        self.assertEqual(code, 2)
        self.assertIn("missing style guide", err)
        code, _, err = self.call("findings", "--run-dir", str(FIXTURES / "nope"))
        self.assertEqual(code, 2)

    def test_end_to_end(self):
        with TempDir() as tmp:
            art = tmp / "post.md"
            shutil.copy(str(FIXTURES / "article-violations.md"), str(art))
            run = str(tmp / "post.style-check")
            g = str(FIXTURES / "guide-v2.md")
            for argv in (["prepare", str(art), "--run-dir", run], ["packets", g, "--run-dir", run],
                         ["lint", g, "--run-dir", run], ["findings", "--run-dir", run],
                         ["verdicts", "--run-dir", run], ["report", "--run-dir", run, "--guide", g],
                         ["apply", "--run-dir", run, "--accept", "auto"]):
                code, out, err = self.call(*argv)
                self.assertEqual(code, 0, (argv, err))
                json.loads(out)
            self.assertTrue((tmp / "post_edited.md").exists())


if __name__ == "__main__":
    unittest.main()
