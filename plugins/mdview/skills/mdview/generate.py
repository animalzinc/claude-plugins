#!/usr/bin/env python3
"""mdview: render a markdown file into a self-contained HTML reading view and open it.

Pure stdlib. Reads template.html + assets/marked.min.js (both alongside this file),
injects the markdown as a safely-escaped JS string, writes one self-contained file to
~/.cache/mdview/<hash>.html (deterministic per source path, so localStorage persists),
and opens it in the default browser.

With --against, a second file is rendered read-only in a left-hand pane so the two can be
read side by side and blocks carried from the reference into the working document.

Usage: python3 generate.py <path-to.md> [--against <other.md>]
                           [--browser <AppName>] [--no-open] [--print-path]
"""
import argparse
import base64
import hashlib
import html
import json
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
TEMPLATE = SKILL_DIR / "template.html"
MARKED = SKILL_DIR / "assets" / "marked.min.js"
MERMAID = SKILL_DIR / "assets" / "mermaid.min.js"
# a ```mermaid fence anywhere in the document triggers injecting mermaid.min.js (~3.4MB),
# so ordinary documents stay small
MERMAID_FENCE = re.compile(r"^\s{0,3}(?:```|~~~)\s*mermaid\b", re.MULTILINE)
CACHE = Path.home() / ".cache" / "mdview"

# Local images get inlined as data URIs so the generated HTML is fully
# self-contained and images survive "Copy as rich text" into other apps.
MAX_INLINE_IMG = 4 * 1024 * 1024  # per image; larger ones fall back to <base>-relative loading
IMG_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
            ".webp": "image/webp", ".svg": "image/svg+xml", ".avif": "image/avif", ".bmp": "image/bmp"}
MD_IMG = re.compile(r'!\[([^\]]*)\]\(\s*([^)\s]+)(\s+"[^"]*")?\s*\)')
HTML_IMG = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(")')
FENCE = re.compile(r"^\s{0,3}(```|~~~)")

# YAML frontmatter is metadata, not prose. Left in the payload, marked renders the
# delimiters as a rule and the fields as one run-on paragraph in the body font, above
# the title. It is split out here and rendered as a key/value card instead.
FM_KEY = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9 _.\-]*):[ \t]*(.*)$")


def split_frontmatter(md: str) -> "tuple[str | None, str]":
    """Return (frontmatter block, body). No frontmatter -> (None, md)."""
    lines = md.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, md
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            block = "\n".join(lines[1:i])
            first = next((l for l in block.splitlines() if l.strip()), "")
            # a doc that merely opens with a thematic break is not frontmatter
            return (block, "\n".join(lines[i + 1:]).lstrip("\n")) if FM_KEY.match(first) else (None, md)
    return None, md  # unterminated: treat as body, don't eat the file


def parse_frontmatter(block: str) -> "list[tuple[str, str]] | None":
    """Tolerant key: value parse. Returns None for anything it can't read flatly,
    so the caller can fall back to showing the block verbatim."""
    pairs: "list[list[str]]" = []
    for line in block.splitlines():
        m = FM_KEY.match(line)
        if m and not line[:1].isspace():
            pairs.append([m.group(1), m.group(2).strip()])
        elif not line.strip():
            continue
        elif pairs:
            cont, val = line.strip(), pairs[-1][1]
            # list items and block scalars keep their line structure; a wrapped
            # plain value is rejoined into one flowing line
            if cont.startswith("-") or val.startswith(("|", ">")) or "\n" in val:
                pairs[-1][1] = (val + "\n" + cont).strip("\n")
            else:
                pairs[-1][1] = (val + " " + cont).strip()
        else:
            return None  # content before any key: not a flat mapping
    return [(k, v) for k, v in pairs] or None


def frontmatter_html(block: str) -> str:
    """A labelled card. Each value is a <p>, so it stays a leaf block the comment
    and inline-edit machinery already handles."""
    e = lambda s: html.escape(s, quote=True)
    pairs = parse_frontmatter(block)
    if pairs is None:
        pairs = [("frontmatter", block.strip())]
    rows = "".join(
        '<dt class="fm-key">%s</dt><dd class="fm-val"><p>%s</p></dd>' % (e(k), e(v) or "&nbsp;")
        for k, v in pairs
    )
    return ('<div class="fm" aria-label="Frontmatter">'
            '<div class="fm-label">Frontmatter</div>'
            '<dl class="fm-list">%s</dl></div>' % rows)


def inline_images(md: str, base: Path) -> str:
    def to_data_uri(url: str):
        if re.match(r"^(https?:|data:|file:|//)", url):
            return None  # remote or already-inlined: leave untouched
        p = urllib.parse.unquote(url)
        f = Path(p).expanduser() if p.startswith(("/", "~")) else base / p
        mime = IMG_MIME.get(f.suffix.lower())
        try:
            if not mime or not f.is_file() or f.stat().st_size > MAX_INLINE_IMG:
                return None
            return "data:%s;base64,%s" % (mime, base64.b64encode(f.read_bytes()).decode())
        except OSError:
            return None

    def sub_md(m):
        uri = to_data_uri(m.group(2))
        return "![%s](%s%s)" % (m.group(1), uri, m.group(3) or "") if uri else m.group(0)

    def sub_html(m):
        uri = to_data_uri(m.group(2))
        return m.group(1) + uri + m.group(3) if uri else m.group(0)

    out, in_fence = [], False
    for line in md.splitlines(keepends=True):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            line = MD_IMG.sub(sub_md, line)
            line = HTML_IMG.sub(sub_html, line)
        out.append(line)
    return "".join(out)


