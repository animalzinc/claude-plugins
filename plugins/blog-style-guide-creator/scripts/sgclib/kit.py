"""kit-candidates: saved brand kit JSON into candidate rules, kit text verbatim.

Reads every *.json in the kit folder. Each file is one saved kit read, either
the kit object itself or wrapped as {"data": {...}}. Fields used:
    id, brand_name / name                  the kit
    updated_at                             the kit's last change, for freshness checks
    writing_persona, writing_tone          one voice candidate each
    writing_rules: [{id, text}]            one candidate per global rule
    content_types: [{id, name, header_case?, writing_rules: [{id, text}]}]
                                           rules scoped to that content type
"""
import re
from pathlib import Path

from .common import die, read_json, rule_id_from, slugify

MUST_RE = re.compile(r"\b(always|never|must|do not|don't|no exceptions)\b", re.IGNORECASE)


def _kind(text):
    t = text.lower()
    if re.search(r"\b(voice|tone|persona|sound|personality|warm|formal|casual)\b", t):
        return "voice"
    if re.search(r"\b(heading|headline|title|intro|introduction|conclusion|section|structure|"
                 r"paragraph|outline|cta|call to action)\b", t):
        return "structure"
    if re.search(r"\b(comma|dash|hyphen|capitali[sz]|punctuation|numeral|percent|quotation|"
                 r"apostrophe|ampersand|abbreviat)\w*", t):
        return "mechanical"
    return "usage"


def _title(text, words=8):
    first = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    parts = first.split()
    out = " ".join(parts[:words]).rstrip(".,;:")
    return out + ("..." if len(parts) > words else "")


def _unwrap(data):
    if isinstance(data, dict) and isinstance(data.get("data"), dict):
        return data["data"]
    if isinstance(data, dict) and isinstance(data.get("brand_kit"), dict):
        return data["brand_kit"]
    return data


def _heading_case_check(value):
    v = str(value or "").lower()
    if "sentence" in v:
        return "sentence"
    if "title" in v:
        return "title"
    return None


def kit_candidates(kit_dir):
    folder = Path(kit_dir)
    if not folder.is_dir():
        die("kit folder not found: %s" % folder)
    files = sorted(folder.glob("*.json"))
    if not files:
        die("no saved kit reads (*.json) in %s" % folder)
    kit_id, brand, updated_at, cands, content_types, seen = None, None, None, [], [], set()

    def add(cand):
        if cand["source"] in seen:
            return
        seen.add(cand["source"])
        cands.append(cand)

    for path in files:
        data = _unwrap(read_json(path, "kit read"))
        if not isinstance(data, dict):
            die("%s does not hold a kit object" % path)
        kit_id = kit_id or data.get("id")
        updated_at = updated_at or data.get("updated_at")
        brand = brand or data.get("brand_name") or data.get("name")
        for field, title in (("writing_persona", "Writing persona"), ("writing_tone", "Writing tone")):
            text = data.get(field)
            if isinstance(text, str) and text.strip():
                add({"id": "KIT-" + rule_id_from(field.replace("writing_", "")), "title": title,
                     "section": "Voice and tone", "kind": "voice", "severity": "should",
                     "scope": "all", "source": "kit:%s" % field.replace("writing_", ""),
                     "evidence": "Brand kit field %s" % field, "text": text.strip(),
                     "kit_field": field, "file": path.name})
        for rule in data.get("writing_rules") or []:
            if not isinstance(rule, dict) or not (rule.get("text") or "").strip():
                continue
            rid = str(rule.get("id") or "")
            if not rid:
                die("%s: a writing rule has no id, so a re-import could not update it" % path)
            text = rule["text"].strip()
            add({"id": "KIT-" + rule_id_from(rid), "title": _title(text), "section": "Brand kit rules",
                 "kind": _kind(text), "severity": "must" if MUST_RE.search(text) else "should",
                 "scope": "all", "source": "kit:%s" % rid,
                 "evidence": "Brand kit global writing rule %s" % rid, "text": text,
                 "kit_field": "writing_rules", "file": path.name})
        for ct in data.get("content_types") or []:
            if not isinstance(ct, dict) or not ct.get("name"):
                continue
            slug = slugify(ct["name"])
            if slug not in content_types:
                content_types.append(slug)
            case = _heading_case_check(ct.get("header_case"))
            if case:
                cid = str(ct.get("id") or slug)
                add({"id": "KIT-" + rule_id_from("%s-headings" % slug), "title": "%s headings in %s case"
                     % (ct["name"], case), "section": "Brand kit rules", "kind": "mechanical",
                     "severity": "must", "scope": [slug], "source": "kit:%s:header_case" % cid,
                     "evidence": "Brand kit content type %s, header_case" % ct["name"],
                     "text": str(ct.get("header_case")), "check": "heading-case",
                     "params": {"case": case}, "kit_field": "content_types.header_case", "file": path.name})
            for rule in ct.get("writing_rules") or []:
                if not isinstance(rule, dict) or not (rule.get("text") or "").strip():
                    continue
                rid = str(rule.get("id") or "")
                if not rid:
                    die("%s: a rule of content type %s has no id" % (path, ct["name"]))
                text = rule["text"].strip()
                add({"id": "KIT-" + rule_id_from(rid), "title": _title(text),
                     "section": "Brand kit rules: %s" % ct["name"], "kind": _kind(text),
                     "severity": "must" if MUST_RE.search(text) else "should", "scope": [slug],
                     "source": "kit:%s" % rid,
                     "evidence": "Brand kit content type %s, rule %s" % (ct["name"], rid),
                     "text": text, "kit_field": "content_types.writing_rules", "file": path.name})
    return {"kit_id": kit_id, "kit_updated_at": updated_at, "brand": brand, "content_types": content_types,
            "files": [p.name for p in files], "candidates": cands}
