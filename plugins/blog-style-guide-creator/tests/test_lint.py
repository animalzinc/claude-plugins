"""Every lint check, in both directions of its parameters."""
import unittest

from helpers import hits, quotes

EM, EN = "—", "–"


class DashSpacing(unittest.TestCase):
    def test_closed_flags_spaced(self):
        self.assertEqual(quotes("dash-spacing", {"style": "closed"}, "It was late %s again." % EM),
                         [("late %s again." % EM, "late%sagain." % EM)])

    def test_spaced_flags_closed(self):
        self.assertEqual(quotes("dash-spacing", {"style": "spaced"}, "It was late%sagain." % EM),
                         [("late%sagain." % EM, "late %s again." % EM)])

    def test_each_style_accepts_its_own(self):
        self.assertEqual(hits("dash-spacing", {"style": "closed"}, "late%sagain" % EM), [])
        self.assertEqual(hits("dash-spacing", {"style": "spaced"}, "late %s again" % EM), [])

    def test_none_flags_every_dash(self):
        found = hits("dash-spacing", {"style": "none"}, "a%sb and c %s d" % (EM, EM))
        self.assertEqual(len(found), 2)
        self.assertIsNone(found[0]["replacement"])

    def test_none_skips_sign_off_lines(self):
        for line in ("%s Ty Magnin" % EM, "  *%s Ty Magnin*" % EM, "> %s Ty Magnin" % EM, "%sJ. R. Smith" % EM):
            self.assertEqual(hits("dash-spacing", {"style": "none"}, "Thanks for reading.\n\n" + line), [], line)
        self.assertEqual(len(hits("dash-spacing", {"style": "none"}, "%s Ty Magnin said so" % EM)), 1)
        self.assertEqual(len(hits("dash-spacing", {"style": "none"}, "We flew %s Ty Magnin" % EM)), 1)

    def test_spaced_hyphen_and_en_dash_as_em_dash(self):
        self.assertEqual(quotes("dash-spacing", {"style": "closed"}, "fun - and risky"),
                         [("fun - and", "fun%sand" % EM)])
        self.assertEqual(quotes("dash-spacing", {"style": "spaced"}, "fun %s and risky" % EN),
                         [("fun %s and" % EN, "fun %s and" % EM)])

    def test_ranges_both_ways(self):
        self.assertEqual(quotes("dash-spacing", {"style": "closed", "ranges": "en-dash"}, "pages 10-20"),
                         [("10-20", "10%s20" % EN)])
        self.assertEqual(hits("dash-spacing", {"style": "closed", "ranges": "en-dash"}, "pages 10%s20" % EN), [])
        self.assertEqual(quotes("dash-spacing", {"style": "closed", "ranges": "hyphen"}, "pages 10%s20" % EN),
                         [("10%s20" % EN, "10-20")])
        self.assertEqual(hits("dash-spacing", {"style": "closed", "ranges": "hyphen"}, "pages 10-20"), [])

    def test_dates_and_list_markers_are_not_ranges_or_dashes(self):
        self.assertEqual(hits("dash-spacing", {"style": "closed", "ranges": "en-dash"}, "On 2026-11-09 we met."), [])
        self.assertEqual(hits("dash-spacing", {"style": "closed"}, "- a list item"), [])

    def test_protected_zones_skipped(self):
        text = "`a %s b`\n> a %s b\nShe said \"late %s again\".\n```\nx %s y\n```" % (EM, EM, EM, EM)
        self.assertEqual(hits("dash-spacing", {"style": "closed"}, text), [])


