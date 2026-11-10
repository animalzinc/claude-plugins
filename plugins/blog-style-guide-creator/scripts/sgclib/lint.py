"""Lint checks. Each check reads every preference from its rule block's
parameters; the code holds no brand's style.

A check function takes a Ctx and calls ctx.add() for each finding. Findings
follow schema/finding.schema.json, with `pass: lint`, a 0-based `col`, a
`certainty`, and a `note` that explains the finding in plain words.
"""
import re
import urllib.parse

from .article import ALL_KINDS, MASK, SENTENCE_BOUNDARY_RE
from . import pairs
from .common import number_words, ordinal_words

EM = "—"
EN = "–"

# ------------------------------------------------------------ parameters


class ParamError(Exception):
    pass


def _enum(*values):
    def check(v):
        if v not in values:
            raise ParamError("must be one of %s, found %r" % (", ".join(map(str, values)), v))
        return v
    return check


def _bool(v):
    if not isinstance(v, bool):
        raise ParamError("must be true or false, found %r" % (v,))
    return v


def _int(v):
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        raise ParamError("must be a whole number of 0 or more, found %r" % (v,))
    return v


def _optional_int(v):
    if v is None:
        return None
    return _int(v)


def _str(v):
    if not isinstance(v, str) or not v.strip():
        raise ParamError("must be a non-empty string, found %r" % (v,))
    return v


def _str_list(v):
    if isinstance(v, str):
        v = [v]
    if not isinstance(v, list) or not v or not all(isinstance(x, str) and x.strip() for x in v):
        raise ParamError("must be a list of non-empty strings, found %r" % (v,))
    return v


def _levels(v):
    if isinstance(v, int) and not isinstance(v, bool):
        v = [v]
    if not isinstance(v, list) or not v or not all(
            isinstance(x, int) and not isinstance(x, bool) and 1 <= x <= 6 for x in v):
        raise ParamError("must be a list of heading levels from 1 to 6, found %r" % (v,))
    return v


def _pairs(v):
    v = _str_list(v)
    out = []
    for item in v:
        if "=>" not in item:
            raise ParamError('each pair must read "wrong => right", found %r' % item)
        wrong, right = [x.strip() for x in item.split("=>", 1)]
        if not wrong:
            raise ParamError("a pair has nothing before =>: %r" % item)
        out.append((wrong, right))
    return out


def _flags(v):
    if v is None or v == "":
        return ""
    if not isinstance(v, str) or not re.match(r"^[imsx]*$", v):
        raise ParamError("must be a string of regex flag letters from i, m, s, x, found %r" % (v,))
    return v


REQUIRED = object()


# ------------------------------------------------------------ context


class Ctx(object):
    def __init__(self, rule, params, article, extra):
        self.rule = rule
        self.p = params
        self.art = article
        self.extra = extra
        self.out = []

    def add(self, n, start, end, replacement, certainty="certain", note=None, comment=None):
        line = self.art.line(n)
        quote = line[start:end]
        if not quote:
            return
        if replacement is not None and replacement == quote:
            return
        self.out.append({
            "rule_id": self.rule["id"],
            "pass": "lint",
            "line": n,
            "col": start,
            "quote": quote,
            "replacement": replacement,
            "comment": comment if replacement is None else None,
            "basis": "explicit",
            "certainty": certainty,
            "note": note,
            "check": self.rule.get("check"),
        })

    def lines(self, kinds=ALL_KINDS, headings=True, tables=True):
        """(line number, masked text) for every line of text the check reads."""
        art = self.art
        for n in art.numbers():
            if n <= art.fm_lines or n in art.fence_lines:
                continue
            if not headings and n in art.headings:
                continue
            if not tables and n in art.table_lines:
                continue
            masked = art.masked(n, kinds)
            if masked.strip(MASK + " \t"):
                yield n, masked


def _word_bounds(text, start, end):
    """Widen [start, end) to the neighboring non-space runs, stopping at masks."""
    s = start
    while s > 0 and not text[s - 1].isspace() and text[s - 1] != MASK:
        s -= 1
    e = end
    while e < len(text) and not text[e].isspace() and text[e] != MASK:
        e += 1
    return s, e


def _term_regex(term, case_sensitive):
    pattern = re.escape(term)
    if re.match(r"\w", term):
        pattern = r"(?<!\w)" + pattern
    if re.search(r"\w$", term):
        pattern = pattern + r"(?!\w)"
    return re.compile(pattern, 0 if case_sensitive else re.IGNORECASE)


def _capitalize(s):
    return s[:1].upper() + s[1:] if s else s


def _at_sentence_start(masked, col, list_col=0):
    before = masked[list_col:col]
    stripped = re.sub(r"[*_\"“(\[]+$", "", before)
    return stripped.strip() == "" or bool(re.search(r"[.!?][\"'”’)\]*_]*\s+$", stripped))


# ------------------------------------------------------------ dash-spacing


SIGN_OFF_RE = re.compile(r"^[ \t]*(?:>[ \t]*)*[*_]*[ \t]*" + EM + r"[ \t]*[*_]*[ \t]*"
                         r"[A-ZÀ-ÖØ-Þ][\w.'’\-]*(?:[ \t]+[A-ZÀ-ÖØ-Þ][\w.'’\-]*){0,3}"
                         r"[ \t]*[*_]*[ \t]*$")


