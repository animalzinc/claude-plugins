"""Guides: parse, validate, render, diff, checklist, v1 indexing, brand paths."""
import difflib
import json
import os
import re
from pathlib import Path

from . import lint as lintmod
from .article import Article
from .common import die, read_json, read_text, slugify
from .yamlish import format_value, parse_block, render_frontmatter, split_frontmatter

ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9-]*$")
RULE_HEADING_RE = re.compile(r"^###[ \t]+([A-Za-z0-9][A-Za-z0-9-]*)[ \t]*:[ \t]*(.+?)[ \t]*$")
SECTION_RE = re.compile(r"^##[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
CHECK_START = "<!-- checklist:start -->"
CHECK_END = "<!-- checklist:end -->"

FIELDS = ("severity", "scope", "kind", "check", "source", "evidence", "audience")
REQUIRED_FIELDS = ("severity", "scope", "kind", "source", "evidence")
SEVERITIES = ("must", "should", "prefer")
KINDS = ("mechanical", "usage", "voice", "structure")
AUDIENCES = ("all", "ai-drafting")
SOURCE_RE = re.compile(r"^(articles|edits|doc|manual|kit:\S+)$")
GOOD, BAD = "✅", "❌"


# ------------------------------------------------------------ document model


def _parse_doc(text, where="guide"):
    """Split a guide into frontmatter, preamble, sections with intro and rules,
    the retired list, and checklist markers. Every rule keeps its raw lines."""
    fm, fm_count, lines = split_frontmatter(text)
    doc = {"frontmatter": fm, "fm_lines": fm_count, "preamble": [], "sections": [],
           "retired": [], "retired_raw": None, "checklist": None}
    section, rule, fence = None, None, None
    for i, line in enumerate(lines):
        n = i + 1 + fm_count
        f = FENCE_RE.match(line)
        if fence:
            if f and f.group(1)[0] == fence[0] and len(f.group(1)) >= len(fence) and not f.group(2).strip():
                fence = None
        elif f:
            fence = f.group(1)
        else:
            if line.strip() == CHECK_START:
                doc["checklist"] = {"start": n, "end": None}
            elif line.strip() == CHECK_END and doc["checklist"]:
                doc["checklist"]["end"] = n
            sm = SECTION_RE.match(line) if not line.startswith("###") else None
            rm = RULE_HEADING_RE.match(line)
            if sm:
                section = {"title": sm.group(1).strip(), "line": n, "heading": line,
                           "intro": [], "rules": []}
                doc["sections"].append(section)
                rule = None
                continue
            if rm and section is not None and not _is_retired(section):
                rule = {"id": rm.group(1), "title": rm.group(2), "line": n, "lines": [line]}
                section["rules"].append(rule)
                continue
        if rule is not None:
            rule["lines"].append(line)
        elif section is not None:
            section["intro"].append(line)
        else:
            doc["preamble"].append(line)
    for section in doc["sections"]:
        if _is_retired(section):
            for line in section["intro"]:
                m = re.match(r"^\s*[-*+]\s+`?([A-Za-z0-9][A-Za-z0-9-]*)`?\s*(?::\s*(.*))?$", line)
                if m:
                    doc["retired"].append({"id": m.group(1), "reason": (m.group(2) or "").strip()})
    return doc


def _is_retired(section):
    return section["title"].strip().lower() == "retired"


def _parse_rule(raw, section_title, where):
    """A rule dict from its raw lines, plus a list of problems found."""
    problems = []
    lines = raw["lines"]
    i = 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    fields, block_end = {}, i
    if i < len(lines) and re.match(r"^\s{0,3}```\s*rule\s*$", lines[i]):
        j = i + 1
        while j < len(lines) and not re.match(r"^\s{0,3}```\s*$", lines[j]):
            j += 1
        if j >= len(lines):
            problems.append("rule block never closes")
        try:
            fields = parse_block(lines[i + 1:j], "%s, rule %s" % (where, raw["id"]))
        except Exception as exc:  # SgcError carries the message
            problems.append(str(exc))
            fields = {}
        block_end = j + 1
    else:
        problems.append("no ```rule block after the heading")
    body = "\n".join(lines[block_end:]).strip("\n")
    body = re.sub(r"(?:\n|^)\s*-{3,}\s*$", "", body.rstrip()).rstrip()
    scope = fields.get("scope", None)
    if isinstance(scope, str) and scope != "all":
        scope = [scope]
    params = {k: v for k, v in fields.items() if k not in FIELDS}
    rule = {
        "id": raw["id"],
        "title": raw["title"],
        "section": section_title,
        "line": raw["line"],
        "severity": fields.get("severity"),
        "scope": scope,
        "kind": fields.get("kind"),
        "check": fields.get("check"),
        "params": params,
        "source": fields.get("source"),
        "evidence": fields.get("evidence"),
        "audience": fields.get("audience") or "all",
        "body": body,
        "text": "\n".join(lines).rstrip(),
        "examples": _examples(body),
        "fields": fields,
    }
    return rule, problems


def _examples(body):
    good, bad = [], []
    for line in body.split("\n"):
        s = line.strip().lstrip("-*+ ").strip()
        if s.startswith(GOOD):
            good.append(s[len(GOOD):].strip())
        elif s.startswith(BAD):
            bad.append(s[len(BAD):].strip())
    return {"good": good, "bad": bad}


def schema_version_of(text):
    """2 for a v2 guide, 1 for a numbered v1 guide, None when neither."""
    try:
        fm, _n, _lines = split_frontmatter(text)
    except Exception:
        fm = None
    if fm and str(fm.get("schema_version")) == "2":
        return 2
    if re.search(r"^##\s+\d+\.\s+\S", text, re.MULTILINE) or re.search(
            r"^###\s+\d+\.\d+\s", text, re.MULTILINE):
        return 1
    return None


def parse_guide(text, where="guide"):
    """Parse a v2 guide. Returns (guide dict, problems list)."""
    doc = _parse_doc(text, where)
    problems = []
    rules = []
    for section in doc["sections"]:
        if _is_retired(section):
            continue
        for raw in section["rules"]:
            rule, probs = _parse_rule(raw, section["title"], where)
            rules.append(rule)
            problems.extend("%s (line %d): %s" % (raw["id"], raw["line"], p) for p in probs)
    guide = {
        "schema_version": (doc["frontmatter"] or {}).get("schema_version"),
        "frontmatter": doc["frontmatter"],
        "sections": [s["title"] for s in doc["sections"]],
        "rules": rules,
        "retired": doc["retired"],
        "checklist": doc["checklist"],
    }
    return guide, problems


def load_guide_file(path):
    text = read_text(path, "style guide")
    version = schema_version_of(text)
    if version == 2:
        guide, problems = parse_guide(text, str(path))
        if problems:
            die("the guide has rules that do not parse; run `sgc guide validate %s`: %s"
                % (path, "; ".join(problems[:5])))
        return guide
    if version == 1:
        return index_v1(text)
    die("%s is neither a v2 guide (frontmatter schema_version: 2) nor a numbered v1 guide" % path)


def load_rules(path):
    """A guide (.md, v2 or v1) or a rules JSON (output of `guide parse` or `index-v1`)."""
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = read_json(p, "rules JSON")
        if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
            die("%s must be a JSON object with a rules list" % p)
        return data
    return load_guide_file(p)


# ------------------------------------------------------------ validate


def _example_article(rule, example):
    check = rule.get("check")
    text = example
    if check in ("heading-case", "heading-format") and not text.startswith("#"):
        levels = (rule.get("params") or {}).get("levels") or [2]
        level = levels[0] if isinstance(levels, list) and levels else 2
        text = "#" * int(level) + " " + text
    if check == "bold-label" and not re.match(r"^\s*([-*+]|\d+[.)])\s", text):
        text = "- " + text
    return Article(text)


def validate_guide(text, where="guide"):
    guide, problems = parse_guide(text, where)
    errors, warnings = list(problems), []
    fm = guide["frontmatter"]
    if fm is None:
        errors.append("no frontmatter; a v2 guide opens with --- and schema_version: 2")
        fm = {}
    if str(fm.get("schema_version")) != "2":
        errors.append("frontmatter schema_version must be 2, found %r" % fm.get("schema_version"))
    if not fm.get("brand"):
        errors.append("frontmatter has no brand")
    types = fm.get("content_types")
    if types is None:
        types = []
    if not isinstance(types, list):
        errors.append("frontmatter content_types must be a list")
        types = []
    if "generated" in fm and not (fm["generated"] is False or isinstance(fm["generated"], str)):
        errors.append("frontmatter generated must be false or a sentence naming the source")
    seen = {}
    retired_ids = {r["id"] for r in guide["retired"]}
    for rule in guide["rules"]:
        rid = rule["id"]
        where_r = "%s (line %d)" % (rid, rule["line"])
        if not ID_RE.match(rid):
            errors.append("%s: IDs are uppercase letters, digits, and hyphens" % where_r)
        if rid in seen:
            errors.append("%s: duplicate ID, also on line %d" % (where_r, seen[rid]))
        seen.setdefault(rid, rule["line"])
        if rid in retired_ids:
            errors.append("%s: ID is listed under Retired; retired IDs are never reused" % where_r)
        for field in REQUIRED_FIELDS:
            if rule["fields"] and rule["fields"].get(field) in (None, "", []):
                errors.append("%s: missing field %s" % (where_r, field))
        if not rule["fields"]:
            continue
        if rule["severity"] not in SEVERITIES:
            errors.append("%s: severity must be one of %s, found %r" % (where_r, ", ".join(SEVERITIES), rule["severity"]))
        if rule["kind"] not in KINDS:
            errors.append("%s: kind must be one of %s, found %r" % (where_r, ", ".join(KINDS), rule["kind"]))
        if rule["audience"] not in AUDIENCES:
            errors.append("%s: audience must be all or ai-drafting, found %r" % (where_r, rule["audience"]))
        if rule["source"] and not SOURCE_RE.match(str(rule["source"])):
            errors.append("%s: source must be articles, edits, doc, kit:<id>, or manual, found %r"
                          % (where_r, rule["source"]))
        scope = rule["scope"]
        if isinstance(scope, list):
            for t in scope:
                if t not in types:
                    errors.append("%s: scope %r is not in content_types %s" % (where_r, t, types))
        elif scope not in (None, "all"):
            errors.append("%s: scope must be all or a list of content types" % where_r)
        if rule["check"]:
            params, perrs = lintmod.normalize_params(rule["check"], rule["params"])
            errors.extend("%s: %s" % (where_r, e) for e in perrs)
            if not perrs:
                for ex in rule["examples"]["good"]:
                    hits = lintmod.run_rule(rule, _example_article(rule, ex))
                    if hits:
                        errors.append("%s: the ✅ example %r is flagged by the rule's own check (%s)"
                                      % (where_r, ex, hits[0].get("note")))
                for ex in rule["examples"]["bad"]:
                    if not lintmod.run_rule(rule, _example_article(rule, ex)):
                        warnings.append("%s: the ❌ example %r is not caught by the rule's check"
                                        % (where_r, ex))
        elif rule["params"]:
            errors.append("%s: parameters %s without a check" % (where_r, ", ".join(sorted(rule["params"]))))
    if guide["checklist"] and guide["checklist"]["end"] is None:
        errors.append("checklist start marker without an end marker")
    return {"valid": not errors, "rules": len(guide["rules"]), "retired": len(guide["retired"]),
            "errors": errors, "warnings": warnings}


# ------------------------------------------------------------ render


def render_rule(rule):
    block = rule.get("block") or {}
    order = ["severity", "scope", "kind", "check"]
    keys = [k for k in order if k in block]
    keys += [k for k in block if k not in order and k not in ("source", "evidence", "audience")]
    keys += [k for k in ("source", "evidence") if k in block]
    if block.get("audience") not in (None, "all"):
        keys.append("audience")
    lines = ["### %s: %s" % (rule["id"], rule["title"]), "```rule"]
    for k in keys:
        if block[k] is None:
            continue
        lines.append("%s: %s" % (k, format_value(block[k])))
    lines.append("```")
    body = (rule.get("body") or "").strip("\n")
    if body:
        lines.append(body)
    return "\n".join(lines)


def _rule_signature(rule_dict):
    """Comparable form of a parsed or proposed rule: title, block fields, body."""
    if "block" in rule_dict:
        block = {k: v for k, v in rule_dict["block"].items() if v is not None}
        body = (rule_dict.get("body") or "").strip()
    else:
        block = dict(rule_dict["fields"])
        body = (rule_dict.get("body") or "").strip()
    if block.get("audience") == "all":
        block.pop("audience")
    return json.dumps([rule_dict["title"].strip(), block, body], sort_keys=True, ensure_ascii=False)


def _check_proposal(prop):
    if not isinstance(prop, dict):
        die("the proposal must be a JSON object")
    rules = prop.get("rules", [])
    if not isinstance(rules, list):
        die("proposal.rules must be a list")
    for i, r in enumerate(rules):
        if not isinstance(r, dict):
            die("proposal.rules[%d] must be an object" % i)
        for key in ("id", "title", "block"):
            if not r.get(key):
                die("proposal.rules[%d] has no %s" % (i, key))
        if not ID_RE.match(r["id"]):
            die("proposal.rules[%d]: ID %r is not uppercase letters, digits, and hyphens" % (i, r["id"]))
        if not isinstance(r["block"], dict):
            die("proposal.rules[%d].block must be an object" % i)
    retire = prop.get("retire", [])
    if not isinstance(retire, list) or not all(isinstance(x, dict) and x.get("id") for x in retire):
        die("proposal.retire must be a list of {\"id\", \"reason\"} objects")
    ids = [r["id"] for r in rules]
    dupes = sorted({x for x in ids if ids.count(x) > 1})
    if dupes:
        die("the proposal lists these IDs twice: %s" % ", ".join(dupes))
    return rules, retire


def _checklist_body(rules):
    out = []
    for sev, label in (("must", "Must"), ("should", "Should"), ("prefer", "Prefer")):
        chosen = [r for r in rules if r.get("severity") == sev]
        if not chosen:
            continue
        out.append("**%s:**" % label)
        out.append("")
        for r in chosen:
            scope = r.get("scope")
            suffix = " (%s)" % ", ".join(scope) if isinstance(scope, list) else ""
            out.append("- [ ] %s: %s%s" % (r["id"], r["title"], suffix))
        out.append("")
    return "\n".join(out).rstrip("\n")


KIT_KEEP = ("severity", "scope", "kind", "check", "audience")


def _merge_kit_rules(proposal, doc):
    """A proposal rule whose source names a kit rule already in the existing
    guide takes that rule's ID, and its kind, severity, scope, check, params,
    and audience wherever the proposal leaves them unset. Returns the IDs matched."""
    if not doc or not isinstance(proposal.get("rules"), list):
        return {}
    by_source = {}
    for s in doc["sections"]:
        if _is_retired(s):
            continue
        for raw in s["rules"]:
            parsed, _p = _parse_rule(raw, s["title"], "existing guide")
            src = str(parsed["fields"].get("source") or "")
            if src.startswith("kit:"):
                by_source[src] = parsed
    matched = {}
    for r in proposal["rules"]:
        if not isinstance(r, dict) or not isinstance(r.get("block"), dict):
            continue
        src = str(r["block"].get("source") or "")
        old = by_source.get(src)
        if not old:
            continue
        if r.get("id") and r["id"] != old["id"]:
            matched[old["id"]] = r["id"]
        else:
            matched[old["id"]] = old["id"]
        r["id"] = old["id"]
        block = dict(r["block"])
        for key in KIT_KEEP:
            if block.get(key) is None and old["fields"].get(key) is not None:
                block[key] = old["fields"][key]
        if block.get("check") == old["fields"].get("check"):
            for key, value in old["params"].items():
                block.setdefault(key, value)
        if not r.get("title"):
            r["title"] = old["title"]
        r["block"] = block
    return matched


def render(proposal, existing_text=None):
    doc = _parse_doc(existing_text) if existing_text else None
    kit_matched = _merge_kit_rules(proposal, doc)
    rules, retire = _check_proposal(proposal)
    fm = dict(doc["frontmatter"] or {}) if doc else {}
    fm.update(proposal.get("frontmatter") or {})
    fm.setdefault("schema_version", 2)
    if not fm.get("brand"):
        die("the proposal has no frontmatter.brand and there is no existing guide to take it from")

    # sections: [title, intro text, [rule text or rule dict]]
    sections, existing_rules = [], {}
    retired = list(doc["retired"]) if doc else []
    retired_ids = {r["id"] for r in retired}
    preamble = None
    checklist_heading = None
    if doc:
        preamble = "\n".join(doc["preamble"]).strip("\n")
        for s in doc["sections"]:
            if _is_retired(s):
                continue
            intro = "\n".join(s["intro"]).strip("\n")
            if CHECK_START in intro:
                checklist_heading = s["heading"]
                continue
            entry = {"title": s["title"], "heading": s["heading"], "intro": intro, "rules": []}
            for raw in s["rules"]:
                parsed, _p = _parse_rule(raw, s["title"], "existing guide")
                existing_rules[raw["id"]] = (entry, parsed)
                entry["rules"].append({"id": raw["id"], "text": parsed["text"], "parsed": parsed})
            sections.append(entry)
    by_title = {s["title"]: s for s in sections}

    def section_for(title):
        if title not in by_title:
            entry = {"title": title, "heading": "## " + title, "intro": "", "rules": []}
            sections.append(entry)
            by_title[title] = entry
        return by_title[title]

    report = {"added": [], "changed": [], "unchanged": [], "retired": [],
              "kit_matched": sorted(kit_matched)}
    proposed_ids = set()
    for r in rules:
        rid = r["id"]
        proposed_ids.add(rid)
        if rid in retired_ids:
            die("proposal rule %s reuses a retired ID; retired IDs are never reused" % rid)
        if rid in existing_rules:
            entry, parsed = existing_rules[rid]
            if _rule_signature(parsed) == _rule_signature(r) and (not r.get("section") or r["section"] == entry["title"]):
                report["unchanged"].append(rid)
                continue
            target = section_for(r["section"]) if r.get("section") else entry
            item = {"id": rid, "text": render_rule(r)}
            if target is entry:
                entry["rules"] = [item if x["id"] == rid else x for x in entry["rules"]]
            else:
                entry["rules"] = [x for x in entry["rules"] if x["id"] != rid]
                target["rules"].append(item)
            report["changed"].append(rid)
        else:
            if not r.get("section"):
                die("new rule %s has no section" % rid)
            section_for(r["section"])["rules"].append({"id": rid, "text": render_rule(r)})
            report["added"].append(rid)

    to_retire = list(retire)
    if proposal.get("complete"):
        for rid in existing_rules:
            if rid not in proposed_ids and rid not in [x["id"] for x in to_retire]:
                to_retire.append({"id": rid, "reason": "not in the approved proposal"})
    for item in to_retire:
        rid = item["id"]
        if rid in proposed_ids:
            die("rule %s is both proposed and retired" % rid)
        if rid in retired_ids:
            continue
        if rid in existing_rules:
            entry, _parsed = existing_rules[rid]
            entry["rules"] = [x for x in entry["rules"] if x["id"] != rid]
        elif doc:
            die("cannot retire %s: no such rule in the existing guide" % rid)
        retired.append({"id": rid, "reason": item.get("reason") or ""})
        retired_ids.add(rid)
        report["retired"].append(rid)

    # assemble
    out = [render_frontmatter(fm), ""]
    if preamble:
        out += [preamble, ""]
    else:
        out += ["# %s" % (proposal.get("title") or "%s style guide" % fm["brand"]), ""]
        if proposal.get("intro"):
            out += [proposal["intro"].strip(), ""]
    all_rules_for_checklist = []
    for s in sections:
        if not s["rules"] and not s["intro"]:
            continue
        out.append(s["heading"])
        out.append("")
        if s["intro"]:
            out += [s["intro"], ""]
        for item in s["rules"]:
            out += [item["text"], ""]
    text_so_far = "\n".join(out)
    parsed_now, _ = parse_guide(text_so_far + "\n")
    all_rules_for_checklist = parsed_now["rules"]
    out.append(checklist_heading or "## Quick reference checklist")
    out += ["", CHECK_START, _checklist_body(all_rules_for_checklist), CHECK_END, ""]
    if retired:
        out += ["## Retired", ""]
        for r in retired:
            out.append("- %s%s" % (r["id"], ": " + r["reason"] if r.get("reason") else ""))
        out.append("")
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).rstrip("\n") + "\n"
    return text, report


