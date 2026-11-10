# Fact-check

With `--facts`, the fact-checker lists every checkable claim and outbound link, fetches a source for each through `sgc fetch`, and writes a ledger whose excerpts are copied from the saved pages. Code then confirms every excerpt against its page, so a confirmed claim always rests on text that is on the page.

1. In the step 3 launch message, include `blog-style-guide-creator:fact-checker` with the absolute run folder. It writes `<run>/facts/ledger.json` and saves pages in `<run>/facts/pages/`.
2. When it returns, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sgc.py" ledger-check --run-dir <run>`.
3. Exit 0: every row passed. Continue with step 4 of the skill; the ledger's issues are in `findings/facts.json`, which `sgc findings` reads.
4. Exit 1: some rows failed. `<run>/facts/ledger-check.json` lists `failing_ids` with each row's status and note (an excerpt not on the page, a confirmed row without an excerpt, a link marked dead whose fetch succeeded). Launch the fact-checker again with the run folder, those IDs, and their notes, asking it to update only those rows in `ledger.json`: fetch the source again and copy the excerpt exactly, or mark the row `unverifiable`. Run `ledger-check` once more. Rows that still fail are reported as failed checks, never as confirmed.

Fact findings carry the ledger verdict in their rule ID (`FACT-CONTRADICTED`, `FACT-UNSUPPORTED`, `FACT-UNVERIFIABLE`, `FACT-LINK-DEAD`, `FACT-LINK-MISMATCH`) and appear in their own section of the report. The verifier does not see them; the ledger check stands in for it.