def check_dash_spacing(ctx):
    style, ranges = ctx.p["style"], ctx.p.get("ranges")

    def dash_for_style(left_word, right_word):
        if style == "closed":
            return left_word + EM + right_word
        if style == "spaced":
            return left_word + " " + EM + " " + right_word
        return None

    for n, m in ctx.lines():
        sign_off = style == "none" and SIGN_OFF_RE.match(ctx.art.line(n))
        for i, ch in enumerate(m):
            if ch != EM or sign_off:
                continue
            ls = i
            while ls > 0 and m[ls - 1] in " \t":
                ls -= 1
            re_ = i + 1
            while re_ < len(m) and m[re_] in " \t":
                re_ += 1
            left_space, right_space = i - ls, re_ - (i + 1)
            at_edge = ls == 0 or re_ >= len(m) or m[ls - 1] == MASK or m[re_] == MASK
            s, _ = _word_bounds(m, ls, ls)
            _, e = _word_bounds(m, re_, re_)
            left_word, right_word = m[s:ls], m[re_:e]
            if style == "none":
                ctx.add(n, s, e, None, note="em dash in a guide that uses none",
                        comment="Rewrite without the em dash.")
            elif at_edge:
                continue
            elif style == "closed" and (left_space or right_space):
                ctx.add(n, s, e, dash_for_style(left_word, right_word),
                        note="spaced em dash; the guide closes em dashes")
            elif style == "spaced" and (not left_space or not right_space):
                ctx.add(n, s, e, dash_for_style(left_word, right_word),
                        note="closed em dash; the guide spaces em dashes")
        for mt in re.finditer(r"(?<=\S)([ \t]+)(--|-|–)([ \t]+)(?=\S)", m):
            start_dash, end_dash = mt.start(1), mt.end(3)
            before = m[start_dash - 1]
            after = m[end_dash] if end_dash < len(m) else ""
            if mt.group(2) == EN and before.isdigit() and after.isdigit():
                continue  # a spaced range, handled below
            if MASK in (before, after):
                continue
            s, _ = _word_bounds(m, start_dash, start_dash)
            _, e = _word_bounds(m, end_dash, end_dash)
            repl = dash_for_style(m[s:start_dash], m[end_dash:e])
            ctx.add(n, s, e, repl, note="%s used as an em dash"
                    % ("spaced en dash" if mt.group(2) == EN else "spaced hyphen"),
                    comment=None if repl else "Rewrite without a dash.")
        if ranges == "en-dash":
            for mt in re.finditer(r"(?<![\w\-/.:,])(\d+)-(\d+)(?![\w\-/:]|[.,]\d)", m):
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + EN + mt.group(2), "uncertain",
                        note="a number range with a hyphen; the guide uses an en dash "
                             "(could be a code, score, or identifier)")
        elif ranges == "hyphen":
            for mt in re.finditer(r"(\d+)[ \t]*–[ \t]*(\d+)", m):
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + "-" + mt.group(2),
                        note="a number range with an en dash; the guide uses a hyphen")


# ------------------------------------------------------------ heading-case

ARTICLES_CONJ = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "as", "vs"}
AP_SMALL = ARTICLES_CONJ | {"at", "by", "in", "of", "off", "on", "out", "per", "to", "up", "via"}
PREPOSITIONS = {
    "at", "by", "in", "of", "off", "on", "out", "per", "to", "up", "via", "about", "above",
    "across", "after", "against", "along", "amid", "among", "around", "before", "behind",
    "below", "beneath", "beside", "besides", "between", "beyond", "despite", "down", "during",
    "except", "from", "inside", "into", "like", "near", "onto", "outside", "over", "past",
    "since", "through", "throughout", "toward", "towards", "under", "underneath", "until",
    "upon", "with", "within", "without"}
CMOS_SMALL = {"a", "an", "the", "and", "but", "or", "nor", "for", "as", "to", "vs"} | PREPOSITIONS
ALL_SMALL = AP_SMALL | CMOS_SMALL
# Always capitalized in English; "may" stays out because the verb is common in headings.
ALWAYS_PROPER = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
                 "january", "february", "march", "april", "june", "july", "august",
                 "september", "october", "november", "december"}
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’]*")


def _case_tokens(masked):
    """(start, end, word, edge) for each word of a heading; `edge` is true for
    the first and last word and for a word after a colon or sentence end."""
    toks = [(m.start(), m.end(), m.group(0)) for m in TOKEN_RE.finditer(masked)]
    out = []
    for i, (s, e, w) in enumerate(toks):
        prev_text = masked[toks[i - 1][1]:s] if i else ""
        after_break = bool(re.search(r"[:?!.]|" + EM, prev_text))
        out.append((s, e, w, i == 0, i == len(toks) - 1, after_break))
    return out


def _skip_token(word):
    if re.search(r"\d", word):
        return True
    if len(word) > 1 and word.isupper():
        return True
    if re.search(r"[A-Z]", word[1:]):
        return True
    return False