def js_payload(text: str) -> str:
    """Markdown -> a valid JS string literal. json.dumps handles quotes/newlines/unicode.
    The extra replace neutralizes a literal "</script>" (or any "</") in the content
    that would otherwise close the host <script> tag. "<\\/" is still valid JSON/JS."""
    return json.dumps(text).replace("</", "<\\/")


def build(md_path: Path, ref_path: "str | Path | None" = None) -> Path:
    src = Path(md_path).expanduser().resolve()
    if not src.is_file():
        sys.exit(f"mdview: not a file: {src}")

    # Split mode: a second file rendered read-only beside the first, to compare against
    # and carry blocks back from. The working file is always the one passed first.
    ref = Path(ref_path).expanduser().resolve() if ref_path else None
    if ref is not None and not ref.is_file():
        sys.exit(f"mdview: not a file: {ref}")
    if ref is not None and ref == src:
        sys.exit("mdview: --against needs a different file from the one being viewed")

    md = inline_images(src.read_text(encoding="utf-8"), src.parent)
    fm, md = split_frontmatter(md)
    tpl = TEMPLATE.read_text(encoding="utf-8")
    marked = MARKED.read_text(encoding="utf-8")

    payload = js_payload(md)

    # Relative images/links resolve against the *source* dir even though the HTML lives
    # in the cache dir. as_uri() percent-encodes spaces/unicode correctly.
    base_href = src.parent.as_uri() + "/"

    # str.replace only (never re.sub): the marked blob and JSON contain backslashes that
    # re.sub would interpret in the replacement string.
    out = tpl
    out = out.replace("/*__MARKED_JS__*/", marked)
    out = out.replace("__MDVIEW_MARKDOWN_JSON__", payload)
    fm_payload = json.dumps(frontmatter_html(fm) if fm is not None else "").replace("</", "<\\/")
    out = out.replace("__MDVIEW_FRONTMATTER_JSON__", fm_payload)
    out = out.replace("__MDVIEW_SOURCE_PATH__", json.dumps(str(src)))
    out = out.replace("__MDVIEW_BASE_HREF__", html.escape(base_href, quote=True))
    out = out.replace("__MDVIEW_TITLE__", html.escape(src.name if ref is None
                                                     else f"{ref.name} → {src.name}"))

    # Reference pane. Its own local images are inlined against *its* directory, since
    # <base> points at the working file's directory and would not resolve them.
    ref_md = ""
    if ref is None:
        ref_md_payload, ref_fm_payload, ref_path_payload = "null", '""', "null"
    else:
        ref_md = inline_images(ref.read_text(encoding="utf-8"), ref.parent)
        ref_fm, ref_md = split_frontmatter(ref_md)
        ref_md_payload = js_payload(ref_md)
        ref_fm_payload = js_payload(frontmatter_html(ref_fm) if ref_fm is not None else "")
        ref_path_payload = json.dumps(str(ref))
    out = out.replace("__MDVIEW_REF_MARKDOWN_JSON__", ref_md_payload)
    out = out.replace("__MDVIEW_REF_FRONTMATTER_JSON__", ref_fm_payload)
    out = out.replace("__MDVIEW_REF_SOURCE_PATH__", ref_path_payload)
    out = out.replace("__MDVIEW_IS_SPLIT__", "false" if ref is None else "true")

    # mermaid.min.js only rides along when a document actually contains a mermaid fence
    needs_mermaid = bool(MERMAID_FENCE.search(md) or MERMAID_FENCE.search(ref_md))
    mermaid_js = MERMAID.read_text(encoding="utf-8") if needs_mermaid and MERMAID.is_file() else ""
    out = out.replace("/*__MERMAID_JS__*/", mermaid_js)

    # Deterministic per source path (so localStorage persists across regenerations),
    # and per *pair* in split mode, so a split view is its own page.
    key = str(src) if ref is None else str(src) + "||" + str(ref)
    CACHE.mkdir(parents=True, exist_ok=True)
    dst = CACHE / (hashlib.sha1(key.encode()).hexdigest()[:16] + ".html")
    dst.write_text(out, encoding="utf-8")
    return dst


def open_in_browser(dst: Path, browser: "str | None" = None) -> None:
    """Open the built file in a browser. Cross-platform: macOS honors --browser
    (e.g. a specific app); Linux/Windows/other use the OS default browser."""
    if sys.platform == "darwin":
        cmd = ["open", "-a", browser, str(dst)] if browser else ["open", str(dst)]
        subprocess.run(cmd, check=True)
    else:
        import webbrowser
        webbrowser.open(dst.as_uri())


def main() -> None:
    ap = argparse.ArgumentParser(prog="mdview", description="Render markdown and open it.")
    ap.add_argument("file", help="path to a .md file (the working document)")
    ap.add_argument("--against", "--ref", dest="against", metavar="PATH",
                    help="split view: render this file read-only alongside, to compare "
                         "against and carry blocks back from")
    ap.add_argument("--browser", help="open in a specific app, e.g. Chrome (macOS only; default: system default)")
    ap.add_argument("--no-open", action="store_true", help="build but do not open")
    ap.add_argument("--print-path", action="store_true", help="print the output HTML path")
    args = ap.parse_args()

    dst = build(args.file, args.against)

    if not args.no_open:
        open_in_browser(dst, args.browser)

    if args.print_path or args.no_open:
        print(dst)


if __name__ == "__main__":
    main()