class HeadingCase(unittest.TestCase):
    def test_sentence_flags_title(self):
        found = hits("heading-case", {"case": "sentence"}, "## How The Kite Flies\n\nthe kite flies")
        self.assertEqual(found[0]["replacement"], "How the kite flies")
        self.assertEqual(found[0]["certainty"], "certain")

    def test_title_flags_sentence(self):
        self.assertEqual(quotes("heading-case", {"case": "title"}, "## How the kite flies"),
                         [("How the kite flies", "How the Kite Flies")])

    def test_sentence_keeps_weekdays_and_months(self):
        self.assertEqual(hits("heading-case", {"case": "sentence"}, "## A different Monday in March"), [])
        self.assertEqual(quotes("heading-case", {"case": "sentence"}, "## Plans You May Like"),
                         [("Plans You May Like", "Plans you may like")])

    def test_each_case_accepts_its_own(self):
        self.assertEqual(hits("heading-case", {"case": "sentence"}, "## How the kite flies"), [])
        self.assertEqual(hits("heading-case", {"case": "title"}, "## How the Kite Flies"), [])

    def test_possible_proper_noun_is_uncertain(self):
        found = hits("heading-case", {"case": "sentence"}, "## Flying with Portia")
        self.assertEqual(found[0]["certainty"], "uncertain")

    def test_acronyms_and_camel_case_left_alone(self):
        self.assertEqual(hits("heading-case", {"case": "sentence"}, "## Using the API with KiteKit"), [])

    def test_levels(self):
        self.assertEqual(hits("heading-case", {"case": "sentence", "levels": [2]}, "### How The Kite Flies"), [])

    def test_ap_and_cmos_prepositions(self):
        cmos = hits("heading-case", {"case": "title", "style": "cmos"}, "## Flying Through the Storm")
        self.assertEqual(cmos[0]["replacement"], "Flying through the Storm")
        self.assertEqual(cmos[0]["certainty"], "uncertain")
        self.assertEqual(hits("heading-case", {"case": "title", "style": "ap"}, "## Flying Through the Storm"), [])


class HeadingFormat(unittest.TestCase):
    def test_flags_when_on(self):
        self.assertEqual(quotes("heading-format", {"no_bold": True, "no_end_period": True}, "## **Getting** started."),
                         [("**Getting** started.", "Getting started")])

    def test_quiet_when_off(self):
        self.assertEqual(hits("heading-format", {"no_bold": False, "no_end_period": False}, "## **Getting** started."), [])


class SerialComma(unittest.TestCase):
    def test_required(self):
        found = hits("serial-comma", {"required": True}, "We tested kites, boats and bikes.")
        self.assertEqual([(f["quote"], f["replacement"]) for f in found], [("boats and", "boats, and")])
        self.assertEqual(found[0]["certainty"], "uncertain")
        self.assertEqual(hits("serial-comma", {"required": True}, "We tested kites, boats, and bikes."), [])

    def test_not_required(self):
        self.assertEqual(quotes("serial-comma", {"required": False}, "We tested kites, boats, and bikes."),
                         [("boats, and", "boats and")])
        self.assertEqual(hits("serial-comma", {"required": False}, "We tested kites, boats and bikes."), [])


class Terms(unittest.TestCase):
    def test_banned(self):
        found = hits("banned", {"terms": ["synergy"]}, "Real Synergy here.")
        self.assertEqual(found[0]["quote"], "Synergy")
        self.assertEqual(hits("banned", {"terms": ["synergy"], "case_sensitive": True}, "Real Synergy here."), [])
        self.assertEqual(hits("banned", {"terms": ["synergy"]}, 'She said "synergy" twice.'), [])

    def test_preferred(self):
        self.assertEqual(quotes("preferred", {"pairs": ["e-mail => email"]}, "E-mail us."), [("E-mail", "Email")])
        self.assertEqual(hits("preferred", {"pairs": ["e-mail => email"]}, "Email us."), [])
        self.assertEqual(quotes("preferred", {"pairs": ["email => e-mail"]}, "Email us."), [("Email", "E-mail")])

    def test_term_case(self):
        self.assertEqual(quotes("term-case", {"terms": ["KiteKit"]}, "Open Kitekit now."), [("Kitekit", "KiteKit")])
        self.assertEqual(hits("term-case", {"terms": ["KiteKit"]}, "Open KiteKit at https://kitekit.example/x."), [])
        self.assertEqual(quotes("term-case", {"terms": ["Kitekit"]}, "Open KiteKit now."), [("KiteKit", "Kitekit")])