def check_heading_case(ctx):
    case, levels, style = ctx.p["case"], ctx.p["levels"], ctx.p["style"]
    small = CMOS_SMALL if style == "cmos" else AP_SMALL
    lower_words = ctx.extra.get("lower_words", set())
    known_terms = {t.lower() for t in ctx.extra.get("known_terms", set())}
    for n, (level, text, col) in sorted(ctx.art.headings.items()):
        if level not in levels:
            continue
        masked = ctx.art.masked(n)[col:col + len(text)]
        masked = re.sub(r"\]\(" + MASK + r"*\)", lambda m: MASK * len(m.group(0)), masked)
        chars = list(text)
        changed, uncertain = [], False
        for s, e, w, first, last, after_break in _case_tokens(masked):
            if _skip_token(w):
                continue
            lw = w.lower()
            if case == "title":
                if w == "I":
                    continue
                want_cap = first or last or after_break or lw not in small
                if want_cap and w[0].islower():
                    chars[s] = w[0].upper()
                    changed.append(w)
                elif not want_cap and w[0].isupper():
                    chars[s] = w[0].lower()
                    changed.append(w)
                    if style == "cmos" and lw in PREPOSITIONS and len(lw) >= 5:
                        uncertain = True
            else:
                if first:
                    if w[0].islower():
                        chars[s] = w[0].upper()
                        changed.append(w)
                    continue
                if after_break or w == "I" or not w[0].isupper():
                    continue
                if lw in known_terms or lw in ALWAYS_PROPER:
                    continue
                chars[s] = w[0].lower()
                changed.append(w)
                if lw not in ALL_SMALL and lw not in lower_words:
                    uncertain = True
        if changed:
            ctx.add(n, col, col + len(text), "".join(chars), "uncertain" if uncertain else "certain",
                    note="heading not in %s case (%s)%s" % (
                        case, ", ".join(changed),
                        "; a capitalized word may be a proper noun or a long preposition"
                        if uncertain else ""))


# ------------------------------------------------------------ heading-format


def check_heading_format(ctx):
    for n, (level, text, col) in sorted(ctx.art.headings.items()):
        new, notes = text, []
        if ctx.p["no_bold"] and re.search(r"\*\*|__", ctx.art.masked(n)[col:]):
            new = re.sub(r"(\*\*|__)(.+?)\1", r"\2", new).replace("**", "")
            notes.append("bold inside a heading")
        if ctx.p["no_end_period"] and re.search(r"(?<!\.)\.$", new.rstrip("*_")):
            stripped = new.rstrip("*_")
            new = stripped[:-1] + new[len(stripped):]
            notes.append("heading ends in a period")
        if notes:
            ctx.add(n, col, col + len(text), new, note="; ".join(notes))


# ------------------------------------------------------------ serial-comma

_W = r"[A-Za-z0-9][\w'’\-]*"


def check_serial_comma(ctx):
    if ctx.p["required"]:
        pattern = re.compile(r"(?:%s, )((?:%s ){0,3}%s) (and|or) (?=\w)" % (_W, _W, _W))
    else:
        pattern = re.compile(r"(?:%s, )((?:%s ){0,3}%s), (and|or) (?=\w)" % (_W, _W, _W))
    for n, m in ctx.lines(headings=False):
        for mt in pattern.finditer(m):
            start, end = mt.start(1), mt.end(2)
            if ctx.p["required"]:
                repl = mt.group(1) + ", " + mt.group(2)
                note = "list of three or more without a serial comma"
            else:
                repl = mt.group(1) + " " + mt.group(2)
                note = "serial comma in a guide that leaves it out"
            ctx.add(n, start, end, repl, "uncertain", note=note + " (could be two clauses, not a list)")


# ------------------------------------------------------------ banned, preferred, term-case


def check_banned(ctx):
    regs = [(t, _term_regex(t, ctx.p["case_sensitive"])) for t in ctx.p["terms"]]
    for n, m in ctx.lines():
        for term, rx in regs:
            for mt in rx.finditer(m):
                ctx.add(n, mt.start(), mt.end(), None, note="banned term %r" % term,
                        comment="Banned term: %s." % term)


def check_preferred(ctx):
    regs = [(w, r, _term_regex(w, False)) for w, r in ctx.p["pairs"]]
    for n, m in ctx.lines():
        for wrong, right, rx in regs:
            for mt in rx.finditer(m):
                found = mt.group(0)
                if found == right:
                    continue
                repl = right
                if found[:1].isupper() and right[:1].islower() and not found.isupper():
                    repl = _capitalize(right)
                ctx.add(n, mt.start(), mt.end(), repl, note="%r is preferred over %r" % (right, wrong))


def check_term_case(ctx):
    terms = ctx.p["terms"]
    exact = set(terms)
    for n, m in ctx.lines():
        for term in terms:
            pattern = r"(?<![\w@#/.])" + re.escape(term) + r"(?![\w]|\.\w)"
            for mt in re.finditer(pattern, m, re.IGNORECASE):
                found = mt.group(0)
                if found in exact:
                    continue
                certainty = "certain"
                if found.islower() and " " not in term and term[:1].isupper() and term[1:].islower():
                    certainty = "uncertain"
                ctx.add(n, mt.start(), mt.end(), term, certainty,
                        note="%r is written %r in the guide%s" % (
                            found, term, "; the lowercase form may be the common word"
                            if certainty == "uncertain" else ""))


# ------------------------------------------------------------ numbers

MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|October|November|"
          r"December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)")
UNITS = (r"(?:px|pt|em|rem|ms|kb|mb|gb|tb|kg|mg|g|lb|lbs|oz|km|cm|mm|m|mi|ft|inches|inch|"
         r"mph|kph|kmh|hz|khz|mhz|ghz|k|bn|degrees?|°)")
LABELS = (r"(?:figure|fig\.|table|chapter|section|page|p\.|step|phase|level|tier|part|item|"
          r"no\.|number|episode|season|rule|appendix|grade|stage|week|day|round|issue|vol\.|"
          r"volume|version|v\.?|line|row|column|slide|question|q)")
NOT_PLURAL = {"is", "was", "has", "does", "as", "us", "its", "this", "his", "plus", "versus",
              "less", "yes", "thus", "previous", "various", "bonus", "focus", "status"}


def check_numerals(ctx):
    limit = ctx.p["spell_out_below"]
    rx = re.compile(r"(?<![\w.,$€£¥%:/\-#+])(\d+)(?![\w%]|[.,:/]\d|\s*%|-\d|–\d)")
    for n, m in ctx.lines(tables=False):
        list_col = ctx.art.strip_list_marker(n)
        heading = ctx.art.headings.get(n)
        for mt in rx.finditer(m):
            raw = mt.group(1)
            if raw.startswith("0") and len(raw) > 1:
                continue
            value = int(raw)
            if value >= limit:
                continue
            before, after = m[:mt.start()], m[mt.end():]
            if list_col and mt.start() < list_col:
                continue
            if re.search(r"\d[ \t]*" + EN + r"[ \t]*$", before) or re.match(r"^[ \t]*" + EN + r"[ \t]*\d", after):
                continue  # one end of an en-dash range
            if heading and not before[heading[2]:].strip(" *_"):
                if re.match(r"^[.):]", after):
                    continue
            if re.match(r"^\s*(?:percent|per cent|percentage points?)\b", after, re.IGNORECASE):
                continue
            if re.match(r"^\s?" + UNITS + r"\b", after, re.IGNORECASE):
                continue
            if re.match(r"^\s*(?:a\.m\.|p\.m\.|am\b|pm\b|o'clock)", after, re.IGNORECASE):
                continue
            if re.search(r"\b" + LABELS + r"\s*$", before, re.IGNORECASE):
                continue
            if re.search(MONTHS + r"\.?\s+$", before) or re.match(r"^\s+(?:of\s+)?" + MONTHS + r"\b", after):
                continue
            nxt = re.match(r"^\s+([a-z][a-z\-]*)(?:\s+([a-z][a-z\-]*))?", after)
            certainty = "uncertain"
            if nxt and any(w and w.endswith("s") and len(w) > 2 and w not in NOT_PLURAL
                           for w in nxt.groups()):
                certainty = "certain"
            words = number_words(value)
            if words and _at_sentence_start(m, mt.start(), list_col):
                words = _capitalize(words)
            ctx.add(n, mt.start(), mt.end(), words, certainty,
                    note="numeral under %d in prose%s" % (
                        limit, "" if certainty == "certain" else "; may not be a count"))


def check_ordinals(ctx):
    limit = ctx.p["spell_out_below"]
    for n, m in ctx.lines(tables=False):
        for mt in re.finditer(r"(?<![\w.])(\d+)(st|nd|rd|th)\b", m):
            value = int(mt.group(1))
            if value >= limit:
                continue
            before, after = m[:mt.start()], m[mt.end():]
            if re.search(MONTHS + r"\.?\s+$", before) or re.match(r"^\s+(?:of\s+)?" + MONTHS + r"\b", after):
                continue
            words = ordinal_words(value)
            if _at_sentence_start(m, mt.start(), ctx.art.strip_list_marker(n)):
                words = _capitalize(words)
            ctx.add(n, mt.start(), mt.end(), words, note="ordinal under %d as a numeral" % limit)


def check_sentence_start_numeral(ctx):
    for n, m in ctx.lines(headings=False, tables=False):
        list_col = ctx.art.strip_list_marker(n)
        starts = [0] + [mt.end() for mt in SENTENCE_BOUNDARY_RE.finditer(m)]
        for pos in starts:
            if list_col and pos <= list_col:
                continue
            lead = re.match(r"[*_\"“(\[]*", m[pos:])
            p = pos + lead.end()
            mt = re.match(r"\d[\d,.]*(%?)", m[p:])
            if not mt:
                continue
            token = mt.group(0).rstrip(".,")
            end = p + len(token)
            certainty = "certain"
            if re.match(r"^(1\d|20|21)\d\d$", token):
                certainty = "uncertain"
            repl = None
            if token.isdigit() and int(token) < 100 and not mt.group(1):
                repl = _capitalize(number_words(int(token)))
            ctx.add(n, p, end, repl, certainty,
                    note="sentence starts with a numeral%s" % (
                        "; a year opening a sentence is accepted by some guides"
                        if certainty == "uncertain" else ""),
                    comment="Rewrite so the sentence does not open with a numeral.")


