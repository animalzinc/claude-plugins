---
name: validate-style-guide
description: Audits a brand's style guide for problems that would make two reviewers disagree, such as rules that contradict each other or their own examples, rules too vague to apply, overlapping rules, and code-check settings that disagree with the rule text, plus schema errors. Use when someone asks to validate, audit, lint, or sanity-check a style guide.
argument-hint: <brand> [--guide F]
allowed-tools: Read, Write, Glob, Agent, Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" *), Bash(py -3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" *)
---

# Validate a style guide

Checks one guide in two passes: code for the schema, then an auditor for what needs reading. Changes nothing unless the user asks.

Arguments: $ARGUMENTS

Every `sgc` step is `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" <command> ...`, written out in full and run as its own Bash call, never chained with `;`, `&&`, or a pipe, so it matches the skill's permission for `sgc`. On Windows, `py -3` in place of `python3`. Without Python 3.9 or later, stop and say the plugin needs it.

1. The plugin's guides folder setting reads: `${user_config.guides_dir}`. Run `sgc brand-path <brand> --project-dir "${CLAUDE_PROJECT_DIR}"`, adding `--guides-dir "<path>"` only when that setting is an absolute path (an unset setting shows as text starting with `${`, which must never reach the shell), and `--guide F` when given. Without a guide, stop and offer `build-style-guide`.
2. A `schema_version` of 1: report that the guide predates rule IDs, that the checks still read it, and that `build-style-guide <brand> --upgrade` converts it. Then audit it as it is.
3. Run `sgc guide validate <guide>` and `sgc guide parse <guide> --out <brand_dir>/builds/<YYYY-MM-DD>/rules.json`.
4. Launch `blog-style-guide-creator:guide-auditor` with `model: "${user_config.deep_model}"` (leave `model` out when the value is empty or still reads `${`), giving the guide path, the parsed rules path, the validate output, and the output `<brand_dir>/builds/<YYYY-MM-DD>/audit.json`.
5. Report the schema errors and warnings, then the audit's findings grouped by type (contradiction, example conflict, vague, overlap, check mismatch, scope gap), each with the rules involved and the proposed fix. End with the counts.
6. When the user asks for fixes, make them through `build-style-guide`'s approve-and-write steps, so the diff is shown before the guide changes.
