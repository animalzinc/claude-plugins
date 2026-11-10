"""Guide parse, validate, render, diff, checklist, index-v1, brand-path."""
import json
import os
import unittest

from helpers import FIXTURES, TempDir

from sgclib import guide as G
from sgclib.common import SgcError, read_text

V2 = read_text(FIXTURES / "guide-v2.md")
V1 = read_text(FIXTURES / "guide-v1.md")
CHECKS_USED = {"dash-spacing", "heading-case", "heading-format", "serial-comma", "banned", "preferred",
               "term-case", "numerals", "ordinals", "sentence-start-numeral", "percent", "money",
               "thousands", "date-format", "time-format", "quote-style", "bold-label", "link-hygiene", "regex"}

MINI = """---
schema_version: 2
brand: Mini
content_types: [essay]
generated: false
---

# Mini style guide

## Punctuation

### P-DASH: Close dashes
```rule
severity: must
scope: all
kind: mechanical
check: dash-spacing
style: closed
source: manual
evidence: invented
```
Hand-written prose that render keeps.

✅ late—again

### P-KEEP: Short sentences
```rule
severity: should
scope: all
kind: usage
source: kit:k1
evidence: kit
```
Keep sentences short.

## Retired

- P-OLD: gone
"""


class Parse(unittest.TestCase):
    def test_fixture_uses_every_check(self):
        guide, problems = G.parse_guide(V2)
        self.assertEqual(problems, [])
        self.assertEqual({r["check"] for r in guide["rules"] if r["check"]}, CHECKS_USED)
        emdash = next(r for r in guide["rules"] if r["id"] == "PUNC-EMDASH")
        self.assertEqual((emdash["params"], emdash["section"], emdash["severity"]),
                         ({"style": "closed", "ranges": "en-dash"}, "Punctuation", "must"))
        self.assertEqual(guide["retired"], [{"id": "PUNC-OLD", "reason": "replaced by PUNC-EMDASH"}])
        tone = next(r for r in guide["rules"] if r["id"] == "WORD-TONE")
        self.assertEqual(tone["scope"], ["essay"])

    def test_schema_version_detection(self):
        self.assertEqual(G.schema_version_of(V2), 2)
        self.assertEqual(G.schema_version_of(V1), 1)
        self.assertIsNone(G.schema_version_of("# Notes\n\nNothing here."))


class Validate(unittest.TestCase):
    def test_fixture_is_valid(self):
        result = G.validate_guide(V2)
        self.assertEqual((result["valid"], result["errors"], result["warnings"]), (True, [], []))

    def _errors(self, text):
        return "\n".join(G.validate_guide(text)["errors"])

    def test_duplicate_unknown_params_scope_retired_example(self):
        bad = MINI.replace("### P-KEEP", "### P-DASH").replace("style: closed", "style: closed\ncolor: red")
        errs = self._errors(bad)
        self.assertIn("duplicate ID", errs)
        self.assertIn("no parameter 'color'", errs)
        self.assertIn("unknown check", self._errors(MINI.replace("check: dash-spacing", "check: sparkle")))
        self.assertIn("not in content_types", self._errors(MINI.replace("scope: all\nkind: usage", "scope: [how-to]\nkind: usage")))
        self.assertIn("retired IDs are never reused", self._errors(MINI.replace("P-KEEP", "P-OLD", 1)))
        self.assertIn("missing field evidence", self._errors(MINI.replace("evidence: kit\n", "")))
        self.assertIn("flagged by the rule's own check", self._errors(MINI.replace("✅ late—again", "✅ late — again")))
        self.assertIn("schema_version must be 2", self._errors(MINI.replace("schema_version: 2", "schema_version: 3")))


