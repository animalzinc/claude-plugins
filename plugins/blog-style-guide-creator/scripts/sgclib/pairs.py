"""Built-in PROOF-PAIR check: unclosed parentheses, square brackets, and bold markers.

Runs on every draft, whatever the guide says, because an unclosed bracket is an
error in any house style. Each paragraph, list item, and heading is checked on
its own, with code spans, URLs, and frontmatter masked. Quotation marks stay
with the proofreader agent: a quote may run across paragraphs on purpose.
Findings are comments, since only the author knows where the closing mark goes.
"""
import re

from .article import MASK

ZONES = ("frontmatter", "code", "url")
# "1)", "a)" at a word start: an enumeration, not a closing parenthesis.
ENUM_RE = re.compile(r"(?:^|[\s(])(?:\d{1,2}|[A-Za-z])$")
EMOTICON_RE = re.compile(r"[:;]-?$")
# A Markdown link or image target, allowing one level of parentheses inside the URL.
LINK_TARGET_RE = re.compile(r"\]\((?:[^()\s]|\([^()\s]*\))*\)")
ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
OPENERS = {"(": ")", "[": "]"}
CLOSERS = {")": "(", "]": "["}
NAMES = {"(": "parenthesis", "[": "square bracket"}


def _units(article):
    """Lists of line numbers, one per paragraph, list item, blockquote, or heading."""
    units = [[n] for n in sorted(article.headings)]
    for block in article.blocks():
        lines = list(range(block["line_start"], block["line_end"] + 1))
        if block["kind"] in ("code", "table"):
            continue
        if block["kind"] == "list":
            # One unit per item: a marker line plus the continuation lines that wrap it.
            item = []
            for n in lines:
                text = article.line(n)
                if not text.strip():
                    continue
                if ITEM_RE.match(text) and item:
                    units.append(item)
                    item = []
                item.append(n)
            if item:
                units.append(item)
        else:
            units.append([n for n in lines if article.line(n).strip()])
    return [u for u in units if u]


def _after(line, col, words=5):
    m = re.match(r"\S+(?:\s+\S+){0,%d}" % (words - 1), line[col:])
    return line[col:col + m.end()] if m else line[col:col + 1]


def _before(line, col, words=4):
    m = re.search(r"(?:\S+\s+){0,%d}\S*$" % (words - 1), line[:col + 1])
    return line[m.start():col + 1] if m else line[col:col + 1]


def _finding(article, n, start, quote, comment, note):
    return {"rule_id": "PROOF-PAIR", "pass": "lint", "line": n, "col": start, "quote": quote,
            "replacement": None, "comment": comment, "basis": "explicit", "certainty": "certain",
            "note": note, "check": "pairs"}


def check_pairs(article):
    out = []
    for unit in _units(article):
        stack, bold = [], []
        for n in unit:
            line, masked = article.line(n), article.masked(n, ZONES)
            masked = LINK_TARGET_RE.sub(lambda m: "]" + MASK * (len(m.group(0)) - 1), masked)
            for mt in re.finditer(r"\*\*", masked):
                bold.append((n, mt.start()))
            for col, ch in enumerate(masked):
                if ch in OPENERS:
                    stack.append((ch, n, col))
                elif ch in CLOSERS:
                    if stack and stack[-1][0] == CLOSERS[ch]:
                        stack.pop()
                        continue
                    if any(s[0] == CLOSERS[ch] for s in stack):
                        # A mismatch such as "( ... ]": report the opener that is still open below.
                        continue
                    before = masked[:col]
                    if ch == ")" and (ENUM_RE.search(before) or EMOTICON_RE.search(before)):
                        continue
                    if MASK in masked[max(0, col - 1):col + 1]:
                        continue
                    out.append(_finding(article, n, col if col == 0 else col - len(_before(line, col)) + 1,
                                        _before(line, col),
                                        "A closing %s with no opening one in this paragraph." % NAMES[CLOSERS[ch]],
                                        "unopened %s" % NAMES[CLOSERS[ch]]))
        for ch, n, col in stack:
            line = article.line(n)
            out.append(_finding(article, n, col, _after(line, col),
                                "An opening %s that nothing in this paragraph closes." % NAMES[ch],
                                "unclosed %s" % NAMES[ch]))
        if len(bold) % 2:
            n, col = bold[-1]
            line = article.line(n)
            out.append(_finding(article, n, col, _after(line, col, 3),
                                "A bold marker (**) that nothing in this paragraph closes or opens.",
                                "unpaired bold marker"))
    return out
