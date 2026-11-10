"""diff-pairs: original and edited drafts into word-level hunks with their sentences.

Two layouts are read:
    <edits>/<pair>/original.md and edited.md     (v2)
    <edits>/original/<name>.md and edited/<name>.md, paired by file name (v1)
"""
import difflib
import re
from pathlib import Path

from .common import die, read_text

TOKEN_RE = re.compile(r"\s+|\w+(?:['’]\w+)*|[^\w\s]")
BOUNDARY_RE = re.compile(r"(?<=[.!?])[\"'”’)\]]*\s+|\n\s*\n|\n(?=#|\s*[-*+] |\s*\d+\. )")


def _sentence(text, pos):
    start, end = 0, len(text)
    for m in BOUNDARY_RE.finditer(text):
        if m.end() <= pos:
            start = m.end()
        elif m.start() >= pos:
            end = m.start()
            break
    return text[start:end].strip()


def _line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def _category(before, after):
    if before.lower() == after.lower() and before != after:
        return "case"
    if re.sub(r"\s+", "", before) == re.sub(r"\s+", "", after):
        return "spacing"
    if re.sub(r"[\W_]+", "", before) == re.sub(r"[\W_]+", "", after):
        return "punctuation"
    return "words"


def diff_texts(original, edited, context_merge=1):
    a = TOKEN_RE.findall(original)
    b = TOKEN_RE.findall(edited)
    a_pos, b_pos = [0], [0]
    for t in a:
        a_pos.append(a_pos[-1] + len(t))
    for t in b:
        b_pos.append(b_pos[-1] + len(t))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = []
    for op in sm.get_opcodes():
        if op[0] == "equal":
            continue
        tag, i1, i2, j1, j2 = op
        before, after = "".join(a[i1:i2]), "".join(b[j1:j2])
        if not before.strip() and not after.strip():
            if re.sub(r"\s+", " ", before) == re.sub(r"\s+", " ", after):
                continue  # line wrapping only
            # spacing around a token (a dash, a slash): show the neighbors too
            i1, j1 = max(0, i1 - 1), max(0, j1 - 1)
            i2, j2 = min(len(a), i2 + 1), min(len(b), j2 + 1)
        if ops and i1 <= ops[-1][2] and j1 <= ops[-1][4]:
            prev = ops[-1]
            ops[-1] = ("replace", prev[1], max(prev[2], i2), prev[3], max(prev[4], j2))
        else:
            ops.append((tag, i1, i2, j1, j2))
    merged = []
    for op in ops:
        if merged and op[1] - merged[-1][2] <= context_merge and all(
                not a[k].strip() for k in range(merged[-1][2], op[1])):
            prev = merged[-1]
            merged[-1] = ("replace", prev[1], op[2], prev[3], op[4])
        else:
            merged.append(op)
    hunks = []
    for tag, i1, i2, j1, j2 in merged:
        before, after = "".join(a[i1:i2]), "".join(b[j1:j2])
        if before == after:
            continue
        op ="insert" if i1 == i2 else "delete" if j1 == j2 else "replace"
        hunks.append({"op": op, "before": before, "after": after,
                      "category": _category(before, after),
                      "line_original": _line_of(original, a_pos[i1]),
                      "line_edited": _line_of(edited, b_pos[j1]),
                      "original_sentence": _sentence(original, a_pos[i1]),
                      "edited_sentence": _sentence(edited, b_pos[j1])})
    return hunks


def find_pairs(edits_dir):
    root = Path(edits_dir)
    if not root.is_dir():
        die("edits folder not found: %s" % root)
    pairs, unpaired = [], []
    o_dir, e_dir = root / "original", root / "edited"
    if o_dir.is_dir() and e_dir.is_dir():
        o = {p.name: p for p in o_dir.iterdir() if p.is_file() and not p.name.startswith(".")}
        e = {p.name: p for p in e_dir.iterdir() if p.is_file() and not p.name.startswith(".")}
        for name in sorted(set(o) & set(e)):
            pairs.append((Path(name).stem, o[name], e[name]))
        unpaired += ["original/" + n for n in sorted(set(o) - set(e))]
        unpaired += ["edited/" + n for n in sorted(set(e) - set(o))]
    for sub in sorted(p for p in root.iterdir() if p.is_dir() and p.name not in ("original", "edited")):
        orig = next((sub / n for n in ("original.md", "original.markdown", "original.txt") if (sub / n).is_file()), None)
        edit = next((sub / n for n in ("edited.md", "edited.markdown", "edited.txt") if (sub / n).is_file()), None)
        if orig and edit:
            pairs.append((sub.name, orig, edit))
        elif orig or edit:
            die("edit pair %s has %s but no %s" % (sub, (orig or edit).name,
                                                   "edited.md" if orig else "original.md"))
    if not pairs:
        die("no edit pairs in %s (expected <pair>/original.md and edited.md, or original/ and edited/)" % root)
    return pairs, unpaired


def diff_pairs(edits_dir):
    pairs, unpaired = find_pairs(edits_dir)
    out, total = [], 0
    for name, o, e in pairs:
        hunks = diff_texts(read_text(o, "original draft"), read_text(e, "edited draft"))
        total += len(hunks)
        cats = {}
        for h in hunks:
            cats[h["category"]] = cats.get(h["category"], 0) + 1
        out.append({"pair": name, "original": str(o), "edited": str(e), "hunks": hunks,
                    "counts": cats})
    return {"pairs": out, "pair_count": len(out), "hunk_count": total, "unpaired": unpaired}