def check_percent(ctx):
    for n, m in ctx.lines():
        if ctx.p["style"] == "symbol":
            for mt in re.finditer(r"(?<![\w.])(\d[\d.,]*)\s?(?:percent|per cent)\b", m, re.IGNORECASE):
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + "%", note="percent as a word")
        else:
            for mt in re.finditer(r"(?<![\w.])(\d[\d.,]*)\s?%", m):
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + " percent", note="percent as a symbol")


_SCALE_WORDS = {"million": "M", "billion": "B", "trillion": "T"}
_SCALE_ABBR = {"k": "thousand", "m": "million", "mn": "million", "b": "billion",
               "bn": "billion", "t": "trillion"}


def check_money(ctx):
    for n, m in ctx.lines():
        if ctx.p["style"] == "abbreviated":
            for mt in re.finditer(r"([$€£¥]\s?\d[\d.,]*)\s+(million|billion|trillion)\b",
                                  m, re.IGNORECASE):
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + _SCALE_WORDS[mt.group(2).lower()],
                        note="money amount with the scale as a word")
        else:
            for mt in re.finditer(r"([$€£¥]\s?\d[\d.,]*)(bn|mn|[KMBTkmbt])\b", m):
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + " " + _SCALE_ABBR[mt.group(2).lower()],
                        note="money amount with an abbreviated scale")


def _fmt_thousands(value):
    if value != int(value):
        return None
    return "{:,}".format(int(value))


def _k_form(value):
    if value % 100:
        return None
    k = value / 1000.0
    return ("%d" % k if k == int(k) else ("%.1f" % k).rstrip("0").rstrip(".")) + "k"


K_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s?([kK])\b")
COMMA_RE = re.compile(r"(?<![\w.,])(\d{1,3}(?:,\d{3})+)(?![\d,]|\.\d)")
PLAIN_RE = re.compile(r"(?<![\w.,$€£¥])(\d{5,})(?![\w]|[.,]\d)")


def check_thousands(ctx):
    style, consistent = ctx.p["style"], ctx.p["consistent"]
    k_hits, comma_hits = [], []
    for n, m in ctx.lines(tables=True):
        for mt in K_RE.finditer(m):
            k_hits.append((n, mt))
        for mt in COMMA_RE.finditer(m):
            comma_hits.append((n, mt))
        if style == "comma":
            for mt in PLAIN_RE.finditer(m):
                ctx.add(n, mt.start(), mt.end(), _fmt_thousands(int(mt.group(1))), "uncertain",
                        note="large number without thousands separators (could be an ID or code)")

    def k_to_comma(n, mt, note):
        value = float(mt.group(1)) * 1000
        ctx.add(n, mt.start(), mt.end(), _fmt_thousands(value), note=note,
                comment="Write the number in full with commas.")

    def comma_to_k(n, mt, note):
        value = int(mt.group(1).replace(",", ""))
        repl = _k_form(value)
        if repl:
            ctx.add(n, mt.start(), mt.end(), repl, note=note)

    if style == "comma":
        for n, mt in k_hits:
            k_to_comma(n, mt, "thousands written with k; the guide writes them with commas")
    elif style == "k":
        for n, mt in comma_hits:
            comma_to_k(n, mt, "thousands written with commas; the guide writes them with k")
    elif consistent and k_hits and comma_hits:
        first_k = (k_hits[0][0], k_hits[0][1].start())
        first_c = (comma_hits[0][0], comma_hits[0][1].start())
        if len(k_hits) < len(comma_hits) or (len(k_hits) == len(comma_hits) and first_c < first_k):
            for n, mt in k_hits:
                k_to_comma(n, mt, "the piece mixes k and comma forms; most use commas")
        else:
            for n, mt in comma_hits:
                comma_to_k(n, mt, "the piece mixes k and comma forms; most use k")


def check_date_format(ctx):
    for n, m in ctx.lines():
        if not ctx.p["ordinals"]:
            for mt in re.finditer(r"\b(" + MONTHS + r"\.?\s+)(\d{1,2})(st|nd|rd|th)\b", m):
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + mt.group(2),
                        note="date with an ordinal suffix")
            for mt in re.finditer(r"(?<![\w.])(\d{1,2})(?:st|nd|rd|th)\s+(?:of\s+)?(" + MONTHS + r")\b", m):
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + " " + mt.group(2),
                        note="date with an ordinal suffix")
        else:
            for mt in re.finditer(r"\b(" + MONTHS + r"\.?\s+)(\d{1,2})(?![\d\w]|,?\s*\d{4})", m):
                day = int(mt.group(2))
                if not 1 <= day <= 31:
                    continue
                suffix = "th" if 10 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
                ctx.add(n, mt.start(), mt.end(), mt.group(0) + suffix, "uncertain",
                        note="date without the ordinal suffix the guide uses")


TIME_RE = re.compile(r"(?<![\w:.])(\d{1,2})(:\d{2})?(\s?)(a\.m\.|p\.m\.|am|pm|AM|PM|A\.M\.|P\.M\.)(?!\w)")


