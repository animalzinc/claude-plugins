"""The check pipeline over a run folder."""
import json
import shutil
import unittest

from helpers import FIXTURES, TempDir

from sgclib.apply import apply_edits, apply_run
from sgclib.article import Article
from sgclib.common import SgcError, read_json
from sgclib.findings import decisions_run, findings_run, lint_run, verdicts_run
from sgclib.prepare import packets, prepare
from sgclib.report import report_run

GUIDE = str(FIXTURES / "guide-v2.md")
GUIDE_V1 = str(FIXTURES / "guide-v1.md")


def write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = TempDir()
        self.tmp = self._tmp.__enter__()
        self.article = self.tmp / "draft.md"
        shutil.copy(str(FIXTURES / "article-violations.md"), str(self.article))
        self.run = self.tmp / "draft.style-check"

    def tearDown(self):
        self._tmp.__exit__(None, None, None)

    def lint(self, guide=GUIDE):
        prepare(self.article, self.run)
        return lint_run(guide, self.run)

    def lint_findings(self):
        return read_json(self.run / "findings" / "lint.json")


class Numbering(unittest.TestCase):
    def test_numbered_prefix_and_width(self):
        art = Article("a\nb")
        self.assertEqual(art.numbered(), "L0001| a\nL0002| b\n")
        self.assertTrue(Article("x\n" * 12000).numbered().startswith("L00001| x"))

    def test_protected_zones(self):
        art = Article('---\ntitle: x\n---\nSee `code` at https://ex.com and "a quote".\n> quoted\n```\nfence\n```')
        kinds = {(z[2]) for n in art.numbers() for z in art.zones(n)}
        self.assertEqual(kinds, {"frontmatter", "code", "url", "quote", "blockquote"})
        self.assertEqual(art.zone_at(4, 4, 10), "code")
        outline = art.outline()
        self.assertEqual(outline["links"][0]["url"], "https://ex.com")


class Prepare(Base):
    def test_outputs_and_content_type(self):
        out = prepare(self.article, self.run)
        self.assertEqual(out["content_type"], "how-to")
        numbered = (self.run / "article.numbered.md").read_text(encoding="utf-8")
        self.assertTrue(numbered.startswith("L0001| ---"))
        outline = read_json(self.run / "outline.json")
        self.assertEqual(outline["headings"][1], {"line": 8, "level": 2, "text": "How The Kite Flies"})
        link = outline["links"][0]
        self.assertEqual((link["anchor"], link["line"]), ("kite manual", 15))
        self.assertIn("Click here", link["sentence"])

    def test_rerun_clears_generated_files(self):
        prepare(self.article, self.run)
        (self.run / "findings" / "usage.json").write_text("[]", encoding="utf-8")
        (self.run / "report.md").write_text("old", encoding="utf-8")
        out = prepare(self.article, self.run)
        self.assertFalse((self.run / "findings" / "usage.json").exists())
        self.assertEqual((self.run / "report.previous.md").read_text(encoding="utf-8"), "old")
        self.assertIn("findings", out["cleared"])

    def test_missing_article(self):
        with self.assertRaises(SgcError):
            prepare(self.tmp / "nope.md", self.run)


class Packets(Base):
    def test_index_and_mechanical(self):
        prepare(self.article, self.run, content_type="essay")
        index = packets(GUIDE, self.run)
        by = {p["reviewer"]: p for p in index["packets"]}
        self.assertEqual(sorted(by), ["mechanical", "voice"])
        self.assertEqual(by["voice"]["rule_ids"], ["WORD-TONE"])
        self.assertEqual(by["mechanical"]["output"], "mechanical-confirmed.json")
        mech = (self.run / "packets" / "mechanical.md").read_text(encoding="utf-8")
        self.assertIn("Check `dash-spacing` with parameters", mech)
        voice = (self.run / "packets" / "voice.md").read_text(encoding="utf-8")
        self.assertNotIn("PUNC-EMDASH", voice)
        self.assertTrue((self.run / "packets" / "index.json").exists())

    def test_split(self):
        prepare(self.article, self.run, content_type="essay")
        index = packets(GUIDE, self.run, split_above=10)
        names = [p["packet"] for p in index["packets"]]
        self.assertEqual(names, ["packets/voice.md", "packets/mechanical.md"])
        index = packets(GUIDE_V1, self.run, split_above=3)
        outs = [p["output"] for p in index["packets"]]
        self.assertIn("usage-1.json", outs)
        self.assertIn("usage-2.json", outs)

    def test_scoped_guide_needs_type(self):
        art = self.tmp / "plain.md"
        art.write_text("# Plain\n\nText.\n", encoding="utf-8")
        prepare(art, self.run)
        with self.assertRaises(SgcError):
            packets(GUIDE, self.run)


