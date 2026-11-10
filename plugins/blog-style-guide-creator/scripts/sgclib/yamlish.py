"""The small YAML subset guides use: `key: value`, inline lists `[a, b]`,
quoted strings, booleans, and numbers. Nothing nested."""
import json
import re

from .common import die

_NUMBER = re.compile(r"^-?\d+(\.\d+)?$")
_KEY_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:(?:\s+(.*)|\s*)$")


def _split_list(inner, where):
    items, buf, quote, i = [], [], None, 0
    while i < len(inner):
        ch = inner[i]
        if quote:
            buf.append(ch)
            if ch == "\\" and quote == '"' and i + 1 < len(inner):
                buf.append(inner[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'" and not "".join(buf).strip():
            # A quote mark opens a quoted item only at the item's start; mid-word it is an apostrophe.
            quote = ch
            buf.append(ch)
        elif ch == ",":
            items.append("".join(buf))
            buf = []
        elif ch in "[]":
            die("%s: nested lists are not part of the rule-block syntax: [%s]" % (where, inner))
        else:
            buf.append(ch)
        i += 1
    if quote:
        die("%s: unclosed quote in list [%s]" % (where, inner))
    items.append("".join(buf))
    items = [x.strip() for x in items]
    if items == [""]:
        return []
    if any(x == "" for x in items):
        die("%s: empty item in list [%s]" % (where, inner))
    return items


def parse_scalar(raw, where="value"):
    s = raw.strip()
    if s.startswith('"'):
        if len(s) < 2 or not s.endswith('"'):
            die("%s: unclosed double quote: %s" % (where, s))
        try:
            return json.loads(s)
        except ValueError:
            die("%s: malformed double-quoted string: %s" % (where, s))
    if s.startswith("'"):
        if len(s) < 2 or not s.endswith("'"):
            die("%s: unclosed single quote: %s" % (where, s))
        return s[1:-1].replace("''", "'")
    low = s.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "~"):
        return None
    if _NUMBER.match(s):
        return float(s) if "." in s else int(s)
    return s


def parse_value(raw, where="value"):
    s = (raw or "").strip()
    if s.startswith("["):
        if not s.endswith("]"):
            die("%s: unclosed list: %s" % (where, s))
        return [parse_scalar(x, where) for x in _split_list(s[1:-1], where)]
    if s == "":
        return None
    return parse_scalar(s, where)


def parse_block(lines, where="block"):
    """Parse `key: value` lines into an ordered dict. Blank lines and `#` comment
    lines are skipped; anything else is an error."""
    out = {}
    for offset, line in enumerate(lines):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = _KEY_LINE.match(line.strip())
        if not m:
            die("%s, line %d: expected `key: value`, found %r" % (where, offset + 1, line))
        key = m.group(1)
        if key in out:
            die("%s: key %r appears twice" % (where, key))
        out[key] = parse_value(m.group(2) or "", "%s, key %s" % (where, key))
    return out


def _needs_quotes(s):
    if s == "" or s != s.strip():
        return True
    if s[0] in "[\"'#{&*!|>%@`" or s.lower() in ("true", "false", "null", "~"):
        return True
    if _NUMBER.match(s):
        return True
    return "\n" in s


def format_scalar(value, in_list=False):
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    if _needs_quotes(s) or (in_list and re.search(r"[,\[\]]", s)):
        return json.dumps(s, ensure_ascii=False)
    return s


def format_value(value):
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(format_scalar(v, True) for v in value) + "]"
    return format_scalar(value)


def split_frontmatter(text):
    """(frontmatter dict or None, number of lines the block takes, body lines)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, 0, lines
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            return parse_block(lines[1:i], "frontmatter"), i + 1, lines[i + 1:]
    die("frontmatter opens with --- but never closes")


def render_frontmatter(data):
    out = ["---"]
    for key, value in data.items():
        out.append("%s: %s" % (key, format_value(value)))
    out.append("---")
    return "\n".join(out)