# ------------------------------------------------------------ checklist


def write_checklist(text):
    """Return (new text, markers_added)."""
    guide, problems = parse_guide(text)
    if problems:
        die("the guide has rules that do not parse: %s" % "; ".join(problems[:5]))
    body = _checklist_body(guide["rules"])
    lines = text.rstrip("\n").split("\n")
    starts = [i for i, l in enumerate(lines) if l.strip() == CHECK_START]
    ends = [i for i, l in enumerate(lines) if l.strip() == CHECK_END]
    if len(starts) > 1 or len(ends) > 1:
        die("the guide has more than one checklist marker pair")
    if starts and ends and ends[0] > starts[0]:
        new = lines[:starts[0] + 1] + body.split("\n") + lines[ends[0]:]
        return "\n".join(new) + "\n", False
    if starts or ends:
        die("the guide has only one of the checklist markers")
    block = ["## Quick reference checklist", "", CHECK_START] + body.split("\n") + [CHECK_END, ""]
    retired_at = next((i for i, l in enumerate(lines) if re.match(r"^##\s+Retired\s*$", l, re.IGNORECASE)), None)
    if retired_at is None:
        new = lines + [""] + block
    else:
        new = lines[:retired_at] + block + lines[retired_at:]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(new)).rstrip("\n") + "\n", True


