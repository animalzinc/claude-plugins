# Applying fixes

Fixes go to a copy, `<article name>_edited.<ext>` next to the article, unless the user asks to edit the article itself. `sgc apply` always starts from the original article, so gather every choice first and apply once.

1. Read `<run>/findings/final.json`. Split the findings that have a `replacement` into two groups:
   - **Automatic:** lint findings with `"certainty": "certain"` that are not suggestions. `--accept auto` selects exactly these.
   - **To offer:** every other finding with a replacement, grouped by rule ID. Show each group as numbered lines (line number, quote, replacement) and ask which to accept: numbers, a rule ID for the whole group, "all", or "none".
2. Findings with only a comment are never applied; list them as the edits left for the author.
3. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" apply --run-dir <run> --accept auto,<accepted ids>` (comma-separated IDs; drop `auto` if the user declined the automatic fixes). Add `--in-place` only when the user asked to edit the article itself; it saves `<article name>.bak` first and refuses when the article changed since the check.
4. Report from its JSON: how many fixes were applied, each refused fix with its reason (two fixes touching the same span are both refused, so the user can pick one), the output path, and the re-lint count. A re-lint finding on a line that was edited means a fix introduced a problem; name it.
5. Record the fixes the user rejected, so the next check of any article for this brand leaves them out: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" decisions --run-dir <run> --reject <ids> --brand-dir <brand_dir> --reason "<the user's reason, if they gave one>"`. Record only explicit rejections, never findings the user skipped without a word.
