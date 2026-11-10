"""extract: a URL, saved HTML, or Markdown file into clean Markdown.

HTML: the article body is the <article> element, else <main>, else the deepest
container holding at least half the page's prose. Navigation, headers,
footers, asides, forms, scripts, and styles are dropped. Kept: headings,
paragraphs, emphasis, links, lists (nested), block quotes, code, tables,
images with alt text, and footnotes (`[^1]` references and definitions).
"""
import html as html_module
import re
from html.parser import HTMLParser
from pathlib import Path

from .article import count_words
from .common import die, read_text, write_text
from .fetch import fetch_text, title_from_html

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source",
        "track", "wbr"}
DROP = {"script", "style", "noscript", "template", "nav", "header", "footer", "aside", "form",
        "svg", "iframe", "button", "select", "textarea", "head", "title", "canvas"}
INLINE = {"a", "abbr", "b", "bdi", "bdo", "cite", "code", "data", "dfn", "em", "i", "kbd", "mark",
          "q", "s", "samp", "small", "span", "strong", "sub", "sup", "time", "u", "var", "img",
          "br", "#text", "del", "ins", "label", "font"}
HEADINGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}


class _Dom(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = {"tag": "#root", "attrs": {}, "children": []}
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": dict(attrs), "children": []}
        self.stack[-1]["children"].append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1]["children"].append({"tag": tag, "attrs": dict(attrs), "children": []})

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1]["children"].append({"tag": "#text", "attrs": {}, "children": [], "text": data})


def _find(node, tags, out=None):
    out = [] if out is None else out
    if node["tag"] in tags:
        out.append(node)
    for c in node["children"]:
        _find(c, tags, out)
    return out


def _plain(node, skip_links=False):
    if node["tag"] == "#text":
        return node.get("text", "")
    if node["tag"] in DROP or (skip_links and node["tag"] == "a"):
        return " "
    return " ".join(_plain(c, skip_links) for c in node["children"])


def _prose_len(node):
    return len(re.sub(r"\s+", "", _plain(node, skip_links=True)))


def _is_footnotes(node):
    attrs = node.get("attrs") or {}
    hay = ("%s %s %s" % (attrs.get("class") or "", attrs.get("id") or "", attrs.get("role") or "")).lower()
    return "footnote" in hay or "doc-endnotes" in hay


def choose_body(root):
    for tag in ("article", "main"):
        found = [n for n in _find(root, {tag}) if _prose_len(n) > 0]
        if found:
            return max(found, key=_prose_len)
    total = _prose_len(root)
    core = root
    while total:
        rich = [c for c in core["children"] if c["tag"] not in DROP and c["tag"] not in INLINE
                and c["tag"] not in HEADINGS and c["tag"] not in ("p", "ul", "ol", "table", "li")
                and _prose_len(c) >= 0.5 * total]
        if not rich:
            break
        core = rich[0]
    bodies = _find(root, {"body"})
    return core if core is not root else (bodies[0] if bodies else root)


def _wrap(inner, mark, close=None):
    body = inner.strip()
    if not body:
        return " " if inner and inner.isspace() else ""
    lead = " " if inner[:1].isspace() else ""
    trail = " " if inner[-1:].isspace() else ""
    return lead + mark + body + (mark if close is None else close) + trail


def _footnote_ref(node):
    links = _find(node, {"a"})
    if not links:
        return None
    href = links[0]["attrs"].get("href") or ""
    if not href.startswith("#"):
        return None
    label = re.sub(r"\D", "", _plain(node)) or re.sub(r"\D", "", href)
    return "[^%s]" % label if label else None


def _inline(node):
    tag = node["tag"]
    if tag in DROP:
        return ""
    if tag == "#text":
        return re.sub(r"[ \t\r\n]+", " ", node.get("text", ""))
    if tag == "br":
        return "  \n"
    if tag == "img":
        src = node["attrs"].get("src") or node["attrs"].get("data-src") or ""
        return "![%s](%s)" % ((node["attrs"].get("alt") or "").strip(), src)
    if tag == "sup":
        ref = _footnote_ref(node)
        if ref:
            return ref
    inner = "".join(_inline(c) for c in node["children"])
    if tag == "a":
        href = node["attrs"].get("href") or ""
        if not inner.strip():
            return ""
        if re.match(r"^#fn|^#footnote", href) and re.match(r"^\s*\[?\d+\]?\s*$", inner):
            return "[^%s]" % re.sub(r"\D", "", inner)
        if not href or href.startswith("#") or href.startswith("javascript:"):
            return inner
        return _wrap(inner, "[", "](%s)" % href)
    if tag in ("strong", "b"):
        return _wrap(inner, "**")
    if tag in ("em", "i"):
        return _wrap(inner, "*")
    if tag == "code":
        return _wrap(inner, "`")
    return inner


def _clean(text):
    return re.sub(r"[ \t]+", " ", text).strip()


def _footnote_blocks(node):
    out = []
    for i, li in enumerate(_find(node, {"li"})):
        label = re.sub(r"\D", "", li["attrs"].get("id") or "") or str(i + 1)
        parts = [c for c in li["children"]]
        text = _clean("".join(_inline(c) for c in parts))
        text = re.sub(r"\s*[↩↪]︎?\s*$", "", text)
        text = re.sub(r"\s*\[↩︎?\]\([^)]*\)\s*$", "", text).strip()
        if text:
            out.append("[^%s]: %s" % (label, text))
    return out


