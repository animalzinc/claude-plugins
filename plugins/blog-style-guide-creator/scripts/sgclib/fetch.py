"""fetch: save a page's text and metadata under a hash of its URL, keep index.json current.

Files in the output folder:
    <sha1>.txt   the page as plain text, only when the fetch succeeded
    <sha1>.json  url, final_url, status, http_status, content_type, title,
                 fetched_at, chars, blocked, note, text_file, html_file
    <sha1>.html  the raw HTML, when the page was HTML (for `extract`)
    index.json   normalized url -> sha1, for the requested and the final url
A failed refetch deletes the text an earlier fetch saved, so no excerpt is
checked against a page the latest fetch did not read.
"""
import hashlib
import html as html_module
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from .common import die, now_iso

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
TIMEOUT = 20
HEAD_CHARS = 3000
CHALLENGE_MARKERS = ("cloudflare", "enable javascript", "access denied", "captcha")
CHALLENGE_MAX_CHARS = 2000
READABLE_TYPES = ("text/html", "application/xhtml", "text/plain", "text/markdown",
                  "application/json", "xml")
_BLOCK = ("p", "div", "br", "li", "ul", "ol", "tr", "table", "section", "article", "h1", "h2",
          "h3", "h4", "h5", "h6", "blockquote", "pre", "header", "footer", "main", "aside",
          "figure", "figcaption", "td", "th", "dd", "dt")


def normalize_url(url):
    """Drop the scheme, lowercase the host, drop a trailing slash and utm parameters."""
    raw = (url or "").strip()
    if not raw:
        return ""
    parts = urllib.parse.urlsplit(raw if "://" in raw else "http://" + raw.lstrip("/"))
    host = (parts.netloc or "").lower()
    path = parts.path or ""
    if path.endswith("/") and len(path) > 1:
        path = path[:-1]
    if path == "/":
        path = ""
    query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith("utm_")]
    out = host + path
    if query:
        out += "?" + urllib.parse.urlencode(query)
    return out


def url_key(url):
    return hashlib.sha1(normalize_url(url).encode("utf-8")).hexdigest()


