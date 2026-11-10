"""The article model: lines, structure, and protected zones.

Protected zones are character spans on a line, with a kind:
    frontmatter  the leading --- block
    code         fenced code lines, inline code, HTML comments
    blockquote   a line starting with >
    url          link targets, autolinks, bare URLs, reference definitions
    quote        text inside double quotation marks, straight or curly
Columns are 0-based character offsets, the end exclusive. Line numbers are 1-based.
"""
import re

from .yamlish import parse_scalar

ALL_KINDS = ("frontmatter", "code", "blockquote", "url", "quote")
MASK = "\x00"

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*(?:[ \t]#+[ \t]*)?$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
TABLE_RE = re.compile(r"^\s*\|")
INLINE_CODE_RE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->")
LINK_TARGET_RE = re.compile(r"\]\((<[^>]*>|[^)\s]*)(?:\s+\"[^\"]*\")?\)")
AUTOLINK_RE = re.compile(r"<(?:https?|mailto|ftp):[^>\s]+>", re.IGNORECASE)
BARE_URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>()\[\]]+", re.IGNORECASE)
REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")
QUOTE_RE = re.compile(r"\"[^\"\n]+\"|“[^”\n]*”")
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\((<[^>]*>|[^)\s]*)(?:\s+\"[^\"]*\")?\)")
SENTENCE_BOUNDARY_RE = re.compile(r"[.!?][\"'”’)\]*_]*\s+")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")


def _merge(spans):
    out = []
    for start, end, kind in sorted(spans):
        if out and start < out[-1][1]:
            prev = out[-1]
            if end > prev[1]:
                out[-1] = (prev[0], end, prev[2])
            continue
        out.append((start, end, kind))
    return out


def mask_spans(line, spans):
    chars = list(line)
    for start, end, _kind in spans:
        for i in range(start, min(end, len(chars))):
            chars[i] = MASK
    return "".join(chars)