class Numbers(unittest.TestCase):
    def test_numerals(self):
        found = hits("numerals", {"spell_out_below": 10}, "We built 3 kites.")
        self.assertEqual((found[0]["replacement"], found[0]["certainty"]), ("three", "certain"))
        self.assertEqual(hits("numerals", {"spell_out_below": 0}, "We built 3 kites."), [])

    def test_numeral_exclusions(self):
        text = ("It rose 5% in 3 px, at 9am, on May 4, in version 2, step 3, for $5.\n"
                "1. First step\n## 2. Setup")
        self.assertEqual(hits("numerals", {"spell_out_below": 10}, text), [])

    def test_numeral_en_dash_range(self):
        self.assertEqual(hits("numerals", {"spell_out_below": 10}, "Post 3%s5 times per week." % EN), [])
        self.assertEqual(hits("numerals", {"spell_out_below": 10}, "Post 3 %s 5 times per week." % EN), [])
        self.assertEqual(quotes("numerals", {"spell_out_below": 10}, "Post 3%s5 times, then 4 more posts." % EN),
                         [("4", "four")])

    def test_numeral_not_clearly_a_count(self):
        self.assertEqual(hits("numerals", {"spell_out_below": 10}, "The score was 3 at halftime.")[0]["certainty"],
                         "uncertain")

    def test_ordinals(self):
        self.assertEqual(quotes("ordinals", {"spell_out_below": 10}, "The 2nd kite."), [("2nd", "second")])
        self.assertEqual(hits("ordinals", {"spell_out_below": 2}, "The 2nd kite."), [])

    def test_sentence_start_numeral(self):
        self.assertEqual(quotes("sentence-start-numeral", {}, "Fine. 12 kites flew."), [("12", "Twelve")])
        self.assertEqual(hits("sentence-start-numeral", {}, "Twelve kites flew. We saw 12."), [])
        self.assertEqual(hits("sentence-start-numeral", {}, "2025 was windy.")[0]["certainty"], "uncertain")

    def test_percent(self):
        self.assertEqual(quotes("percent", {"style": "symbol"}, "up 40 percent"), [("40 percent", "40%")])
        self.assertEqual(hits("percent", {"style": "symbol"}, "up 40%"), [])
        self.assertEqual(quotes("percent", {"style": "word"}, "up 40%"), [("40%", "40 percent")])
        self.assertEqual(hits("percent", {"style": "word"}, "up 40 percent"), [])

    def test_money(self):
        self.assertEqual(quotes("money", {"style": "abbreviated"}, "raised $2.6 million"), [("$2.6 million", "$2.6M")])
        self.assertEqual(hits("money", {"style": "abbreviated"}, "raised $2.6M"), [])
        self.assertEqual(quotes("money", {"style": "words"}, "raised $2.6M"), [("$2.6M", "$2.6 million")])
        self.assertEqual(hits("money", {"style": "words"}, "raised $2.6 million"), [])
        self.assertEqual(hits("money", {"style": "abbreviated"}, "earned $150 thousand"), [])
        self.assertEqual(quotes("money", {"style": "abbreviated"}, "$3 billion and $1 trillion"),
                         [("$3 billion", "$3B"), ("$1 trillion", "$1T")])

    def test_thousands(self):
        self.assertEqual(quotes("thousands", {"style": "comma"}, "sold 4k kites"), [("4k", "4,000")])
        self.assertEqual(hits("thousands", {"style": "comma"}, "sold 4,000 kites"), [])
        self.assertEqual(quotes("thousands", {"style": "k"}, "sold 200,000 kites"), [("200,000", "200k")])
        self.assertEqual(hits("thousands", {"style": "k"}, "sold 200k kites"), [])

    def test_thousands_consistency(self):
        mixed = "We sold 200k kites, then 300k, then 400,000."
        self.assertEqual(quotes("thousands", {"style": "either", "consistent": True}, mixed),
                         [("400,000", "400k")])
        self.assertEqual(hits("thousands", {"style": "either", "consistent": False}, mixed), [])

    def test_date_format(self):
        self.assertEqual(quotes("date-format", {"ordinals": False}, "On September 24th we flew."),
                         [("September 24th", "September 24")])
        self.assertEqual(hits("date-format", {"ordinals": False}, "On September 24 we flew."), [])
        self.assertEqual(quotes("date-format", {"ordinals": True}, "On September 24 we flew."),
                         [("September 24", "September 24th")])
        self.assertEqual(hits("date-format", {"ordinals": True}, "On September 24th we flew."), [])

    def test_time_format(self):
        self.assertEqual(quotes("time-format", {"style": "9am"}, "Meet at 9 a.m. sharp."), [("9 a.m.", "9am")])
        self.assertEqual(hits("time-format", {"style": "9am"}, "Meet at 9am sharp."), [])
        self.assertEqual(quotes("time-format", {"style": "9 a.m."}, "Meet at 9am sharp."), [("9am", "9 a.m.")])
        self.assertEqual(hits("time-format", {"style": "9 a.m."}, "Meet at 9 a.m. sharp."), [])
        self.assertEqual(quotes("time-format", {"style": "9am"}, "Meet at 9 a.m. Then fly."), [("9 a.m.", "9am.")])

    def test_time_format_on_the_hour_and_noon(self):
        style = {"style": "9 a.m."}
        self.assertEqual(hits("time-format", style, "Meet at 9:00 a.m. sharp."), [])
        self.assertEqual(quotes("time-format", style, "Meet at 9:00am or 12pm today."),
                         [("9:00am", "9:00 a.m."), ("12pm", "12 p.m.")])
        both = dict(style, drop_zero_minutes=True, noon_midnight=True)
        self.assertEqual(quotes("time-format", both, "Meet at 9:00 a.m. sharp, 9:30am, or 12 p.m. today."),
                         [("9:00 a.m.", "9 a.m."), ("9:30am", "9:30 a.m."), ("12 p.m.", "noon")])
        self.assertEqual(quotes("time-format", both, "Fly till 12:00am. 12 p.m. is lunch."),
                         [("12:00am", "midnight"), ("12 p.m.", "Noon")])
        self.assertEqual(quotes("time-format", dict(style, noon_midnight=True), "Lunch at 12:30pm today."),
                         [("12:30pm", "12:30 p.m.")])
        self.assertEqual(hits("time-format", both, "Meet at 9 a.m., noon, or midnight."), [])


