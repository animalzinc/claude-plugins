#!/usr/bin/env python3
"""mdview: render a markdown file into a self-contained HTML reading view and open it.

Pure stdlib. Reads template.html + assets/marked.min.js (both alongside this file),
injects the markdown as a safely-escaped JS string, writes one self-contained file to
~/.cache/mdview/<hash>.html (deterministic per source path, so localStorage persists),
and opens it in the default browser.

Usage: python3 generate.py <path-to.md> [--browser <AppName>] [--no-open] [--print-path]
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
CACHE = Path.home() / ".cache" / "mdview"

# Local images get inlined as data URIs so the generated HTML is fully
# self-contained and images survive "Copy as rich text" into other apps.
MAX_INLINE_IMG = 4 * 1024 * 1024  # per image; larger ones fall back to <base>-relative loading
IMG_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
            ".webp": "image/webp", ".svg": "image/svg+xml", ".avif": "image/avif", ".bmp": "image/bmp"}
MD_IMG = re.compile(r'!\[([^\]]*)\]\(\s*([^)\s]+)(\s+"[^"]*")?\s*\)')
HTML_IMG = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(")')
FENCE = re.compile(r"^\s{0,3}(```|~~~)")


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


def build(md_path: Path) -> Path:
    src = Path(md_path).expanduser().resolve()
    if not src.is_file():
        sys.exit(f"mdview: not a file: {src}")

    md = inline_images(src.read_text(encoding="utf-8"), src.parent)
    tpl = TEMPLATE.read_text(encoding="utf-8")
    marked = MARKED.read_text(encoding="utf-8")

    # Markdown -> a valid JS string literal. json.dumps handles quotes/newlines/unicode.
    # The extra replace neutralizes a literal "</script>" (or any "</") in the content
    # that would otherwise close the host <script> tag. "<\/" is still valid JSON/JS.
    payload = json.dumps(md).replace("</", "<\\/")

    # Relative images/links resolve against the *source* dir even though the HTML lives
    # in the cache dir. as_uri() percent-encodes spaces/unicode correctly.
    base_href = src.parent.as_uri() + "/"

    # str.replace only (never re.sub): the marked blob and JSON contain backslashes that
    # re.sub would interpret in the replacement string.
    out = tpl
    out = out.replace("/*__MARKED_JS__*/", marked)
    out = out.replace("__MDVIEW_MARKDOWN_JSON__", payload)
    out = out.replace("__MDVIEW_SOURCE_PATH__", json.dumps(str(src)))
    out = out.replace("__MDVIEW_BASE_HREF__", html.escape(base_href, quote=True))
    out = out.replace("__MDVIEW_TITLE__", html.escape(src.name))

    CACHE.mkdir(parents=True, exist_ok=True)
    dst = CACHE / (hashlib.sha1(str(src).encode()).hexdigest()[:16] + ".html")
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
    ap.add_argument("file", help="path to a .md file")
    ap.add_argument("--browser", help="open in a specific app, e.g. Dia (macOS only; default: system default)")
    ap.add_argument("--no-open", action="store_true", help="build but do not open")
    ap.add_argument("--print-path", action="store_true", help="print the output HTML path")
    args = ap.parse_args()

    dst = build(args.file)

    if not args.no_open:
        open_in_browser(dst, args.browser)

    if args.print_path or args.no_open:
        print(dst)


if __name__ == "__main__":
    main()