def check_time_format(ctx):
    style, drop_zero, noon = ctx.p["style"], ctx.p["drop_zero_minutes"], ctx.p["noon_midnight"]
    for n, m in ctx.lines():
        for mt in TIME_RE.finditer(m):
            hour = int(mt.group(1))
            if not 1 <= hour <= 12:
                continue
            ap = "am" if mt.group(4).lower().startswith("a") else "pm"
            mins = mt.group(2) or ""
            if drop_zero and mins == ":00":
                mins = ""
            note = "time not written as %s" % style
            if noon and hour == 12 and mins in ("", ":00"):
                want = "noon" if ap == "pm" else "midnight"
                if _at_sentence_start(m, mt.start(), ctx.art.strip_list_marker(n)):
                    want = _capitalize(want)
                note = "12 o'clock as a time; the guide writes noon and midnight"
            elif style == "9am":
                want = "%d%s%s" % (hour, mins, ap)
            elif style == "9 am":
                want = "%d%s %s" % (hour, mins, ap)
            else:
                want = "%d%s %s.m." % (hour, mins, ap[0])
            start, end = mt.start(), mt.end()
            if mt.group(0) == want:
                continue
            rest = m[end:]
            if mt.group(0).endswith(".") and not want.endswith(".") and (
                    not rest.strip() or re.match(r"^\s+[A-Z]", rest)):
                want += "."
            if want.endswith(".") and rest.startswith("."):
                end += 1
            ctx.add(n, start, end, want, note=note)


# ------------------------------------------------------------ quote-style

CURLY = {"“": '"', "”": '"', "‘": "'", "’": "'"}


def _curl_apostrophes(text):
    out = re.sub(r"(?<=\w)'(?=\w)", "’", text)
    out = re.sub(r"(?<=\w)'(?=\s|$|[.,;:!?)])", "’", out)
    out = re.sub(r"(?:(?<=^)|(?<=[\s(\[]))'(?=\w)", "‘", out)
    return out


def _fold_punct(open_q, inner, close_q, after, inside):
    """Text for a converted quote, with a trailing comma or period moved to the
    guide's side of the closing mark. `after` is the punctuation after the quote."""
    if inside and after:
        return open_q + inner + after + close_q, True
    if not inside and inner[-1:] in (".", ",") and not after:
        return open_q + inner[:-1] + close_q + inner[-1], True
    return open_q + inner + close_q + after, False


def check_quote_style(ctx):
    marks, inside = ctx.p["marks"], ctx.p["punctuation_inside"]
    lq, rq, lsq, rsq = "\u201c", "\u201d", "\u2018", "\u2019"
    for n, m in ctx.lines(kinds=("frontmatter", "code", "url")):
        taken = []
        if marks == "curly":
            pattern = r'(?<!\d)"([^"\n]*)"([.,]?)'
        else:
            pattern = lq + "([^" + rq + "\\n]*)" + rq + "([.,]?)"
        for mt in re.finditer(pattern, m):
            if MASK in mt.group(0):
                continue
            taken.append((mt.start(), mt.end()))
            inner = mt.group(1)
            if marks == "curly":
                inner = _curl_apostrophes(inner)
                repl, moved = _fold_punct(lq, inner, rq, mt.group(2), inside)
            else:
                for k, v in CURLY.items():
                    inner = inner.replace(k, v)
                repl, moved = _fold_punct('"', inner, '"', mt.group(2), inside)
            ctx.add(n, mt.start(), mt.end(), repl,
                    "uncertain" if moved and not inside else "certain",
                    note="%s double quotes; the guide uses %s quotes%s" % (
                        "straight" if marks == "curly" else "curly", marks,
                        "; punctuation moved %s the closing mark" % ("inside" if inside else "outside")
                        if moved else ""))
        if marks == "curly":
            for mt in re.finditer(r'(?<!\d)"', m):
                if any(a <= mt.start() < b for a, b in taken):
                    continue
                s_, e_ = _word_bounds(m, mt.start(), mt.end())
                ctx.add(n, s_, e_, None, "uncertain", note="unpaired straight double quote",
                        comment="Use a curly quotation mark.")
            for mt in re.finditer(r"\S*'\S*", m):
                if any(a <= mt.start() < b for a, b in taken) or MASK in mt.group(0):
                    continue
                if re.search(r"\d'", mt.group(0)):
                    continue
                token = mt.group(0)
                new = _curl_apostrophes(token)
                if new != token:
                    ctx.add(n, mt.start(), mt.end(), new, "uncertain" if lsq in new else "certain",
                            note="straight apostrophe or single quote; the guide uses curly quotes")
        else:
            for mt in re.finditer("\\S*[" + lq + rq + lsq + rsq + "]\\S*", m):
                if any(a <= mt.start() < b for a, b in taken):
                    continue
                new = mt.group(0)
                for k, v in CURLY.items():
                    new = new.replace(k, v)
                ctx.add(n, mt.start(), mt.end(), new,
                        note="curly quote or apostrophe; the guide uses straight quotes")
        close = '(?:' + rq + '|(?<=\\S)")'
        if inside:
            for mt in re.finditer("(\\S+)(" + close + ")([.,])", m):
                if any(a <= mt.start(2) < b for a, b in taken):
                    continue
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + mt.group(3) + mt.group(2),
                        note="comma or period outside a closing quotation mark")
        else:
            for mt in re.finditer("(\\S+?)([.,])(" + close + ")(?=\\s|$)", m):
                if any(a <= mt.start(3) < b for a, b in taken):
                    continue
                ctx.add(n, mt.start(), mt.end(), mt.group(1) + mt.group(3) + mt.group(2), "uncertain",
                        note="comma or period inside a closing quotation mark "
                             "(keep it inside when it belongs to the quote)")