def loose_frontmatter(lines):
    """Flat `key: value` pairs of an article's frontmatter, ignoring anything
    nested; (dict, number of lines) or (None, 0)."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            data = {}
            for line in lines[1:i]:
                m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
                if m and not line.startswith((" ", "\t")):
                    raw = m.group(2).strip()
                    try:
                        data[m.group(1)] = parse_scalar(raw) if raw else None
                    except Exception:  # a value outside the subset is kept as text
                        data[m.group(1)] = raw
            return data, i + 1
    return None, 0


class Article(object):
    def __init__(self, text):
        if text.endswith("\n"):
            text = text[:-1]
        self.text = text
        self.lines = text.split("\n") if text else []
        self.frontmatter, self.fm_lines = loose_frontmatter(self.lines)
        self.fence_lines = set()
        self.headings = {}      # line number -> (level, text, column where text starts)
        self.list_lines = set()
        self.table_lines = set()
        self.quote_lines = set()
        self.spans = {}         # line number -> [(start, end, kind)]
        self._scan()

    # ------------------------------------------------------------ scanning

    def _scan(self):
        in_fence = None
        for idx, line in enumerate(self.lines):
            n = idx + 1
            spans = []
            if n <= self.fm_lines:
                spans.append((0, len(line), "frontmatter"))
                self.spans[n] = spans
                continue
            fence = FENCE_RE.match(line)
            if in_fence:
                self.fence_lines.add(n)
                spans.append((0, len(line), "code"))
                if fence and fence.group(1)[0] == in_fence[0] and len(fence.group(1)) >= len(in_fence) \
                        and not line.strip()[len(fence.group(1)):].strip():
                    in_fence = None
                self.spans[n] = spans
                continue
            if fence:
                in_fence = fence.group(1)
                self.fence_lines.add(n)
                self.spans[n] = [(0, len(line), "code")]
                continue
            if re.match(r"^\s{0,3}>", line):
                self.quote_lines.add(n)
                spans.append((0, len(line), "blockquote"))
            h = HEADING_RE.match(line)
            if h and not spans:
                self.headings[n] = (len(h.group(1)), h.group(2), h.start(2))
            if LIST_RE.match(line):
                self.list_lines.add(n)
            if TABLE_RE.match(line):
                self.table_lines.add(n)
            code = [(m.start(), m.end(), "code") for m in INLINE_CODE_RE.finditer(line)]
            code += [(m.start(), m.end(), "code") for m in HTML_COMMENT_RE.finditer(line)]
            spans.extend(code)
            step = mask_spans(line, code)
            urls = []
            for m in LINK_TARGET_RE.finditer(step):
                urls.append((m.start(1), m.end(1), "url"))
            for m in AUTOLINK_RE.finditer(step):
                urls.append((m.start(), m.end(), "url"))
            for m in BARE_URL_RE.finditer(step):
                end = m.end()
                while end > m.start() and line[end - 1] in ".,;:!?'\"":
                    end -= 1
                urls.append((m.start(), end, "url"))
            ref = REF_DEF_RE.match(step)
            if ref:
                urls.append((ref.start(1), ref.end(1), "url"))
            spans.extend(urls)
            step = mask_spans(step, urls)
            spans.extend((m.start(), m.end(), "quote") for m in QUOTE_RE.finditer(step))
            self.spans[n] = _merge_keep_kinds(spans)
        return self

    def strip_list_marker(self, n):
        """Column where a list item's text starts, or 0."""
        m = LIST_RE.match(self.lines[n - 1])
        return m.end() if m else 0

    # ------------------------------------------------------------ access

    def line(self, n):
        return self.lines[n - 1]

    def numbers(self):
        return range(1, len(self.lines) + 1)

    def zones(self, n, kinds=ALL_KINDS):
        return [s for s in self.spans.get(n, []) if s[2] in kinds]

    def masked(self, n, kinds=ALL_KINDS):
        return mask_spans(self.lines[n - 1], self.zones(n, kinds))

    def is_prose(self, n):
        """A line of running text: not frontmatter, code, heading, table, or blank."""
        return (n > self.fm_lines and n not in self.fence_lines and n not in self.headings
                and n not in self.table_lines and bool(self.lines[n - 1].strip()))

    def zone_at(self, n, start, end, kinds=ALL_KINDS):
        """The kind of a zone that holds all of [start, end), or None."""
        for s, e, kind in self.zones(n, kinds):
            if s <= start and end <= e:
                return kind
        return None

    def numbered(self):
        width = max(4, len(str(len(self.lines))))
        return "\n".join("L%s| %s" % (str(i + 1).zfill(width), line)
                         for i, line in enumerate(self.lines)) + "\n"

    # ------------------------------------------------------------ outline

    def sentence_at(self, n, col):
        line = self.lines[n - 1]
        masked = self.masked(n, ("code", "url"))
        start, end = 0, len(line)
        for m in SENTENCE_BOUNDARY_RE.finditer(masked):
            if m.end() <= col:
                start = m.end()
            elif m.start() >= col:
                end = m.start() + 1
                break
        return line[start:end].strip()

    def links(self):
        out = []
        for n in self.numbers():
            if n <= self.fm_lines or n in self.fence_lines:
                continue
            masked_code = self.masked(n, ("code",))
            for m in LINK_RE.finditer(masked_code):
                url = m.group(3).strip("<>")
                out.append({"line": n, "col": m.start(), "image": bool(m.group(1)),
                            "anchor": m.group(2), "url": url,
                            "sentence": self.sentence_at(n, m.start())})
            linked = [(m.start(), m.end()) for m in LINK_RE.finditer(masked_code)]
            for m in BARE_URL_RE.finditer(masked_code):
                if any(a <= m.start() < b for a, b in linked):
                    continue
                url = m.group(0).rstrip(".,;:!?'\">")
                out.append({"line": n, "col": m.start(), "image": False, "anchor": None,
                            "url": url, "sentence": self.sentence_at(n, m.start())})
        return out

    def blocks(self):
        out, current = [], None
        for n in self.numbers():
            if n <= self.fm_lines:
                continue
            line = self.lines[n - 1]
            if n in self.headings:
                if current:
                    out.append(current)
                current = None
                continue
            if not line.strip() and n not in self.fence_lines:
                if current:
                    out.append(current)
                current = None
                continue
            if n in self.fence_lines:
                kind = "code"
            elif n in self.quote_lines:
                kind = "blockquote"
            elif n in self.table_lines:
                kind = "table"
            elif n in self.list_lines:
                kind = "list"
            else:
                kind = "paragraph"
            if current and (current["kind"] == kind or (current["kind"] == "list" and kind == "paragraph")):
                current["line_end"] = n
            else:
                if current:
                    out.append(current)
                current = {"kind": kind, "line_start": n, "line_end": n}
        if current:
            out.append(current)
        for block in out:
            if block["kind"] == "code":
                block["words"] = 0
            else:
                block["words"] = sum(count_words(self.masked(i, ("code", "url", "frontmatter")))
                                     for i in range(block["line_start"], block["line_end"] + 1))
        return out

    def outline(self, content_type=None):
        heads = [{"line": n, "level": lvl, "text": text}
                 for n, (lvl, text, _col) in sorted(self.headings.items())]
        title = next((h["text"] for h in heads if h["level"] == 1), None)
        if title is None and self.frontmatter:
            title = self.frontmatter.get("title")
        blocks = self.blocks()
        zones = []
        for n in self.numbers():
            for start, end, kind in self.spans.get(n, []):
                zones.append({"line": n, "start": start, "end": end, "kind": kind})
        words = sum(b["words"] for b in blocks) + sum(
            count_words(h["text"]) for h in heads)
        return {
            "title": title,
            "content_type": content_type,
            "lines": len(self.lines),
            "frontmatter": {"lines": [1, self.fm_lines] if self.fm_lines else None,
                            "data": self.frontmatter},
            "word_count": words,
            "headings": heads,
            "paragraphs": blocks,
            "links": self.links(),
            "protected": zones,
        }


def _merge_keep_kinds(spans):
    """Drop spans nested inside an earlier, wider span; keep the rest as found."""
    spans = sorted(spans, key=lambda s: (s[0], -(s[1] - s[0])))
    out = []
    for span in spans:
        if any(o[0] <= span[0] and span[1] <= o[1] for o in out):
            continue
        out.append(span)
    return out


def count_words(text):
    clean = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text or "")
    clean = clean.replace(MASK, " ")
    return len(WORD_RE.findall(clean))
