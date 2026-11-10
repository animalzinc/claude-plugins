---
name: batch-review
description: Runs a style check on every draft in a folder against one brand's guide and writes a summary of the violations across them, showing which rules break most often and which drafts need the most work. Use when someone asks to check, review, or audit several drafts or a whole folder against a brand's guide.
argument-hint: <brand> <folder> [--type T] [--draft human|ai] [--facts] [--guide F]
allowed-tools: Read, Write, Glob, Agent, Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" *), Bash(py -3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" *)
---

# Batch review

Checks every draft in a folder, one at a time, then summarizes across them. Each draft gets its own run folder and report, exactly as a single `style-check` would produce.

Arguments: $ARGUMENTS

1. List the Markdown files directly in the folder, skipping `*_edited.md`, `*.bak`, and anything inside a `.style-check` folder. Show the count and confirm before starting when there are more than ten; each draft launches up to eight agents.
2. For each draft, run the `blog-style-guide-creator:style-check` skill's steps 1 to 6 with the same brand and flags. Resolve the guide once and reuse it. Never apply fixes in a batch; `--apply` is ignored here.
3. When a draft's check stops on an error, record the draft and the error and continue with the next one.
4. After the last draft, read each run's `findings/final.json` and write `<folder>/style-review-summary.md`:
   - a table of drafts with their must, should, and suggestion counts, highest first, each linked to its `report.md`;
   - the ten rules broken most often, with the number of drafts and findings for each;
   - the drafts that stopped on an error, with the error.
5. Show the table and the path to the summary. A rule broken in most drafts may be one the writers do not know or one the guide states badly; say which rules those are, so the user can decide whether to run `validate-style-guide`.
