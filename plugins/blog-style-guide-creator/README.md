# Blog Style Guide Creator

Created by [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) | Published by [Animalz](https://animalz.co)

Blog Style Guide Creator writes a brand's editorial style guide from what the brand already has: its published articles, a brand kit, a style document, or the edits its editors make. It then checks drafts against that guide. Every finding quotes the exact text it flags, names the rule it breaks, and offers a fix, and nothing in a draft changes unless you ask.

A check combines code and models. Code tests everything a pattern can settle (dash spacing, heading case, numbers, quote marks, links). Parallel reviewers read for usage, structure, voice, and plain errors. A second reviewer then verifies every judgment against the guide's own wording, and code drops any finding whose quote is not in the draft.

## Install

```
/plugin install blog-style-guide-creator --marketplace animalzinc/claude-plugins
```

On Claude Code before 2.1.275, add the marketplace first:

```
/plugin marketplace add animalzinc/claude-plugins
/plugin install blog-style-guide-creator
```

Requirements: Claude Code 2.1.271 or later, and Python 3.9 or later on the machine (standard library only, nothing to install).

## Quick start

Build a guide from a blog, then check a draft against it:

```
/blog-style-guide-creator:build-style-guide acme https://acme.example/blog
/blog-style-guide-creator:style-check acme drafts/launch-post.md
```

The check writes `drafts/launch-post.style-check/report.md`: violations sorted by severity with line numbers, suggestions in a separate list, and a count of the findings that were dropped and why. Add `--apply` to review fixes and write them to `launch-post_edited.md`.

To try it without a brand of your own, point the plugin at the demo brand in `examples/demo-brand/` (see [Demo brand](#demo-brand)).

## Skills

| Skill | Does |
|---|---|
| `build-style-guide` | Creates or updates a guide from articles, a brand kit (`--from-kit`), a style document (`--from-doc`), or editor edits (`--edits`); converts a 1.x guide (`--upgrade`) |
| `style-check` | Checks one draft; `--facts` adds a fact-check, `--apply` offers fixes |
| `batch-review` | Checks every draft in a folder and summarizes the rules broken most often |
| `validate-style-guide` | Audits a guide for contradictions, vague rules, overlaps, and check settings that disagree with the rule text |

`/generate-style-guide` and `/update-style-guide` from version 1 still work and run `build-style-guide`.

## Check pipeline

1. **Prepare:** code writes a line-numbered copy of the draft and marks the zones no rule touches: code, block quotes, URLs, and quoted speech.
2. **Lint:** code runs every rule that has a check, with the parameters the guide sets. A guide that closes its em dashes gets the opposite result from one that spaces them; no brand's preferences live in the code. Every draft is also checked for unclosed parentheses, square brackets, and bold markers, whatever the guide says.
3. **Review:** in parallel, a usage reviewer, a structure reviewer, a voice reviewer, and a proofreader each read the draft against their share of the guide. A small model settles lint findings a pattern could not decide alone. With `--facts`, a fact-checker fetches a source for every claim and link.
4. **Filter:** code drops findings whose quote is not on the cited line, findings outside the rule's scope or inside protected zones, and findings you rejected before.
5. **Verify:** a second reviewer reads each remaining finding with the rule's exact text and keeps, revises, or drops it.
6. **Report:** code writes the report; with `--apply`, it applies the fixes you accept and checks the result again.

A fact-check finding rests on an excerpt copied from a saved page, and code confirms every excerpt is on that page before the report lists it.

## Building a guide

`build-style-guide` reads whatever sources you give it and proposes rules, each with the evidence behind it ("38 of 40 em dashes closed across 12 articles"). When sources disagree, a brand kit or style document outranks editor edits, which outrank article patterns. You see the proposed changes as a diff (added, changed, retired) and approve all, some, or none; the guide changes only after that.

- **Articles:** 8 to 15 recent articles give enough evidence; a blog URL, article URLs, or a folder of Markdown or HTML files all work. Articles are fetched and converted by script, so punctuation and casing counts are exact.
- **Brand kit:** with the AirOps connector, `--from-kit` imports the kit's persona, tone, and rules, keeping each rule's wording and kit ID so a later import updates rules instead of adding copies. `--kit-only` compiles the guide from the kit alone and turns patterns found elsewhere into proposals for the kit's owner.
- **Style document:** `--from-doc` takes Markdown, text, HTML, or PDF.
- **Editor edits:** pairs of drafts before and after an editor's pass, in `sources/edits/<pair>/original.md` and `edited.md`. A change editors make at least twice becomes a proposed rule; content edits are kept apart from style edits.

Each rule in the guide has a stable ID, a severity (`must`, `should`, or `prefer`), a scope (all content or listed content types), and, where code can test it, a check with parameters. The format is in [skills/build-style-guide/schema.md](skills/build-style-guide/schema.md).

## Configuration

Set these when you enable the plugin, or later in `/plugin`:

| Setting | Default | Purpose |
|---|---|---|
| Brand guides folder (`guides_dir`) | `brands/` in the current project | Holds one folder per brand: `<brand>/style-guide.md`, `sources/`, `builds/`, and `decisions.jsonl` |
| Model for building guides (`deep_model`) | `opus` | Model for drafting and auditing guides: `opus` or `fable` |

Every skill also takes `--guide <file>` to use a guide file directly.

## Demo brand

`examples/demo-brand/` is a fictional company, Acme Analytics, whose conventions differ from common defaults on purpose: closed em dashes, sentence-case headings, no serial comma, "percent" spelled out, and times written "9 a.m.". It holds three source articles, the guide built from them, an edit pair, and `drafts/seeded-draft.md`, a draft with 31 planted errors listed in `seeded-draft.expected.json`.

```
/blog-style-guide-creator:style-check demo-brand examples/demo-brand/drafts/seeded-draft.md --guide examples/demo-brand/style-guide.md
```

## Upgrading from 1.x

A 1.x guide keeps working: the checks read its numbered sections as rules. `build-style-guide <brand> --upgrade` converts it to the 2.0 format, keeps its wording, saves the original as `style-guide.v1.md`, and shows the conversion for approval. The [changelog](CHANGELOG.md) lists what changed.

## Docs and support

- [Usage guide](docs/usage.md): every skill's options, the run folder, fixes, and the fact-check
- [Changelog](CHANGELOG.md)
- Issues: https://github.com/animalzinc/claude-plugins/issues
- Email: contact@animalz.co

MIT License. Copyright (c) 2026 Tim Metz.
