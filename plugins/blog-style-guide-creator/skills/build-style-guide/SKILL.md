---
name: build-style-guide
description: Builds or updates a brand's editorial style guide from its published articles, a brand kit, a brand style document, or its editors' edits, and converts a version 1 guide. Every rule cites its evidence, mechanical rules get code checks, and nothing is written until the user approves the changes. Use when someone asks to create, generate, update, import, or upgrade a style guide, or to learn rules from edited drafts.
argument-hint: <brand> [blog URL | article URLs | folder] [--from-kit [kit]] [--from-doc F] [--edits [folder]] [--kit-only] [--upgrade]
allowed-tools: Read, Write, Glob, Agent, Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" *), Bash(py -3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" *)
---

# Build a style guide

Creates, updates, imports, and upgrades one brand's guide. Sources become candidate rules with evidence; one agent merges them with the current guide into a proposal; the user approves the diff before the guide changes. The format every rule follows is in [schema.md](schema.md).

Arguments: $ARGUMENTS

## Commands

Every `sgc` step is `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" <command> ...`, written out in full each time and run as its own Bash call, never chained with `;`, `&&`, or a pipe, so it matches the skill's permission for `sgc`; read and list files with the Read and Glob tools. On Windows, `py -3` in place of `python3`. If neither runs Python 3.9 or later, stop and tell the user the plugin needs Python 3.9+ from python.org. `sgc` prints JSON; on a non-zero exit, show the stderr message and stop unless a step says how to recover.

## Modes

| Arguments | Does |
|---|---|
| `<brand> <sources>` | A new guide, or an update to an existing one, from articles |
| `--from-kit [kit]` | Imports a brand kit through a connected brand kit tool |
| `--from-kit --kit-only` | Compiles the guide from the kit alone; other sources become proposals for the kit's owner |
| `--from-doc F` | Imports a brand style document |
| `--edits [folder]` | Learns rules from original and edited draft pairs |
| `--upgrade` | Converts a version 1 guide, following [upgrade-v1.md](upgrade-v1.md) |

Modes combine: `--from-doc brand.pdf https://blog.example.com` reads both.

## Steps

### 1. Resolve the brand

The plugin's guides folder setting reads: `${user_config.guides_dir}`. Run `sgc brand-path <brand> --project-dir "${CLAUDE_PROJECT_DIR}"`, adding `--guides-dir "<path>"` only when that setting is an absolute path (an unset setting shows as text starting with `${`, which must never reach the shell). Keep `brand_dir`, `guide`, `guide_exists`, and `schema_version`. A `schema_version` of 1 with any mode other than `--upgrade`: run the upgrade first, then continue.

The build folder for this run is `<brand_dir>/builds/<YYYY-MM-DD>/`; every intermediate file goes there, so the user can see what each rule rests on.

### 2. Collect sources

Follow [sources.md](sources.md) for each source type. Afterwards the brand folder holds `sources/articles/*.md`, `sources/docs/` (a brand document, and `kit/*.json` for a kit), and `sources/edits/<pair>/{original,edited}.md`, as each mode needs.

### 3. Count and read

Launch these together, in one message, after running the counting commands:

- **Articles:** run `sgc profile <brand_dir>/sources/articles --out <build>/profile.json`, then one `blog-style-guide-creator:source-reader` per batch of up to eight articles, each given its file paths, the profile path, and the output `<build>/candidates/articles-<n>.json`.
- **Brand document:** one `blog-style-guide-creator:source-reader` given the document, the profile path when articles were read, and the output `<build>/candidates/doc.json`.
- **Brand kit:** run `sgc kit-candidates <brand_dir>/sources/docs/kit --out <build>/candidates/kit.json`. No agent; the kit text stays verbatim.
- **Edits:** run `sgc diff-pairs <brand_dir>/sources/edits --out <build>/hunks.json`, then one `blog-style-guide-creator:edit-miner` given the hunks path, `<brand_dir>/decisions.jsonl` when it exists, the current guide when it exists, and the output `<build>/candidates/edits.json`.

### 4. Propose

Launch `blog-style-guide-creator:guide-builder` with `model: "${user_config.deep_model}"` (when that value is empty or still reads `${`, leave `model` out). The prompt gives every candidate file, the current guide path (or "none, new guide"), the profile path when there is one, `kit_only: true` with `--kit-only`, today's date, and the output `<build>/proposal.json`.

With `--kit-only`, the proposal regenerates the whole guide (`complete: true`), and its frontmatter `generated` reads "Compiled from brand kit <kit id> on <date>; change rules in the kit." Any guide built with `--from-kit` also carries `kit_id` and `kit_updated_at` from `candidates/kit.json`, so a later check can tell when the kit has changed since.

### 5. Approve

1. Run `sgc guide render <build>/proposal.json --out <build>/style-guide.proposed.md`, adding `--existing <guide>` when the guide exists.
2. Run `sgc guide validate <build>/style-guide.proposed.md`. On errors, launch guide-builder once more with the errors and the same output path, then render again. Errors that remain are shown to the user with the diff.
3. Run `sgc guide diff <guide> <build>/style-guide.proposed.md --markdown` (for a new guide, list the proposed rules by section instead).
4. Show the user the diff (added, changed, kit text modified, retired), the `conflicts` from the proposal (which source won and which lost), and the `kit_candidates`. Ask which changes to accept: all, none, or by rule ID.
5. When the user declines some, remove those rules from `proposal.json` (and their entries from `retire`), then render and validate again.

Nothing is written to the guide before this approval.

### 6. Write and check

1. When the guide exists, save its current text to `<build>/style-guide.before.md` (read it, write the copy), then run `sgc guide render <build>/proposal.json --out <guide> --existing <build>/style-guide.before.md`. For a new guide, run the render without `--existing`.
2. Run `sgc guide checklist <guide>`, then `sgc guide validate <guide>`.
3. Launch `blog-style-guide-creator:guide-auditor` with `model: "${user_config.deep_model}"` (same fallback as step 4), giving the guide path, the outputs of `sgc guide parse <guide> --out <build>/rules.json` and the validate run, and the output `<build>/audit.json`.
4. Show the audit's findings by type, each with its proposed fix, and offer to apply the fixes the user picks through another approve and write round.
5. With `--kit-only`, write the `kit_candidates` to `<build>/kit-candidates.md` (title, proposed kit text, evidence) and say they are for the kit's owner; this skill never writes to a brand kit.

Finish with the guide's path, its rule count by severity, and how many rules have a code check.