class QuoteStyle(unittest.TestCase):
    def test_curly_flags_straight(self):
        self.assertEqual(quotes("quote-style", {"marks": "curly"}, 'She said "go" and we don\'t stop.'),
                         [('"go"', "“go”"), ("don't", "don’t")])

    def test_straight_flags_curly(self):
        self.assertEqual(quotes("quote-style", {"marks": "straight"}, "She said “go” and don’t."),
                         [("“go”", '"go"'), ("don’t.", "don't.")])

    def test_each_accepts_its_own(self):
        self.assertEqual(hits("quote-style", {"marks": "curly"}, "She said “go.”"), [])
        self.assertEqual(hits("quote-style", {"marks": "straight"}, 'She said "go."'), [])

    def test_punctuation_side(self):
        self.assertEqual(quotes("quote-style", {"marks": "curly"}, "It was “the plan”."),
                         [("plan”.", "plan.”")])
        self.assertEqual(hits("quote-style", {"marks": "curly", "punctuation_inside": False}, "It was “the plan”."), [])
        found = hits("quote-style", {"marks": "curly", "punctuation_inside": False}, "It was “the plan.”")
        self.assertEqual(found[0]["replacement"], "plan”.")

    def test_code_skipped(self):
        self.assertEqual(hits("quote-style", {"marks": "curly"}, 'Run `echo "hi"` now.'), [])


class BoldLabel(unittest.TestCase):
    def test_colon(self):
        self.assertEqual(quotes("bold-label", {"separator": "colon"}, "- **Setup.** install"),
                         [("**Setup.**", "**Setup:**")])
        self.assertEqual(hits("bold-label", {"separator": "colon"}, "- **Setup:** install"), [])

    def test_period(self):
        self.assertEqual(quotes("bold-label", {"separator": "period"}, "- **Setup**: install"),
                         [("**Setup**:", "**Setup**.")])
        self.assertEqual(hits("bold-label", {"separator": "period"}, "- **Setup.** install"), [])

    def test_dash(self):
        found = hits("bold-label", {"separator": "dash"}, "- **Setup:** install")
        self.assertIsNone(found[0]["replacement"])
        self.assertEqual(hits("bold-label", {"separator": "dash"}, "- **Setup** - install"), [])


class LinkHygiene(unittest.TestCase):
    def test_tracking(self):
        text = "See [the manual](https://ex.com/a?utm_source=x&id=2&fbclid=9)."
        self.assertEqual(quotes("link-hygiene", {"tracking": True}, text),
                         [("https://ex.com/a?utm_source=x&id=2&fbclid=9", "https://ex.com/a?id=2")])
        self.assertEqual(hits("link-hygiene", {"tracking": False}, text), [])

    def test_https(self):
        found = hits("link-hygiene", {"https": True}, "See [it](http://ex.com/a).")
        self.assertEqual((found[0]["replacement"], found[0]["certainty"]), ("https://ex.com/a", "uncertain"))
        self.assertEqual(hits("link-hygiene", {"https": False}, "See [it](http://ex.com/a)."), [])

    def test_anchor_length(self):
        text = "See [one two three four five](https://ex.com)."
        self.assertEqual(hits("link-hygiene", {"max_anchor_words": 4}, text)[0]["quote"],
                         "one two three four five")
        self.assertEqual(hits("link-hygiene", {"max_anchor_words": 5}, text), [])


