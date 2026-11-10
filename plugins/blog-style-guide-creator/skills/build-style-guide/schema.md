# Guide schema

A guide is one Markdown file, `style-guide.md` in the brand folder. `sgc guide parse` reads it, `sgc guide validate` checks it, and every check reads its rules from it, so the format below is exact.

## File

~~~markdown
---
schema_version: 2
brand: Demo Co
content_types: [essay, how-to, case-study]
generated: false
---

# Demo Co style guide

One or two sentences on what the guide covers.

## Punctuation

### PUNC-EMDASH: Close up em dashes
```rule
severity: must
scope: all
kind: mechanical
check: dash-spacing
style: closed
source: articles
evidence: 38 of 40 em dashes closed across 12 articles
```
Write "tools—and", not "tools — and".

✅ The draft was late—again.
❌ The draft was late — again.

## Quick reference checklist

<!-- checklist:start -->
<!-- checklist:end -->

## Retired

- PUNC-OLD: replaced by PUNC-EMDASH
~~~

- **Frontmatter:** flat keys only. `content_types` lists the kinds of piece the brand publishes; a rule's `scope` may name only these. `generated` is `false`, or one sentence naming the source and date of a compiled guide ("Compiled from brand kit 1234 on 2026-11-12; change rules in the kit"). A guide built from a brand kit also holds `kit_id` and `kit_updated_at` (the kit's `updated_at` when it was read), which `style-check` compares against the live kit.
- **Sections:** `##` headings group rules for readers and carry no meaning for the tools; order is free.
- **Rules:** `### <ID>: <title>`, then a fenced `rule` block, then prose and examples. ✅ and ❌ lines are examples; `sgc guide validate` runs the rule's own check on every ✅ line and reports one the check would flag.
- **IDs:** uppercase letters, digits, and hyphens, prefixed by area (`VOICE-`, `HEAD-`, `PUNC-`, `NUM-`, `TERM-`, `STRUCT-`, `LINK-`, `IMG-`, or the brand's own). An ID is never renumbered or reused; a rule that goes is listed under `## Retired` with the reason.
- **Checklist:** `sgc guide checklist` writes it between the markers from the rules themselves; never edit it by hand.

## Rule block

| Field | Values | Meaning |
|---|---|---|
| `severity` | `must`, `should`, `prefer` | `must` for the brand's explicit requirements, `should` for consistent practice, `prefer` for tendencies. `prefer` findings are suggestions |
| `scope` | `all`, or `[type, ...]` | The content types the rule applies to |
| `kind` | `mechanical`, `usage`, `voice`, `structure` | The reviewer that reads the rule when it has no `check` |
| `check` | A lint check below | Code tests the rule with the parameters that follow; no model reads it |
| parameters | Per check | Flat keys after `check` |
| `source` | `articles`, `edits`, `doc`, `manual`, `kit:<id>`, `kit:<id>#<check>` | Where the rule came from |
| `evidence` | Text with real counts | What the rule rests on |
| `audience` | `ai-drafting` (omit for all) | The rule constrains AI drafts; on a human draft its findings are suggestions |

Values are a small YAML subset: `key: value`, inline lists `[a, b]`, and quoted strings (`"\\b[Cc]lick here\\b"` for a regex).

**Kit rules:** a rule from a brand kit keeps the kit's text verbatim as its body and the kit rule's ID in `source`, so a later import updates the rule instead of adding a copy. A kit rule that several checks can test becomes one rule per check (`source: kit:<id>#<check>`, the body holding the kit sentences that check covers) plus one `source: kit:<id>` rule for the sentences no check covers.

## Lint checks

Each check takes its parameters from the rule block, so a guide that sets the opposite parameter gets the opposite result. A finding is `certain` when the pattern settles it and `uncertain` when context could excuse it; uncertain findings go to the mechanical confirmer.

| Check | Parameters | Finds |
|---|---|---|
| `dash-spacing` | `style`: `spaced`, `closed`, or `none`; `ranges`: `en-dash` or `hyphen` | Em dashes against the style (`none` flags every em dash outside quotes); spaced hyphens or en dashes standing in for em dashes; ranges written the other way |
| `heading-case` | `case`: `title` or `sentence`; `levels` (default `[2, 3, 4]`); `style`: `cmos` or `ap` | Headings in the wrong case; possible proper nouns are uncertain |
| `heading-format` | `no_bold`, `no_end_period` | Bold inside headings; headings that end in a period |
| `serial-comma` | `required`: true or false | "A, B and C" (or "A, B, and C" when false); always uncertain |
| `banned` | `terms`: list; `case_sensitive` (default false) | Banned words and phrases outside quoted speech |
| `preferred` | `pairs`: list of `"wrong => right"` | The wrong form, with the right one as the fix |
| `term-case` | `terms`: correctly cased names | Other casings of those names |
| `numerals` | `spell_out_below` (default 10) | Bare numerals under the threshold in prose, excluding percentages, money, units, dates, times, versions, and list numbering |
| `ordinals` | `spell_out_below` (default 10) | "2nd", "8th" under the threshold |
| `sentence-start-numeral` | none | A sentence that starts with a numeral |
| `percent` | `style`: `symbol` or `word` | "70 percent" against `symbol`, "70%" against `word` |
| `money` | `style`: `abbreviated` or `words` | "$2.6 million" against `abbreviated`, "$2.6M" against `words` |
| `thousands` | `style`: `comma`, `k`, or `either`; `consistent` (default true) | "4k" against `comma`; a piece that mixes "200k" and "200,000" |
| `date-format` | `ordinals` (default false) | "September 24th" when ordinals are off |
| `time-format` | `style`: `9am`, `9 am`, or `9 a.m.` | Times in another style |
| `quote-style` | `marks`: `curly` or `straight`; `punctuation_inside` (default true) | The other kind of marks; a comma or period outside a closing quote |
| `bold-label` | `separator`: `colon`, `period`, or `dash` | List labels with another separator |
| `link-hygiene` | `tracking` (default true), `https` (default true), `max_anchor_words` (default 12) | Tracking parameters, `http://` links, anchors longer than the limit |
| `regex` | `pattern`, `message`, `flags`, optional `replacement` | A custom pattern for a rule no built-in check covers |