# ------------------------------------------------------------ diff


def diff_guides(old_text, new_text):
    old, p1 = parse_guide(old_text, "old guide")
    new, p2 = parse_guide(new_text, "new guide")
    if p1 or p2:
        die("a guide does not parse: %s" % "; ".join((p1 + p2)[:5]))
    old_rules = {r["id"]: r for r in old["rules"]}
    new_rules = {r["id"]: r for r in new["rules"]}
    new_retired = {r["id"]: r for r in new["retired"]}
    old_retired = {r["id"] for r in old["retired"]}
    out = {"frontmatter": {}, "added": [], "changed": [], "modified": [], "retired": [],
           "deleted": [], "unchanged": 0}
    for key in sorted(set(old["frontmatter"] or {}) | set(new["frontmatter"] or {})):
        a, b = (old["frontmatter"] or {}).get(key), (new["frontmatter"] or {}).get(key)
        if a != b:
            out["frontmatter"][key] = [a, b]
    for rid, r in new_rules.items():
        if rid not in old_rules:
            out["added"].append({"id": rid, "title": r["title"], "section": r["section"],
                                 "severity": r["severity"], "text": r["text"]})
    for rid, r in old_rules.items():
        if rid in new_rules:
            n = new_rules[rid]
            fields = {}
            for k in sorted(set(r["fields"]) | set(n["fields"])):
                if r["fields"].get(k) != n["fields"].get(k):
                    fields[k] = [r["fields"].get(k), n["fields"].get(k)]
            if r["title"] != n["title"]:
                fields["title"] = [r["title"], n["title"]]
            if r["section"] != n["section"]:
                fields["section"] = [r["section"], n["section"]]
            body_diff = list(difflib.unified_diff(r["body"].split("\n"), n["body"].split("\n"),
                                                  "old", "new", lineterm="", n=1))
            if fields or body_diff:
                entry = {"id": rid, "title": n["title"], "fields": fields,
                         "body_diff": "\n".join(body_diff[2:])}
                is_kit = str(n["fields"].get("source") or "").startswith("kit:")
                text_changed = bool(body_diff) or "title" in fields
                out["modified" if is_kit and text_changed else "changed"].append(entry)
            else:
                out["unchanged"] += 1
        elif rid in new_retired:
            out["retired"].append({"id": rid, "title": r["title"], "reason": new_retired[rid]["reason"]})
        else:
            out["deleted"].append({"id": rid, "title": r["title"]})
    for rid in new_retired:
        if rid not in old_rules and rid not in old_retired:
            out["retired"].append({"id": rid, "title": None, "reason": new_retired[rid]["reason"]})
    return out


