"""profile: count every lint pattern across source articles, so rules cite real counts."""
import re
from pathlib import Path

from . import lint as L
from .article import Article
from .common import die, read_text

SPELLED = r"\b(one|two|three|four|five|six|seven|eight|nine)\b"
SPELLED_ORD = r"\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)\b"


def _heading_case(text):
    words = [w for w in L.TOKEN_RE.findall(text) if not L._skip_token(w)]
    rest = [w for w in words[1:] if w.lower() not in L.ALL_SMALL and w.lower() not in L.ALWAYS_PROPER]
    if len(rest) < 2:
        return "ambiguous"
    caps = sum(1 for w in rest if w[0].isupper())
    if caps == len(rest):
        return "title"
    if caps <= len(rest) // 3:
        return "sentence"
    return "mixed"


def profile_article(art):
    c = {}
    # Count digits the way the numerals check reads them, so list numbering, times,
    # percentages, and units stay out of the evidence a rule cites.
    digits_by_line = {}
    probe = {"id": "PROFILE", "check": "numerals", "params": {"spell_out_below": 10}}
    for f in L.run_rule(probe, art):
        digits_by_line[f["line"]] = digits_by_line.get(f["line"], 0) + 1

    def inc(key, n=1):
        c[key] = c.get(key, 0) + n

    for n, (level, text, col) in art.headings.items():
        inc("headings.h%d.%s" % (level, _heading_case(art.masked(n)[col:])))
        if re.search(r"(?<!\.)\.\s*$", text.rstrip("*_")):
            inc("headings.end_period")
        if "**" in text or "__" in text:
            inc("headings.bold")
        inc("headings.total")
    for n in art.numbers():
        if n <= art.fm_lines or n in art.fence_lines:
            continue
        m = art.masked(n)
        mq = art.masked(n, ("frontmatter", "code", "url"))
        for i, ch in enumerate(m):
            if ch == L.EM:
                left = i > 0 and m[i - 1] == " "
                right = i + 1 < len(m) and m[i + 1] == " "
                inc("em_dash.spaced" if left and right else "em_dash.closed" if not (left or right) else "em_dash.one_sided")
        for mt in re.finditer(r"(?<=\S) (--|-|–) (?=\S)", m):
            if mt.group(1) == L.EN and m[mt.start() - 1].isdigit() and m[mt.end()].isdigit():
                continue
            inc("dash_substitute.spaced_en_dash" if mt.group(1) == L.EN else "dash_substitute.spaced_hyphen")
        inc("ranges.en_dash", len(re.findall(r"\d\s*–\s*\d", m)))
        inc("ranges.hyphen", len(re.findall(r"(?<![\w\-/.:,])\d+-\d+(?![\w\-/:]|[.,]\d)", m)))
        if n not in art.headings:
            inc("serial_comma.with", len(re.findall(r"%s, (?:%s ){0,3}%s, (?:and|or) " % (L._W, L._W, L._W), m)))
            inc("serial_comma.without", len(re.findall(r"%s, (?:%s ){0,3}%s (?:and|or) " % (L._W, L._W, L._W), m)))
        inc("quotes.straight_double", mq.count('"'))
        inc("quotes.curly_double", mq.count("“") + mq.count("”"))
        inc("quotes.straight_apostrophe", len(re.findall(r"(?<=\w)'(?=\w)", mq)))
        inc("quotes.curly_apostrophe", len(re.findall(r"(?<=\w)’(?=\w)", mq)))
        inc("quotes.punctuation_outside", len(re.findall(r"(?:”|(?<=\S)\")[.,]", mq)))
        inc("quotes.punctuation_inside", len(re.findall(r"[.,](?:”|\")(?=\s|$)", mq)))
        if n not in art.table_lines:
            inc("numerals.under_10_digits", digits_by_line.get(n, 0))
            inc("numerals.under_10_words", len(re.findall(SPELLED, m, re.IGNORECASE)))
            inc("ordinals.digits", len(re.findall(r"(?<![\w.])[1-9](?:st|nd|rd|th)\b", m)))
            inc("ordinals.words", len(re.findall(SPELLED_ORD, m, re.IGNORECASE)))
        inc("percent.symbol", len(re.findall(r"\d\s?%", m)))
        inc("percent.word", len(re.findall(r"\d\s?(?:percent|per cent)\b", m, re.IGNORECASE)))
        inc("money.abbreviated", len(re.findall(r"[$€£¥]\s?\d[\d.,]*(?:bn|mn|[KMBTkmbt])\b", m)))
        inc("money.words", len(re.findall(r"[$€£¥]\s?\d[\d.,]*\s+(?:thousand|million|billion|trillion)\b", m, re.IGNORECASE)))
        inc("thousands.k", len(L.K_RE.findall(m)))
        inc("thousands.comma", len(L.COMMA_RE.findall(m)))
        inc("dates.ordinal", len(re.findall(r"\b" + L.MONTHS + r"\.?\s+\d{1,2}(?:st|nd|rd|th)\b", m)))
        inc("dates.plain", len(re.findall(r"\b" + L.MONTHS + r"\.?\s+\d{1,2}(?![\d\w])", m)))
        for mt in L.TIME_RE.finditer(m):
            dotted = "." in mt.group(4)
            inc("times.9 a.m." if dotted else "times.9 am" if mt.group(3) else "times.9am")
        line = art.line(n)
        bm = L.BOLD_LABEL_RE.match(line)
        if bm and n not in art.headings:
            inner, rest = bm.group(2), line[bm.end():]
            if re.search(r":\s*$", inner) or re.match(r"^\s*:", rest):
                inc("bold_labels.colon")
            elif re.search(r"\.\s*$", inner) or re.match(r"^\s*\.", rest):
                inc("bold_labels.period")
            elif re.match(r"^\s*[-–—]", rest):
                inc("bold_labels.dash")
            else:
                inc("bold_labels.none")
        ml = art.masked(n, ("frontmatter", "code"))
        for mt in L.MD_LINK_RE.finditer(ml):
            if mt.group(1):
                inc("images")
                continue
            inc("links.total")
            url = mt.group(3)
            if url.lower().startswith("http://"):
                inc("links.http")
            if L._clean_tracking(url) != url:
                inc("links.tracking")
    return dict(sorted((k, v) for k, v in c.items() if v))


def profile(paths):
    if not paths:
        die("profile needs at least one article file")
    files = []
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            files.extend(sorted(x for x in pp.iterdir() if x.suffix.lower() in (".md", ".markdown")))
        else:
            files.append(pp)
    if not files:
        die("no Markdown articles found in %s" % ", ".join(paths))
    per, totals, present = {}, {}, {}
    for f in files:
        counts = profile_article(Article(read_text(f, "article")))
        per[f.name] = counts
        for k, v in counts.items():
            totals[k] = totals.get(k, 0) + v
            present[k] = present.get(k, 0) + 1
    return {"articles": len(files), "files": [str(f) for f in files],
            "totals": dict(sorted(totals.items())),
            "articles_with": dict(sorted(present.items())), "per_article": per}