class Render(unittest.TestCase):
    def test_new_guide_round_trips(self):
        proposal = {"frontmatter": {"brand": "Fresh", "content_types": ["essay"], "generated": False},
                    "rules": [{"id": "A-ONE", "title": "Close dashes", "section": "Punctuation",
                               "block": {"severity": "must", "scope": "all", "kind": "mechanical",
                                         "check": "dash-spacing", "style": "closed", "source": "manual",
                                         "evidence": "3 of 3"},
                               "body": "✅ a—b"}]}
        text, report = G.render(proposal)
        self.assertEqual(report["added"], ["A-ONE"])
        self.assertTrue(G.validate_guide(text)["valid"], G.validate_guide(text)["errors"])
        self.assertIn(G.CHECK_START, text)
        self.assertIn("- [ ] A-ONE: Close dashes", text)

    def test_existing_keeps_text_and_retires(self):
        proposal = {"rules": [{"id": "P-NEW", "title": "New rule", "section": "Words",
                               "block": {"severity": "prefer", "scope": "all", "kind": "usage",
                                         "source": "articles", "evidence": "2 of 9"}, "body": "Prose."}],
                    "retire": [{"id": "P-DASH", "reason": "brand changed"}]}
        text, report = G.render(proposal, MINI)
        self.assertEqual((report["added"], report["retired"]), (["P-NEW"], ["P-DASH"]))
        self.assertIn("Keep sentences short.", text)
        self.assertIn("- P-DASH: brand changed", text)
        self.assertIn("- P-OLD: gone", text)
        self.assertNotIn("### P-DASH", text)

    def test_unchanged_rule_keeps_raw_text(self):
        guide, _ = G.parse_guide(MINI)
        r = next(x for x in guide["rules"] if x["id"] == "P-DASH")
        proposal = {"rules": [{"id": "P-DASH", "title": r["title"], "block": dict(r["fields"]), "body": r["body"]}]}
        text, report = G.render(proposal, MINI)
        self.assertEqual(report["unchanged"], ["P-DASH"])

    def test_complete_retires_missing_rules(self):
        guide, _ = G.parse_guide(MINI)
        r = next(x for x in guide["rules"] if x["id"] == "P-DASH")
        proposal = {"complete": True,
                    "rules": [{"id": "P-DASH", "title": r["title"], "block": dict(r["fields"]), "body": r["body"]}]}
        _text, report = G.render(proposal, MINI)
        self.assertEqual(report["retired"], ["P-KEEP"])

    def test_reusing_retired_id_refused(self):
        proposal = {"rules": [{"id": "P-OLD", "title": "x", "section": "S",
                               "block": {"severity": "must", "scope": "all", "kind": "usage",
                                         "source": "manual", "evidence": "x"}}]}
        with self.assertRaises(SgcError):
            G.render(proposal, MINI)

    def test_kit_source_keeps_existing_metadata(self):
        proposal = {"rules": [{"title": "Short sentences", "block": {"source": "kit:k1", "evidence": "kit v2"},
                               "body": "Keep sentences under 20 words."}]}
        text, report = G.render(proposal, MINI)
        self.assertEqual((report["kit_matched"], report["changed"]), (["P-KEEP"], ["P-KEEP"]))
        new, _ = G.parse_guide(text)
        rule = next(r for r in new["rules"] if r["id"] == "P-KEEP")
        self.assertEqual((rule["severity"], rule["kind"], rule["scope"], rule["evidence"]),
                         ("should", "usage", "all", "kit v2"))
        diff = G.diff_guides(MINI, text)
        self.assertEqual([m["id"] for m in diff["modified"]], ["P-KEEP"])
        self.assertEqual(diff["changed"], [])

    def test_kit_rule_split_by_check_matches_each_part(self):
        def part(rid, check, params, body):
            block = {"severity": "should", "scope": "all", "kind": "mechanical", "check": check,
                     "source": "kit:k9#" + check, "evidence": "kit"}
            block.update(params)
            return {"id": rid, "title": rid.title(), "section": "Numbers", "block": block, "body": body}
        first = {"frontmatter": {"schema_version": 2, "brand": "Demo Co", "content_types": []},
                 "rules": [part("NUM-PCT", "percent", {"style": "symbol"}, "Use 70%."),
                           part("NUM-MONEY", "money", {"style": "abbreviated"}, "Write $2.6M.")]}
        guide, _ = G.render(first)
        again = {"rules": [{"title": "Percent", "block": {"source": "kit:k9#percent", "evidence": "kit v2"},
                            "body": "Use 70%, never 70 percent."},
                           {"title": "Money", "block": {"source": "kit:k9#money", "evidence": "kit v2"},
                            "body": "Write $2.6M and $1.2B."}]}
        text, report = G.render(again, guide)
        self.assertEqual(sorted(report["kit_matched"]), ["NUM-MONEY", "NUM-PCT"])
        new, _ = G.parse_guide(text)
        by_id = {r["id"]: r for r in new["rules"]}
        self.assertEqual((by_id["NUM-PCT"]["check"], by_id["NUM-MONEY"]["check"]), ("percent", "money"))
        self.assertEqual(len(new["rules"]), 2)

    def test_kit_source_proposal_value_wins(self):
        proposal = {"rules": [{"title": "Short sentences", "block": {"source": "kit:k1", "evidence": "kit",
                                                                     "severity": "must"}, "body": "Keep sentences short."}]}
        text, _ = G.render(proposal, MINI)
        new, _ = G.parse_guide(text)
        self.assertEqual(next(r for r in new["rules"] if r["id"] == "P-KEEP")["severity"], "must")