def diff_markdown(d):
    lines = []
    if d["frontmatter"]:
        lines.append("Frontmatter:")
        for k, (a, b) in d["frontmatter"].items():
            lines.append("- %s: %s -> %s" % (k, json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False)))
        lines.append("")
    for label, key in (("Added", "added"), ("Changed", "changed"),
                       ("Modified kit rules", "modified"), ("Retired", "retired"),
                       ("Deleted without retiring", "deleted")):
        if not d[key]:
            continue
        lines.append("%s (%d):" % (label, len(d[key])))
        for item in d[key]:
            lines.append("- %s: %s" % (item["id"], item.get("title") or ""))
            for f, (a, b) in (item.get("fields") or {}).items():
                lines.append("  - %s: %s -> %s" % (f, json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False)))
            if item.get("body_diff"):
                lines += ["    " + l for l in item["body_diff"].split("\n")]
            if item.get("reason"):
                lines.append("  - reason: %s" % item["reason"])
        lines.append("")
    lines.append("Unchanged: %d" % d["unchanged"])
    return "\n".join(lines)


# ------------------------------------------------------------ v1


def _v1_kind(*titles):
    text = " ".join(t.lower() for t in titles if t)
    if re.search(r"voice|tone|persona|personality|person\b|formality", text):
        return "voice"
    if re.search(r"punctuation|mechanic|format|capitali|number|dash|comma|quotation|hyphen|abbreviation", text):
        return "mechanical"
    if re.search(r"structure|organi[sz]ation|heading|paragraph|list|seo|citation|attribution|link|"
                 r"content pattern|principle|intro|conclusion|template", text):
        return "structure"
    return "usage"