class LintStep(Base):
    def test_ids_and_certainty(self):
        out = self.lint()
        found = self.lint_findings()
        self.assertEqual(out["findings"], len(found))
        self.assertEqual(found[0]["id"], "L0001")
        self.assertTrue(all(f["certainty"] in ("certain", "uncertain") for f in found))
        rules = {f["rule_id"] for f in found}
        self.assertGreaterEqual(len(rules), 18)
        lines = (self.run / "article.md").read_text(encoding="utf-8").split("\n")
        for f in found:
            self.assertEqual(lines[f["line"] - 1][f["col"]:f["col"] + len(f["quote"])], f["quote"])

    def test_v1_guide_lints_empty(self):
        out = self.lint(GUIDE_V1)
        self.assertEqual((out["findings"], out["schema_version"]), (0, 1))
        self.assertEqual(self.lint_findings(), [])


class FindingsStep(Base):
    def setUp(self):
        Base.setUp(self)
        self.lint()
        self.fdir = self.run / "findings"

    def test_reanchor_drop_scope_protected_rule(self):
        write(self.fdir / "structure.json", {"findings": [
            {"rule_id": "WORD-INTRO", "line": 99, "quote": "Strong wind is fun", "replacement": None,
             "comment": "lead with the outcome", "basis": "inferred"},
            {"rule_id": "WORD-INTRO", "line": 10, "quote": "nowhere in the text", "replacement": None},
            {"rule_id": "WORD-INTRO", "line": 99, "quote": "kite", "replacement": None},
            {"rule_id": "WORD-TONE", "line": 10, "quote": "risky", "replacement": None},
            {"rule_id": "WORD-INTRO", "line": 11, "quote": "the plan", "replacement": None},
            {"rule_id": "MADE-UP", "line": 10, "quote": "risky"},
            {"line": 10, "quote": "risky"},
        ]})
        out = findings_run(self.run)
        merged = read_json(self.fdir / "merged.json")
        drops = read_json(self.fdir / "drops.json")
        moved = [f for f in merged if f["pass"] == "structure"]
        self.assertEqual(len(moved), 1)
        self.assertEqual((moved[0]["line"], moved[0]["moved_from"], moved[0]["status"]), (10, 99, "pending"))
        self.assertTrue(moved[0]["id"].startswith("F"))
        stages = sorted(d["stage"] for d in drops if d["pass"] == "structure")
        self.assertEqual(stages, ["anchor", "anchor", "malformed", "protected", "rule", "scope"])
        reasons = " ".join(d["reason"] for d in drops)
        self.assertIn("quote not found", reasons)
        self.assertIn("found", reasons)
        self.assertEqual(out["verify_packets"][0]["output"], "verify/structure.verdicts.json")
        packet = (self.run / "verify" / "structure.md").read_text(encoding="utf-8")
        self.assertIn("### WORD-INTRO: Open with the point", packet)
        self.assertIn("L0010| Strong wind", packet)

    def test_confirmer_answers(self):
        lint = read_json(self.fdir / "lint.json")
        uncertain = [f["id"] for f in lint if f["certainty"] == "uncertain"]
        self.assertGreaterEqual(len(uncertain), 2)
        findings_run(self.run)
        merged = {f["id"]: f for f in read_json(self.fdir / "merged.json")}
        self.assertEqual(merged[uncertain[0]]["basis"], "inferred")
        self.assertEqual(merged[uncertain[0]]["status"], "auto")
        write(self.fdir / "mechanical-confirmed.json", [{"id": uncertain[0], "applies": False, "reason": "proper noun"},
                                                       {"id": uncertain[1], "applies": True}])
        findings_run(self.run)
        merged = {f["id"]: f for f in read_json(self.fdir / "merged.json")}
        self.assertNotIn(uncertain[0], merged)
        self.assertEqual((merged[uncertain[1]]["basis"], merged[uncertain[1]]["confirmed"]), ("explicit", True))

    def test_merge_and_decisions(self):
        lint = read_json(self.fdir / "lint.json")
        dash = next(f for f in lint if f["rule_id"] == "PUNC-EMDASH")
        write(self.fdir / "usage.json", [{"rule_id": "PUNC-EMDASH", "line": dash["line"], "quote": "fun —",
                                          "replacement": "fun—", "basis": "explicit"}])
        findings_run(self.run)
        merged = read_json(self.fdir / "merged.json")
        self.assertEqual(next(f for f in merged if f["id"] == dash["id"])["also_found_by"], ["usage"])
        brand = self.tmp / "brand"
        brand.mkdir()
        verdicts_run(self.run)
        decisions_run(self.run, [dash["id"]], brand, reason="house exception")
        row = json.loads((brand / "decisions.jsonl").read_text(encoding="utf-8").strip())
        self.assertEqual((row["rule_id"], row["quote"]), ("PUNC-EMDASH", dash["quote"]))
        findings_run(self.run, decisions_path=brand / "decisions.jsonl")
        ids = {f["id"] for f in read_json(self.fdir / "merged.json")}
        self.assertNotIn(dash["id"], ids)
        self.assertIn("decision", {d["stage"] for d in read_json(self.fdir / "drops.json")})

    def test_proofreading_counts_inside_quotes_not_code(self):
        lines = (self.run / "article.md").read_text(encoding="utf-8").split("\n")
        quote_line = next(i + 1 for i, l in enumerate(lines) if '"the plan"' in l)
        code_line = next(i + 1 for i, l in enumerate(lines) if "a code sample" in l)
        write(self.fdir / "proof.json", [
            {"rule_id": "PROOF-TYPO", "line": quote_line, "quote": "the plan", "replacement": "the plans", "basis": "explicit"},
            {"rule_id": "PROOF-TYPO", "line": code_line, "quote": "a code sample", "replacement": "a code example", "basis": "explicit"}])
        findings_run(self.run)
        kept = [f for f in read_json(self.fdir / "merged.json") if f["pass"] == "proof"]
        self.assertEqual([f["line"] for f in kept], [quote_line])
        dropped = [d for d in read_json(self.fdir / "drops.json") if d["pass"] == "proof"]
        self.assertEqual([(d["stage"], d["finding"]["line"]) for d in dropped], [("protected", code_line)])

    def test_same_fix_under_two_rules_merges(self):
        lint = read_json(self.fdir / "lint.json")
        name = next(f for f in lint if f["rule_id"] == "WORD-NAMES")
        write(self.fdir / "proof.json", [{"rule_id": "PROOF-NAME", "line": name["line"], "quote": name["quote"],
                                          "replacement": name["replacement"], "basis": "explicit"}])
        findings_run(self.run)
        merged = read_json(self.fdir / "merged.json")
        self.assertEqual([f for f in merged if f["pass"] == "proof"], [])
        self.assertEqual(next(f for f in merged if f["id"] == name["id"])["also_found_by"], ["proof"])

    def test_split_kit_rule_merges_on_same_text(self):
        rules_path = self.run / "rules.json"
        data = read_json(rules_path)
        for r in data["rules"]:
            if r["id"] == "PUNC-EMDASH":
                r["source"] = "kit:k7#dash-spacing"
            elif r["id"] == "WORD-INTRO":
                r["source"] = "kit:k7"
            elif r["id"] == "WORD-NAMES":
                r["source"] = "kit:k8#term-case"
        write(rules_path, data)
        lint = read_json(self.fdir / "lint.json")
        dash = next(f for f in lint if f["rule_id"] == "PUNC-EMDASH")
        name = next(f for f in lint if f["rule_id"] == "WORD-NAMES")
        write(self.fdir / "usage.json", [
            {"rule_id": "WORD-INTRO", "line": dash["line"], "quote": dash["quote"], "replacement": None,
             "comment": "Close up the dash.", "basis": "explicit"},
            {"rule_id": "WORD-INTRO", "line": name["line"], "quote": name["quote"], "replacement": None,
             "comment": "Another kit rule.", "basis": "explicit"}])
        findings_run(self.run)
        merged = read_json(self.fdir / "merged.json")
        on_dash = [f for f in merged if f["line"] == dash["line"] and f["quote"] == dash["quote"]]
        self.assertEqual([(f["id"], f["replacement"]) for f in on_dash], [(dash["id"], dash["replacement"])])
        self.assertEqual(on_dash[0]["also_found_by"], ["usage"])
        merged_drop = next(d for d in read_json(self.fdir / "drops.json") if d["stage"] == "merged")
        self.assertIn("kit:k7", merged_drop["reason"])
        on_name = [f["rule_id"] for f in merged if f["line"] == name["line"] and f["quote"] == name["quote"]]
        self.assertEqual(sorted(on_name), ["WORD-INTRO", "WORD-NAMES"])

    def test_needs_lint(self):
        (self.fdir / "lint.json").unlink()
        with self.assertRaises(SgcError):
            findings_run(self.run)