# ------------------------------------------------------------ bold-label

BOLD_LABEL_RE = re.compile(r"^(\s*(?:[-*+]|\d+[.)])\s+)\*\*(.+?)\*\*")


def check_bold_label(ctx):
    target = ctx.p["separator"]
    for n, _m in ctx.lines(headings=False):
        line = ctx.art.line(n)
        mt = BOLD_LABEL_RE.match(line)
        if not mt:
            continue
        inner, start, after_bold = mt.group(2), mt.end(1), mt.end()
        rest = line[after_bold:]
        sep, placement, label = None, None, inner
        if re.search(r"[:.]\s*$", inner):
            sep = "colon" if inner.rstrip().endswith(":") else "period"
            placement = "inside"
            label = inner.rstrip()[:-1].rstrip()
            sep_end = after_bold
        else:
            om = re.match(r"^\s*([:.])", rest)
            dm = re.match(r"^\s*([-–—])\s*", rest)
            if om:
                sep = "colon" if om.group(1) == ":" else "period"
                placement = "outside"
                sep_end = after_bold + om.end()
            elif dm:
                sep = "dash"
                placement = "outside"
                sep_end = after_bold + dm.end()
                while sep_end > after_bold and line[sep_end - 1] == " ":
                    sep_end -= 1
            else:
                continue
        if sep == target:
            continue
        if sep_end < len(line) and line[sep_end] == " ":
            pass
        if target == "dash":
            ctx.add(n, start, sep_end, None, note="bold label separated by a %s" % sep,
                    comment="Separate the bold label from its text with a dash.")
            continue
        char = ":" if target == "colon" else "."
        if placement == "inside":
            repl = "**%s%s**" % (label, char)
        else:
            repl = "**%s**%s" % (label, char)
        ctx.add(n, start, sep_end, repl, note="bold label separated by a %s; the guide uses a %s"
                % (sep, target))


# ------------------------------------------------------------ link-hygiene

TRACKING_EXACT = {"fbclid", "gclid", "rcm"}
MD_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\((<[^>]*>|[^)\s]*)")
URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>()\[\]]+", re.IGNORECASE)


def _clean_tracking(url):
    parts = urllib.parse.urlsplit(url)
    if not parts.query:
        return url
    kept = [p for p in parts.query.split("&")
            if p and not (p.split("=", 1)[0].lower().startswith("utm_")
                          or p.split("=", 1)[0].lower() in TRACKING_EXACT)]
    return urllib.parse.urlunsplit(parts._replace(query="&".join(kept)))


def check_link_hygiene(ctx):
    tracking, https, max_words = ctx.p["tracking"], ctx.p["https"], ctx.p["max_anchor_words"]
    for n, m in ctx.lines(kinds=("frontmatter", "code")):
        urls, linked = [], []
        for mt in MD_LINK_RE.finditer(m):
            linked.append((mt.start(), mt.end()))
            u_start = mt.start(3) + (1 if mt.group(3).startswith("<") else 0)
            urls.append((u_start, mt.group(3).strip("<>")))
            if not mt.group(1) and max_words:
                words = len(re.findall(r"\S+", re.sub(r"[*_`]", "", mt.group(2))))
                if words > max_words:
                    ctx.add(n, mt.start(2), mt.end(2), None,
                            note="anchor of %d words; the guide allows %d" % (words, max_words),
                            comment="Shorten the link text to %d words or fewer." % max_words)
        for mt in URL_RE.finditer(m):
            if any(a <= mt.start() < b for a, b in linked):
                continue
            url = mt.group(0).rstrip(".,;:!?'\">")
            urls.append((mt.start(), url))
        for start, url in urls:
            new, notes, certainty = url, [], "certain"
            if tracking:
                cleaned = _clean_tracking(new)
                if cleaned != new:
                    new = cleaned
                    notes.append("tracking parameters")
            if https and new.lower().startswith("http://") and not re.match(
                    r"^http://(localhost|127\.0\.0\.1)", new, re.IGNORECASE):
                new = "https://" + new[7:]
                notes.append("http link")
                certainty = "uncertain"
            if notes:
                ctx.add(n, start, start + len(url), new, certainty, note="; ".join(notes) + (
                    " (check that the site serves https)" if certainty == "uncertain" else ""))


# ------------------------------------------------------------ regex


def check_regex(ctx):
    flags = 0
    for letter in ctx.p.get("flags") or "":
        flags |= {"i": re.IGNORECASE, "m": re.MULTILINE, "s": re.DOTALL, "x": re.VERBOSE}[letter]
    rx = re.compile(ctx.p["pattern"], flags)
    template = ctx.p.get("replacement")
    for n, m in ctx.lines():
        for mt in rx.finditer(m):
            if mt.end() == mt.start() or MASK in mt.group(0):
                continue
            repl = mt.expand(template) if template is not None else None
            ctx.add(n, mt.start(), mt.end(), repl, ctx.p["certainty"], note=ctx.p["message"],
                    comment=ctx.p["message"])


def _regex_pattern(v):
    v = _str(v)
    try:
        re.compile(v)
    except re.error as exc:
        raise ParamError("is not a valid regular expression (%s): %r" % (exc, v))
    return v