def _list(node, ordered, depth):
    out, index = [], 0
    for item in node["children"]:
        if item["tag"] != "li":
            continue
        index += 1
        inner = _blocks(item, depth + 1)
        if not inner:
            continue
        marker = "%d." % index if ordered else "-"
        pad = "  " * depth
        out.append("%s%s %s" % (pad, marker, inner[0]))
        for extra in inner[1:]:
            out.append(extra if re.match(r"^\s*([-*+]|\d+\.)\s", extra) else "%s  %s" % (pad, extra))
    return out


def _table(node):
    rows = _find(node, {"tr"})
    out = []
    for i, row in enumerate(rows):
        cells = [c for c in row["children"] if c["tag"] in ("td", "th")]
        texts = [_clean(_inline(c)).replace("|", "\\|") for c in cells]
        if not texts:
            continue
        out.append("| " + " | ".join(texts) + " |")
        if i == 0:
            out.append("|" + "---|" * len(texts))
    return out


def _blocks(node, depth=0):
    out, buf = [], []

    def flush():
        text = _clean("".join(buf))
        buf[:] = []
        if text:
            out.append(text)

    for child in node["children"]:
        tag = child["tag"]
        if tag in DROP:
            continue
        if tag in INLINE:
            buf.append(_inline(child))
            continue
        flush()
        if _is_footnotes(child):
            out.extend(_footnote_blocks(child))
        elif tag in HEADINGS:
            text = _clean(_inline(child))
            whole = re.fullmatch(r"(\*\*|\*)([^*]+)\1", text)
            if whole:
                text = whole.group(2).strip()
            if text:
                out.append("#" * HEADINGS[tag] + " " + text)
        elif tag == "p":
            text = _clean(_inline(child))
            if text:
                out.append(text)
        elif tag in ("ul", "ol"):
            out.extend(_list(child, tag == "ol", depth))
        elif tag == "blockquote":
            for block in _blocks(child, depth):
                out.extend("> " + l for l in block.split("\n"))
        elif tag == "pre":
            out.append("```\n%s\n```" % html_module.unescape(_raw_text(child)).strip("\n"))
        elif tag == "table":
            out.extend(_table(child))
        elif tag == "hr":
            out.append("---")
        elif tag == "figcaption":
            text = _clean(_inline(child))
            if text:
                out.append("*%s*" % text)
        else:
            out.extend(_blocks(child, depth))
    flush()
    return [b for b in out if b.strip()]


def _raw_text(node):
    if node["tag"] == "#text":
        return node.get("text", "")
    return "".join(_raw_text(c) for c in node["children"])


def html_to_markdown(html):
    dom = _Dom()
    dom.feed(html or "")
    root = dom.root
    body = choose_body(root)
    blocks = _blocks(body)
    # footnote lists outside the body still belong to the article
    if not any(b.startswith("[^") and "]:" in b for b in blocks):
        for fn in [n for n in _find(root, set(_all_tags(root))) if _is_footnotes(n)]:
            blocks.extend(_footnote_blocks(fn))
            break
    if not any(b.startswith("# ") for b in blocks):
        title = None
        m = re.search(r"<meta[^>]+property=[\"']og:title[\"'][^>]+content=[\"']([^\"']+)", html or "", re.IGNORECASE)
        if m:
            title = html_module.unescape(m.group(1)).strip()
        title = title or title_from_html(html)
        if title:
            blocks.insert(0, "# " + title)
    md = "\n\n".join(blocks)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    # list items belong together: no blank line between consecutive items
    md = re.sub(r"(?m)^(\s*(?:[-*+]|\d+\.) .*)\n\n(?=\s*(?:[-*+]|\d+\.) )", r"\1\n", md)
    md = re.sub(r"(?m)^(> .*)\n\n(?=> )", r"\1\n>\n", md)
    return md


def _all_tags(node, seen=None):
    seen = set() if seen is None else seen
    seen.add(node["tag"])
    for c in node["children"]:
        _all_tags(c, seen)
    return seen


def extract(source, out_path):
    src = str(source)
    origin = None
    if re.match(r"^https?://", src, re.IGNORECASE):
        result = fetch_text(src)
        if result["status"] != "ok":
            die("could not fetch %s: %s (%s)" % (src, result["status"], result["note"]))
        if not result.get("html"):
            md = result["text"].strip() + "\n"
            kind = "url-text"
        else:
            md = html_to_markdown(result["html"])
            kind = "url-html"
        origin = result.get("final_url") or src
    else:
        p = Path(src)
        raw = read_text(p, "source file")
        if p.suffix.lower() in (".html", ".htm") or re.match(r"^\s*(<!doctype html|<html)", raw[:500], re.IGNORECASE):
            md = html_to_markdown(raw)
            kind = "html-file"
        else:
            md = re.sub(r"\n{3,}", "\n\n", raw).strip() + "\n"
            kind = "markdown-file"
        origin = str(p.resolve())
    if not re.sub(r"\s+", "", md):
        die("no article text found in %s" % src)
    write_text(out_path, md)
    lines = md.split("\n")
    return {"source": src, "origin": origin, "kind": kind, "out": str(out_path),
            "title": next((l[2:] for l in lines if l.startswith("# ")), None),
            "words": count_words(md),
            "headings": sum(1 for l in lines if re.match(r"^#{1,6} ", l)),
            "links": len(re.findall(r"(?<!!)\[[^\]]*\]\([^)]+\)", md)),
            "images": len(re.findall(r"!\[[^\]]*\]\([^)]*\)", md)),
            "footnotes": len(re.findall(r"(?m)^\[\^[^\]]+\]:", md))}
