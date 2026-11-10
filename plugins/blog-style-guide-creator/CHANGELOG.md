# Changelog

## 2.0.1

November 2026. Fixes from running the plugin on a real guide.

**Checking**

- `numerals` skips both numbers of an en-dash range ("3–5 times per week"), closed or spaced.
- `numerals` skips rank positions ("position 3", "rank 2") and ages ("a 5-year-old company"), and marks a numeral after a capitalized name as uncertain, since it may be a version ("Claude 3").
- `dash-spacing` with `style: none` skips a sign-off line: an em dash followed by a short capitalized name ("— Ty Magnin"), with optional leading whitespace, emphasis marks, or a blockquote marker. Em dashes in running prose are still flagged.
- `time-format` takes two optional parameters, both off by default: `drop_zero_minutes` writes "9 a.m." for "9:00 a.m." and flags the ":00" form, and `noon_midnight` writes noon and midnight for 12 p.m. and 12 a.m.
- `regex` takes an optional `certainty` (`certain` by default, or `uncertain`), so a pattern whose rule carries exemptions sends its hits to the mechanical confirmer.
- `money` with `style: abbreviated` abbreviates million, billion, and trillion only, and leaves "$150 thousand" as written.
- `sgc findings` merges findings on the same text from rules that share a kit ID in `source` (a kit rule split into `kit:<id>#<check>` and `kit:<id>`), keeping the lint finding and its fix.

**Auditing**

- The guide auditor no longer reports judgment rules that lack a number, scope gaps the rule's own text already limits, persona and tone sections that restate rules, rules that agree with each other, or wording in instructional prose that is not a model example.

## 2.0.0

November 2026. A rebuild for current Claude Code and the Claude 5 models.

**Loading and paths**

- The plugin loads again: the marketplace entry no longer lists commands and agents beside the plugin's own manifest, which Claude Code refused as conflicting manifests.
- Prompts and scripts resolve through the plugin's own folder, and brand data lives in a configurable guides folder (`brands/` in the project by default), never in the plugin cache.

**Checking**

- Code runs every mechanical rule (19 checks, each set by the guide's parameters), so no brand's conventions are built into the plugin.
- Four parallel reviewers (usage, structure, voice, proofreading) replace the eight section-bound agents, and a verifier confirms each of their findings against the rule's exact text.
- Findings carry real line numbers from a numbered copy, exact quotes that code re-checks, and a replacement or a comment.
- Code, block quotes, URLs, and quoted speech are protected from findings.
- Rejected findings are remembered per brand and not raised again.
- New: `--facts` fact-checks claims and links against saved source pages.
- New: proofreading for typos, wrong words, doubled words, agreement, unbalanced punctuation, and inconsistent name spellings. Code checks every draft for unclosed parentheses, square brackets, and bold markers, so those never depend on a model.
- `--apply` replaces `--auto-apply`: certain fixes apply automatically, the rest are offered by rule, overlapping fixes are refused, and the result is checked again.

**Building guides**

- One skill, `build-style-guide`, creates, updates, imports, and upgrades guides. `/generate-style-guide` and `/update-style-guide` still work.
- New: import a brand kit (`--from-kit`, `--kit-only`) or a style document (`--from-doc`).
- New: learn rules from editor edits (`--edits`).
- Rules have stable IDs, severities, content-type scopes, and evidence with real counts; every change is shown as a diff for approval before the guide is written.
- `validate-style-guide` audits for contradictions, vague rules, overlaps, and check settings that disagree with the rule text.

**Models**

- Every agent names its model and effort: Sonnet for reviewing, Opus for voice and for verifying voice and structure findings, Sonnet for verifying usage and proofreading findings, Haiku for yes-or-no confirmations. Guide building uses the `deep_model` setting (Opus by default).
- Agents run with read and write access only, except the fact-checker, which also searches and fetches.

**Examples**

- A fictional demo brand with a seeded draft replaces the Animalz and We Eat Robots examples.

**Upgrading**

1.x guides keep working as they are; `build-style-guide <brand> --upgrade` converts one.

## 1.x

2025 to 2026. Style guide generation from published articles, an eight-agent review, batch review, and guide validation, as described in The Workflow (April 2026).