class DiffChecklist(unittest.TestCase):
    def test_diff(self):
        new = MINI.replace("severity: must", "severity: should").replace("- P-OLD: gone", "- P-OLD: gone\n- P-KEEP: merged")
        new = new.replace("### P-KEEP: Short sentences", "### P-GONE: Short sentences", 1)
        d = G.diff_guides(MINI, new)
        self.assertEqual([c["id"] for c in d["changed"]], ["P-DASH"])
        self.assertEqual(d["changed"][0]["fields"]["severity"], ["must", "should"])
        self.assertEqual([a["id"] for a in d["added"]], ["P-GONE"])
        self.assertEqual([r["id"] for r in d["retired"]], ["P-KEEP"])
        self.assertIn("Changed (1)", G.diff_markdown(d))

    def test_checklist_adds_and_rewrites(self):
        text, added = G.write_checklist(MINI)
        self.assertTrue(added)
        self.assertLess(text.index(G.CHECK_START), text.index("## Retired"))
        again, added2 = G.write_checklist(text.replace("- [ ] P-KEEP", "- [ ] stale"))
        self.assertFalse(added2)
        self.assertIn("- [ ] P-KEEP: Short sentences", again)
        self.assertEqual(again, text)


class IndexV1(unittest.TestCase):
    def test_index(self):
        data = G.index_v1(V1)
        by_id = {r["id"]: r for r in data["rules"]}
        self.assertEqual(sorted(by_id), sorted(["V1-1.1", "V1-1.2", "V1-2.1", "V1-2.2", "V1-2.2.1", "V1-3.1",
                                                 "V1-4.1", "V1-5.1", "V1-6.1", "V1-7.1", "V1-8.1"]))
        self.assertEqual(by_id["V1-1.1"]["kind"], "voice")
        self.assertEqual(by_id["V1-1.1"]["severity"], "must")
        self.assertEqual(by_id["V1-1.2"]["severity"], "should")
        self.assertEqual(by_id["V1-2.1"]["severity"], "must")
        self.assertEqual(by_id["V1-3.1"]["kind"], "mechanical")
        self.assertEqual(by_id["V1-4.1"]["kind"], "structure")
        self.assertTrue(all(r["check"] is None for r in data["rules"]))
        self.assertEqual(G.load_rules(FIXTURES / "guide-v1.md")["schema_version"], 1)


class BrandPath(unittest.TestCase):
    def test_resolution(self):
        with TempDir() as tmp:
            (tmp / "brands" / "demo-co").mkdir(parents=True)
            (tmp / "brands" / "demo-co" / "style-guide.md").write_text(V2, encoding="utf-8")
            out = G.brand_path("Demo Co", guides_dir="${user_config.guides_dir}", project_dir=str(tmp))
            self.assertEqual(out["ignored_guides_dir"]["reason"], "unresolved variable")
            self.assertTrue(out["brand_dir_exists"])
            self.assertEqual(out["schema_version"], 2)
            out = G.brand_path("demo-co", guides_dir=str(tmp / "brands"))
            self.assertEqual(out["guides_dir_source"], "--guides-dir")
            out = G.brand_path("other", guides_dir="relative/path", project_dir=str(tmp))
            self.assertEqual(out["ignored_guides_dir"]["reason"], "not an absolute path")
            self.assertFalse(out["brand_dir_exists"])
            out = G.brand_path("x", project_dir=str(tmp), guide=str(FIXTURES / "guide-v1.md"))
            self.assertEqual(out["schema_version"], 1)
            with self.assertRaises(SgcError):
                G.brand_path("x", project_dir=str(tmp), guide=str(tmp / "missing.md"))


if __name__ == "__main__":
    unittest.main()


class RuleBlockValues(unittest.TestCase):
    def test_apostrophe_inside_unquoted_item(self):
        from sgclib import yamlish as Y
        self.assertEqual(Y.parse_value("[in today's fast-paced world, delve, \"a, b\", 'quoted']"),
                         ["in today's fast-paced world", "delve", "a, b", "quoted"])

    def test_unclosed_opening_quote_still_refused(self):
        from sgclib import yamlish as Y
        with self.assertRaises(SgcError):
            Y.parse_value('["open, closed]')