class VerdictsReportApply(Base):
    def setUp(self):
        Base.setUp(self)
        self.lint()
        self.fdir = self.run / "findings"
        write(self.fdir / "proof.json", [
            {"rule_id": "PROOF-DOUBLED", "line": 15, "quote": "to the team", "replacement": "to the whole team"},
            {"rule_id": "PROOF-TYPO", "line": 18, "quote": "slowly", "replacement": "slowley"}])
        findings_run(self.run)
        self.pending = [f["id"] for f in read_json(self.fdir / "merged.json") if f["status"] == "pending"]

    def test_missing_verdicts_refused(self):
        with self.assertRaises(SgcError):
            verdicts_run(self.run)

    def test_verdicts_report_apply(self):
        write(self.run / "verify" / "proof.verdicts.json", [
            {"id": self.pending[0], "verdict": "revise", "reason": "smaller", "replacement": "to our team"},
            {"id": self.pending[1], "verdict": "drop", "reason": "not a typo"}])
        out = verdicts_run(self.run)
        self.assertEqual((out["revised"], out["dropped_by_verifier"]), (1, 1))
        rep = report_run(self.run, GUIDE)
        text = (self.run / "report.md").read_text(encoding="utf-8")
        self.assertIn("## Violations", text)
        self.assertIn("## Suggestions", text)
        self.assertIn("WORD-BANNED", text.split("## Suggestions")[1])
        self.assertIn("not a typo", text)
        self.assertGreater(rep["violations"], 10)

        res = apply_run(self.run, "auto," + self.pending[0])
        edited = (self.tmp / "draft_edited.md").read_text(encoding="utf-8")
        self.assertIn("Strong wind is fun—and risky.", edited)
        self.assertIn("to our team", edited)
        self.assertIn("---\ntitle:", edited)
        self.assertEqual(self.article.read_text(encoding="utf-8"),
                         (FIXTURES / "article-violations.md").read_text(encoding="utf-8"))
        self.assertLess(res["relint"]["findings"], len(read_json(self.fdir / "lint.json")))

        res = apply_run(self.run, "auto", in_place=True)
        self.assertTrue((self.tmp / "draft.bak").exists())
        self.assertIn("fun—and", self.article.read_text(encoding="utf-8"))
        with self.assertRaises(SgcError):
            apply_run(self.run, "auto", in_place=True)

    def test_overlaps_refused(self):
        lines = ["one two three"]
        findings = [{"id": "A", "line": 1, "quote": "one two", "replacement": "1 2"},
                    {"id": "B", "line": 1, "quote": "two three", "replacement": "2 3"},
                    {"id": "C", "line": 1, "quote": "three", "replacement": None}]
        out, applied, refused = apply_edits(lines, findings)
        self.assertEqual((out, applied), (lines, []))
        self.assertEqual(sorted(r["id"] for r in refused), ["A", "B", "C"])
        out, applied, _ = apply_edits(["one two three"], [
            {"id": "A", "line": 1, "quote": "one", "replacement": "uno"},
            {"id": "B", "line": 1, "quote": "three", "replacement": "tres"}])
        self.assertEqual(out, ["uno two tres"])


class V1Pipeline(Base):
    def test_report_with_v1_guide(self):
        self.lint(GUIDE_V1)
        index = packets(GUIDE_V1, self.run)
        self.assertIn("usage", [p["reviewer"] for p in index["packets"]])
        write(self.run / "findings" / "usage.json", [
            {"rule_id": "V1-2.1", "line": 10, "quote": "boats and", "replacement": "boats, and"}])
        findings_run(self.run, guide_path=GUIDE_V1)
        pending = [f["id"] for f in read_json(self.run / "findings" / "merged.json")]
        write(self.run / "verify" / "usage.verdicts.json", [{"id": pending[0], "verdict": "keep", "reason": "list"}])
        verdicts_run(self.run)
        report_run(self.run, GUIDE_V1)
        text = (self.run / "report.md").read_text(encoding="utf-8")
        self.assertIn("v1 format", text)
        self.assertIn("V1-2.1", text)


if __name__ == "__main__":
    unittest.main()