SKIP_V1 = re.compile(r"quick reference|checklist|table of contents|^contents$", re.IGNORECASE)


def index_v1(text):
    """Read a v1 guide's subsections as rules V1-N.M (and V1-N.M.K)."""
    lines = text.replace("\r\n", "\n").split("\n")
    rules = []
    sec_num, sec_title, sub_count = None, None, 0
    current, fence = None, None
    skipping = False

    def close():
        if current:
            body = "\n".join(current["lines"][1:]).strip()
            body = re.sub(r"\n-{3,}\s*$", "", body).strip()
            current["text"] = "\n".join(current["lines"]).rstrip()
            current["body"] = body
            severity = "must" if re.search(r"\b(always|never|no exceptions)\b", body + " " + current["title"],
                                           re.IGNORECASE) else "should"
            current["severity"] = severity
            del current["lines"]
            rules.append(current)

    for i, line in enumerate(lines):
        f = FENCE_RE.match(line)
        if fence:
            if f and f.group(1)[0] == fence[0] and not f.group(2).strip():
                fence = None
            if current:
                current["lines"].append(line)
            continue
        if f:
            fence = f.group(1)
            if current:
                current["lines"].append(line)
            continue
        h2 = re.match(r"^##\s+(?:(\d+)\.?\s+)?(.+?)\s*$", line) if not line.startswith("###") else None
        h3 = re.match(r"^(#{3,4})\s+(?:(\d+(?:\.\d+)*)\.?\s+)?(.+?)\s*$", line)
        if h2:
            close()
            current = None
            sec_num = h2.group(1)
            sec_title = h2.group(2)
            sub_count = 0
            skipping = bool(SKIP_V1.search(sec_title)) or sec_num is None
            continue
        if h3 and not skipping and sec_num is not None:
            level, number, title = len(h3.group(1)), h3.group(2), h3.group(3)
            if level == 4 and not number:
                if current:
                    current["lines"].append(line)
                continue
            close()
            if not number:
                sub_count += 1
                number = "%s.%d" % (sec_num, sub_count)
            rid = "V1-" + number
            current = {"id": rid, "title": title, "section": "%s. %s" % (sec_num, sec_title),
                       "line": i + 1, "severity": None, "scope": "all",
                       "kind": _v1_kind(title, sec_title), "check": None, "params": {},
                       "source": "manual", "evidence": "", "audience": "all",
                       "lines": [line]}
            continue
        if current is not None:
            current["lines"].append(line)
    close()
    for r in rules:
        r["examples"] = _examples(r["body"])
        r["fields"] = {}
    title = next((re.sub(r"^#\s+", "", l) for l in lines if l.startswith("# ")), None)
    return {"schema_version": 1, "frontmatter": {"brand": title, "content_types": []},
            "sections": sorted({r["section"] for r in rules}), "rules": rules, "retired": [],
            "checklist": None}


