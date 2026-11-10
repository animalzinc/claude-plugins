---
name: style-check
description: Checks one draft against a brand's style guide and writes a report of violations, each with the exact quote, the rule, and a fix. Code runs the mechanical checks; parallel reviewers cover usage, structure, voice, and proofreading; a verifier confirms every reviewer finding. With --facts, also fact-checks the draft's claims and links against saved source pages; with --apply, offers the fixes. Use when someone asks to check, review, proofread, or fact-check a draft against a brand's guide, "style check this", "does this follow the X guide", or "check the facts and links in this draft".
argument-hint: <brand> <article file> [--type T] [--draft human|ai] [--facts] [--apply] [--guide F]
allowed-tools: Read, Write, Glob, Agent, Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" *), Bash(py -3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" *)
---

# Style check

Checks one article against one brand's guide. Code settles what a pattern can settle; agents judge the rest; a second agent verifies every judgment; code drops any finding whose quote is not in the article. The report goes next to the article, so the user can open it, and nothing in the article changes unless the user asks.

Arguments: $ARGUMENTS

## Commands

Every `sgc` step below is `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" <command> ...`; write the command out in full each time, because the plugin path is substituted in this text and is not set in the shell. Run each command as its own Bash call, never chained with `;`, `&&`, or a pipe, so it matches the skill's permission for `sgc`; read and list files with the Read and Glob tools. On Windows use `py -3` in place of `python3`. If neither runs Python 3.9 or later, stop and tell the user the plugin needs Python 3.9+ from python.org.

`sgc` prints JSON. A non-zero exit prints the reason on stderr: show it to the user and stop, unless a step below says how to recover.

## Steps

### 1. Resolve the guide

Read `<brand>` and the article path from the arguments, plus these flags:

| Flag | Meaning | Default |
|---|---|---|
| `--type T` | Content type, one of the guide's `content_types` | The article's frontmatter `content_type` or `type` |
| `--draft human\|ai` | Who wrote the draft; rules marked `ai-drafting` are suggestions on a human draft | `human` |
| `--facts` | Also fact-check claims and links | Off |
| `--apply` | Offer fixes after the report | Off |
| `--guide F` | Use this guide file instead of the brand folder's | None |

The plugin's guides folder setting reads: `${user_config.guides_dir}`. Run `sgc brand-path <brand> --project-dir "${CLAUDE_PROJECT_DIR}"`, adding `--guides-dir "<path>"` only when that setting is an absolute path (an unset setting shows as text starting with `${`, which must never reach the shell), and `--guide F` when given. From its JSON:

- `guide_exists` false: stop and offer `build-style-guide <brand>`.
- `schema_version` 1: continue (the tools read v1 guides), and add one line to the summary recommending `build-style-guide <brand> --upgrade`.
- Keep `guide` and `brand_dir` for the steps below.

A guide compiled from a brand kit carries `kit_id` and `kit_updated_at` in its frontmatter. When it does and a brand kit tool is connected (the AirOps connector's `get_brand_kit`), read that kit's `updated_at`. When it is later than `kit_updated_at`, the kit has changed since the guide was compiled: continue, and add one line to the summary recommending `build-style-guide <brand> --from-kit --kit-only`.

### 2. Prepare the run

The run folder is `<article folder>/<article file name without extension>.style-check/`. Running again replaces the previous findings and keeps the previous report as `report.previous.md`.

1. `sgc prepare <article> --run-dir <run> --brand-dir <brand_dir> --draft <human|ai>`, plus `--content-type T` when given. When it stops because the guide scopes rules by content type and none is known, ask the user which of the listed types the piece is, then run it again with `--content-type`.
2. `sgc packets <guide> --run-dir <run>`.
3. `sgc lint <guide> --run-dir <run>`.

### 3. Review

Read `<run>/packets/index.json` and `<run>/findings/lint.json`. Launch every agent below in one message, so they run in parallel. Each prompt gives the absolute run folder and, for a packet, the packet and output names from the index:

| Agent (`subagent_type`) | Launch when | Prompt |
|---|---|---|
| `blog-style-guide-creator:usage-checker` | Each `usage` packet with at least one rule | Run folder; packet `packets/usage.md`; output `findings/usage.json` |
| `blog-style-guide-creator:structure-checker` | Each `structure` packet with at least one rule | Same, for structure |
| `blog-style-guide-creator:voice-checker` | Each `voice` packet with at least one rule | Same, for voice |
| `blog-style-guide-creator:proofreader` | Always | Run folder; output `findings/proof.json` |
| `blog-style-guide-creator:mechanical-confirmer` | `lint.json` has a finding with `"certainty": "uncertain"` | Run folder |
| `blog-style-guide-creator:fact-checker` | `--facts` | Run folder; see [facts.md](facts.md) |

A split packet (`usage-1.md`, `usage-2.md`) gets one agent each, with the output name the index gives it. Each agent writes its file and replies with counts only; no agent sees another's findings.

With `--facts`, run the ledger check from [facts.md](facts.md) after the fact-checker returns and before step 4.

### 4. Filter

Run `sgc findings --run-dir <run>`. It drops findings whose quote is not on the cited line, out-of-scope rules, quotes inside protected zones, uncertain lint findings the confirmer answered no, and findings the brand rejected before (from `decisions.jsonl`), then merges duplicates. When it stops on a malformed findings file, launch that one agent again with the same prompt, once; if the file is still malformed, report which reviewer failed and continue without it by writing `[]` to its findings file.

### 5. Verify

For each entry in the `verify_packets` list that `sgc findings` printed, launch `blog-style-guide-creator:finding-verifier` with the absolute path of its packet, all in one message. Pass `model: "sonnet"` for the `proof` and `usage` packets (split usage packets included), whose findings rest on the rule's wording; the `voice` and `structure` packets use the agent's own model, because those findings rest on judgment. Lint and fact findings are not in these packets; code settled them.

Then run `sgc verdicts --run-dir <run>`. When it lists finding IDs without a verdict, launch the verifier for that packet again, once.

### 6. Report

Run `sgc report --run-dir <run> --guide <guide>`. Show the user:

- the counts it prints (violations by severity, suggestions, fact issues, findings dropped);
- the `must` violations, one line each: line number, rule ID, quote, fix;
- the path to `<run>/report.md`, which holds everything.

Keep the summary to the findings themselves; the report carries the detail.

### 7. Apply

Only with `--apply`, or when the user asks after reading the report: follow [apply.md](apply.md).