def html_to_text(html):
    text = html or ""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<(script|style|noscript|template)\b.*?</\1\s*>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<(nav|header|footer|aside|form)\b.*?</\1\s*>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    closers = "|".join(_BLOCK)
    text = re.sub(r"</(%s)\s*>" % closers, "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<(%s)\b[^>]*>" % closers, "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_module.unescape(text).replace(" ", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def title_from_html(html):
    m = re.search(r"<title[^>]*>(.*?)</title>", html or "", re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    return re.sub(r"\s+", " ", html_module.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip() or None


def _decode(body, content_type):
    m = re.search(r"charset=([\w-]+)", content_type or "", re.IGNORECASE)
    for enc in ((m.group(1) if m else None), "utf-8", "latin-1"):
        if not enc:
            continue
        try:
            return body.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return body.decode("utf-8", errors="replace")


def fetch_text(url, opener=None):
    """Fetch one URL. `text` and `html` are None whenever the page could not be read."""
    result = {"status": "error", "url": url, "final_url": None, "http_status": None,
              "content_type": None, "title": None, "fetched_at": now_iso(), "chars": 0,
              "blocked": False, "note": None, "text": None, "html": None}
    request = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"})
    try:
        with (opener or urllib.request.urlopen)(request, timeout=TIMEOUT) as response:
            body = response.read()
            result["final_url"] = response.geturl()
            result["http_status"] = getattr(response, "status", None) or response.getcode()
            result["content_type"] = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        result["http_status"] = exc.code
        result["final_url"] = getattr(exc, "url", url)
        if exc.code == 403:
            result.update(status="blocked", blocked=True, note="HTTP 403, the page refused the fetch")
        else:
            result.update(status="error", note="HTTP %s %s" % (exc.code, exc.reason))
        return result
    except urllib.error.URLError as exc:
        result["note"] = "network error: %s" % (exc.reason,)
        return result
    except Exception as exc:  # timeouts, bad URLs, malformed responses
        result["note"] = "fetch failed: %s" % (exc,)
        return result
    ctype = (result["content_type"] or "").lower()
    if ctype and not any(t in ctype for t in READABLE_TYPES):
        result.update(status="unreadable", note="content type %s is not text" % result["content_type"])
        return result
    if body[:5] == b"%PDF-" or b"\x00" in body[:2048]:
        result.update(status="unreadable", note="body is binary or a PDF")
        return result
    raw = _decode(body, result["content_type"])
    is_html = "html" in ctype or "<html" in raw[:2000].lower()
    text = html_to_text(raw) if is_html else raw.strip()
    lowered = text.lower()
    if len(text) < CHALLENGE_MAX_CHARS and any(m in lowered for m in CHALLENGE_MARKERS):
        hit = next(m for m in CHALLENGE_MARKERS if m in lowered)
        result.update(status="blocked", blocked=True, title=title_from_html(raw),
                      note="bot challenge page (%d characters, mentions '%s')" % (len(text), hit))
        return result
    result.update(status="ok", text=text, chars=len(text), title=title_from_html(raw) if is_html else None,
                  html=raw if is_html else None)
    return result


def rebuild_index(out_dir):
    out = Path(out_dir)
    index = {}
    for meta_path in sorted(out.glob("*.json")):
        if meta_path.name == "index.json":
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not isinstance(meta, dict) or not meta.get("url"):
            continue
        index[normalize_url(meta["url"])] = meta_path.stem
        if meta.get("final_url"):
            index.setdefault(normalize_url(meta["final_url"]), meta_path.stem)
    tmp = out / ("index.json.%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(out / "index.json"))
    return index


def save_fetch(result, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sha = url_key(result["url"])
    ok = result["status"] == "ok"
    meta = {k: result.get(k) for k in ("url", "final_url", "status", "http_status", "content_type",
                                       "title", "fetched_at", "chars", "blocked", "note")}
    meta["text_file"] = "%s.txt" % sha if ok else None
    meta["html_file"] = "%s.html" % sha if ok and result.get("html") else None
    (out / ("%s.json" % sha)).write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for ext, key in (("txt", "text"), ("html", "html")):
        path = out / ("%s.%s" % (sha, ext))
        if ok and result.get(key):
            with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
                handle.write(result[key])
        elif path.exists():
            path.unlink()
    rebuild_index(out)
    return sha


def build_windows(text, terms, window=1500, max_windows=3):
    if not terms:
        return [{"term": None, "text": text[:HEAD_CHARS]}]
    flat = re.sub(r"\s+", " ", text)
    half = max(window // 2, 1)
    windows = []
    for term in terms:
        needle = re.sub(r"\s+", " ", term).strip()
        if not needle:
            continue
        found = 0
        for m in re.finditer(re.escape(needle), flat, re.IGNORECASE):
            if found >= max_windows:
                break
            s, e = max(0, m.start() - half), min(len(flat), m.end() + half)
            windows.append({"term": term, "text": ("..." if s else "") + flat[s:e] + ("..." if e < len(flat) else "")})
            found += 1
        if not found:
            windows.append({"term": term, "text": None, "note": "term not found on the page"})
    return windows


def fetch_cmd(url, out_dir, terms=None, opener=None):
    """Returns (payload, ok)."""
    if not re.match(r"^https?://", url, re.IGNORECASE):
        die("url must start with http:// or https://, got: %s" % url)
    result = fetch_text(url, opener)
    sha = save_fetch(result, out_dir)
    payload = {k: result.get(k) for k in ("url", "final_url", "status", "http_status", "content_type",
                                          "title", "fetched_at", "chars", "blocked", "note")}
    payload.update(sha1=sha, normalized_url=normalize_url(url), out_dir=str(out_dir),
                   text_file="%s.txt" % sha if result["status"] == "ok" else None,
                   windows=build_windows(result["text"], terms or []) if result["status"] == "ok" else [])
    return payload, result["status"] == "ok"