def _optional_str(v):
    if v is None:
        return None
    if not isinstance(v, str):
        raise ParamError("must be a string, found %r" % (v,))
    return v


# ------------------------------------------------------------ registry

CHECKS = {
    "dash-spacing": (check_dash_spacing, {"style": (_enum("spaced", "closed", "none"), REQUIRED),
                                          "ranges": (_enum("en-dash", "hyphen"), None)}),
    "heading-case": (check_heading_case, {"case": (_enum("title", "sentence"), REQUIRED),
                                          "levels": (_levels, [2, 3, 4]),
                                          "style": (_enum("cmos", "ap"), "cmos")}),
    "heading-format": (check_heading_format, {"no_bold": (_bool, False),
                                              "no_end_period": (_bool, False)}),
    "serial-comma": (check_serial_comma, {"required": (_bool, REQUIRED)}),
    "banned": (check_banned, {"terms": (_str_list, REQUIRED), "case_sensitive": (_bool, False)}),
    "preferred": (check_preferred, {"pairs": (_pairs, REQUIRED)}),
    "term-case": (check_term_case, {"terms": (_str_list, REQUIRED)}),
    "numerals": (check_numerals, {"spell_out_below": (_int, 10)}),
    "ordinals": (check_ordinals, {"spell_out_below": (_int, 10)}),
    "sentence-start-numeral": (check_sentence_start_numeral, {}),
    "percent": (check_percent, {"style": (_enum("symbol", "word"), REQUIRED)}),
    "money": (check_money, {"style": (_enum("abbreviated", "words"), REQUIRED)}),
    "thousands": (check_thousands, {"style": (_enum("comma", "k", "either"), REQUIRED),
                                    "consistent": (_bool, True)}),
    "date-format": (check_date_format, {"ordinals": (_bool, False)}),
    "time-format": (check_time_format, {"style": (_enum("9am", "9 am", "9 a.m."), REQUIRED),
                                        "drop_zero_minutes": (_bool, False),
                                        "noon_midnight": (_bool, False)}),
    "quote-style": (check_quote_style, {"marks": (_enum("curly", "straight"), REQUIRED),
                                        "punctuation_inside": (_bool, True)}),
    "bold-label": (check_bold_label, {"separator": (_enum("colon", "period", "dash"), REQUIRED)}),
    "link-hygiene": (check_link_hygiene, {"tracking": (_bool, True), "https": (_bool, True),
                                          "max_anchor_words": (_optional_int, 12)}),
    "regex": (check_regex, {"pattern": (_regex_pattern, REQUIRED), "message": (_str, REQUIRED),
                            "flags": (_flags, ""), "replacement": (_optional_str, None),
                            "certainty": (_enum("certain", "uncertain"), "certain")}),
}


def normalize_params(check, params):
    """(normalized params, list of error strings)."""
    if check not in CHECKS:
        return None, ["unknown check %r (known: %s)" % (check, ", ".join(sorted(CHECKS)))]
    spec = CHECKS[check][1]
    out, errors = {}, []
    for key in params:
        if key not in spec:
            errors.append("check %s takes no parameter %r (it takes: %s)"
                          % (check, key, ", ".join(sorted(spec)) or "none"))
    for key, (validator, default) in spec.items():
        if key in params and params[key] is not None:
            try:
                out[key] = validator(params[key])
            except ParamError as exc:
                errors.append("%s: parameter %s %s" % (check, key, exc))
        elif default is REQUIRED:
            errors.append("check %s needs the parameter %s" % (check, key))
        else:
            out[key] = default
    return out, errors


def in_scope(rule, content_type):
    scope = rule.get("scope", "all")
    if scope in (None, "all"):
        return True
    if content_type is None:
        return True
    return content_type in scope


def gather_extra(rules, article):
    known = set()
    for rule in rules:
        if rule.get("check") == "term-case":
            terms = rule.get("params", {}).get("terms") or []
            known.update(terms if isinstance(terms, list) else [terms])
    lower = set()
    for n in article.numbers():
        if article.is_prose(n):
            lower.update(w for w in re.findall(r"\b[a-z][a-z'’]*\b", article.masked(n)))
    return {"known_terms": known, "lower_words": lower}


def run_rule(rule, article, extra=None):
    params, errors = normalize_params(rule["check"], rule.get("params") or {})
    if errors:
        raise ValueError("; ".join(errors))
    ctx = Ctx(rule, params, article, extra if extra is not None else gather_extra([rule], article))
    CHECKS[rule["check"]][0](ctx)
    return ctx.out


def run_lint(rules, article, content_type=None):
    """Lint findings for every rule with a check that applies, plus the built-in
    PROOF-PAIR check, sorted, with L-ids."""
    extra = gather_extra(rules, article)
    found = []
    for rule in rules:
        if not rule.get("check") or not in_scope(rule, content_type):
            continue
        found.extend(run_rule(rule, article, extra))
    found.extend(pairs.check_pairs(article))
    found.sort(key=lambda f: (f["line"], f["col"], f["rule_id"]))
    width = max(4, len(str(len(found))))
    for i, f in enumerate(found):
        f["id"] = "L" + str(i + 1).zfill(width)
    return found