class Regex(unittest.TestCase):
    def test_regex(self):
        params = {"pattern": r"\bclick here\b", "message": "Name the target.", "flags": "i"}
        found = hits("regex", params, "Click here to go.")
        self.assertEqual((found[0]["quote"], found[0]["comment"]), ("Click here", "Name the target."))
        self.assertEqual(hits("regex", dict(params, flags=""), "Click here to go."), [])

    def test_replacement_template(self):
        params = {"pattern": r"(\d+) users", "message": "Say people.", "replacement": r"\1 people"}
        self.assertEqual(quotes("regex", params, "We met 5 users."), [("5 users", "5 people")])

    def test_certainty(self):
        params = {"pattern": r"\bclick here\b", "message": "Name the target.", "flags": "i"}
        self.assertEqual(hits("regex", params, "Click here to go.")[0]["certainty"], "certain")
        self.assertEqual(hits("regex", dict(params, certainty="uncertain"), "Click here to go.")[0]["certainty"],
                         "uncertain")


class Params(unittest.TestCase):
    def test_invalid_and_missing(self):
        from sgclib.lint import normalize_params
        self.assertTrue(normalize_params("dash-spacing", {})[1])
        self.assertTrue(normalize_params("dash-spacing", {"style": "wide"})[1])
        self.assertTrue(normalize_params("dash-spacing", {"style": "closed", "color": "red"})[1])
        self.assertTrue(normalize_params("nope", {})[1])
        self.assertTrue(normalize_params("regex", {"pattern": "(", "message": "x"})[1])
        self.assertTrue(normalize_params("regex", {"pattern": "x", "message": "x", "certainty": "maybe"})[1])
        params, errors = normalize_params("time-format", {"style": "9am"})
        self.assertEqual((errors, params["drop_zero_minutes"], params["noon_midnight"]), ([], False, False))
        params, errors = normalize_params("heading-case", {"case": "title"})
        self.assertEqual((errors, params["levels"], params["style"]), ([], [2, 3, 4], "cmos"))


if __name__ == "__main__":
    unittest.main()


class ProofPairs(unittest.TestCase):
    def run_pairs(self, text):
        from sgclib.article import Article
        from sgclib.pairs import check_pairs
        return [(f["line"], f["quote"], f["note"]) for f in check_pairs(Article(text))]

    def test_unclosed_parenthesis(self):
        found = self.run_pairs("# T\n\nIf you grasp too tight (i.e. chasing the algos, the bird dies.\n")
        self.assertEqual(found, [(3, "(i.e. chasing the algos, the", "unclosed parenthesis")])

    def test_balanced_text_and_exceptions(self):
        text = ("# T\n\nA (fine) aside, a [note], and **bold** text.\n\n"
                "- 1) first and a) second :)\n"
                "- Read [the guide](https://example.com/a_(b)) and `f(x` in code.\n\n"
                "A paren that opens here (and\ncloses on the next line).\n\n"
                "```\nunclosed ( in code\n```\n")
        self.assertEqual(self.run_pairs(text), [])

    def test_stray_closer_and_bold(self):
        found = self.run_pairs("# T\n\nThis ends early) and **this never closes.\n")
        self.assertEqual([f[2] for f in found], ["unopened parenthesis", "unpaired bold marker"])
        self.assertEqual(found[0][1], "This ends early)")

    def test_pair_finding_flows_through_lint(self):
        from sgclib.article import Article
        from sgclib.lint import run_lint
        found = run_lint([], Article("# T\n\nSee (this.\n"))
        self.assertEqual([(f["rule_id"], f["id"], f["certainty"]) for f in found], [("PROOF-PAIR", "L0001", "certain")])

    def test_list_item_wrapped_across_lines(self):
        text = ("# T\n\n- **Item.** Chase [too many\n  ideas](https://example.com/x),\n  and nothing (gets\n  done).\n"
                "- Next item opens (here\n")
        self.assertEqual([(f[0], f[2]) for f in self.run_pairs(text)], [(7, "unclosed parenthesis")])