# ------------------------------------------------------------ brand-path


def brand_path(brand, guides_dir=None, project_dir=None, guide=None):
    out = {"brand": brand, "guides_dir": None, "guides_dir_source": None, "ignored_guides_dir": None}
    if guides_dir:
        p = Path(guides_dir)
        if "${" in guides_dir:
            out["ignored_guides_dir"] = {"value": guides_dir, "reason": "unresolved variable"}
        elif not p.is_absolute():
            out["ignored_guides_dir"] = {"value": guides_dir, "reason": "not an absolute path"}
        elif not p.is_dir():
            out["ignored_guides_dir"] = {"value": guides_dir, "reason": "folder does not exist"}
        else:
            out["guides_dir"], out["guides_dir_source"] = str(p), "--guides-dir"
    if out["guides_dir"] is None:
        proj = project_dir or os.environ.get("CLAUDE_PROJECT_DIR")
        if proj and "${" in proj:
            proj = None
        source = "--project-dir" if project_dir else ("CLAUDE_PROJECT_DIR" if proj else "working directory")
        base = Path(proj) if proj else Path.cwd()
        out["guides_dir"], out["guides_dir_source"] = str(base / "brands"), source + "/brands"
    gd = Path(out["guides_dir"])
    candidates = [gd / brand, gd / slugify(brand)]
    brand_dir = next((c for c in candidates if c.is_dir()), candidates[0])
    out["brand_dir"] = str(brand_dir)
    out["brand_dir_exists"] = brand_dir.is_dir()
    if guide:
        gp = Path(guide)
        if not gp.is_file():
            die("--guide file not found: %s" % gp)
        out["guide_source"] = "--guide"
    else:
        gp = brand_dir / "style-guide.md"
        out["guide_source"] = "brand folder"
    out["guide"] = str(gp)
    out["guide_exists"] = gp.is_file()
    out["schema_version"] = schema_version_of(read_text(gp, "guide")) if gp.is_file() else None
    out["decisions"] = str(brand_dir / "decisions.jsonl")
    out["decisions_exists"] = (brand_dir / "decisions.jsonl").is_file()
    out["sources_dir"] = str(brand_dir / "sources")
    out["v1_guide_backup"] = str(brand_dir / "style-guide.v1.md")
    return out
