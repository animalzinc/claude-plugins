"""Shared helpers: errors, file IO, text normalization, number words."""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path


class SgcError(Exception):
    """An input is missing or malformed. The CLI prints it and exits 2."""


def die(message):
    raise SgcError(message)


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path, what="file"):
    """Read a UTF-8 file with newlines normalized to \\n and a BOM removed."""
    p = Path(path)
    if not p.exists():
        die("missing %s: %s" % (what, p))
    if p.is_dir():
        die("%s must be a file, found a folder: %s" % (what, p))
    try:
        raw = p.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        die("%s is not UTF-8 (%s): %s" % (what, exc, p))
    except OSError as exc:
        die("could not read %s (%s): %s" % (what, exc, p))
    if raw.startswith("﻿"):
        raw = raw[1:]
    return raw.replace("\r\n", "\n").replace("\r", "\n")


def read_json(path, what="JSON file"):
    raw = read_text(path, what)
    try:
        return json.loads(raw)
    except ValueError as exc:
        die("%s is not valid JSON (%s): %s" % (what, exc, path))


def write_text(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".%d.tmp" % os.getpid())
    with open(str(tmp), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.replace(str(tmp), str(p))
    return p


def write_json(path, data):
    return write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def dumps(data):
    return json.dumps(data, indent=2, ensure_ascii=False)


def slugify(text):
    out = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return out or "item"


def rule_id_from(text):
    """An ID-safe form of any string: uppercase letters, digits, hyphens."""
    out = re.sub(r"[^A-Z0-9]+", "-", (text or "").upper()).strip("-")
    return out or "X"


# ------------------------------------------------------------ normalization

_QUOTE_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "„": '"', "″": '"',
}
_DASH_MAP = {
    "—": "-", "–": "-", "‒": "-", "−": "-", "‐": "-", "‑": "-",
}
_ELLIPSIS = re.compile(r"…|\.\.\.+")


def strip_emphasis(text):
    """Remove Markdown bold and italic markers that touch a word, and link markup,
    so two spellings of one passage compare equal."""
    out = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text or "")
    out = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", out)
    out = re.sub(r"(?<=\w)[*_]+(?=\W|$)|(?<=\W)[*_]+(?=\w)|^[*_]+(?=\w)", "", out)
    return out


def normalize_text(text):
    """Flatten text for comparison: emphasis stripped, lowercase, straight quotes,
    plain hyphens, no ellipses, single spaces."""
    out = strip_emphasis(text).lower()
    for src, dst in _QUOTE_MAP.items():
        out = out.replace(src, dst)
    for src, dst in _DASH_MAP.items():
        out = out.replace(src, dst)
    out = out.replace(" ", " ")
    out = _ELLIPSIS.sub(" ", out)
    out = re.sub(r"\s+", " ", out)
    return out.strip()


# ------------------------------------------------------------ number words

_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
         "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
         "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
_ORDINAL_IRREGULAR = {"one": "first", "two": "second", "three": "third", "five": "fifth",
                      "eight": "eighth", "nine": "ninth", "twelve": "twelfth"}


def number_words(n):
    """English words for 0 to 999, or None outside that range."""
    if n < 0 or n > 999:
        return None
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + ("-" + _ONES[ones] if ones else "")
    hundreds, rest = divmod(n, 100)
    out = _ONES[hundreds] + " hundred"
    if rest:
        out += " " + number_words(rest)
    return out


def ordinal_words(n):
    words = number_words(n)
    if words is None:
        return None
    parts = re.split(r"([ -])", words)
    last = parts[-1]
    if last in _ORDINAL_IRREGULAR:
        last = _ORDINAL_IRREGULAR[last]
    elif last.endswith("y"):
        last = last[:-1] + "ieth"
    else:
        last += "th"
    parts[-1] = last
    return "".join(parts)


SPELLED_NUMBERS = {w: i for i, w in enumerate(_ONES)}
