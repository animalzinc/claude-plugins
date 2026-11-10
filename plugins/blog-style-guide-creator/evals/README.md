# Evals

Four `claude plugin eval` cases, each seeded from the demo brand or the test fixtures by its `scaffold.sh`:

| Case | Checks |
|---|---|
| `seeded-errors` | Every planted error in `examples/demo-brand/drafts/seeded-draft.md` is reported, and nothing in its code block or block quote is |
| `brand-leakage` | A clean article in the demo brand's own conventions gets no finding against those conventions |
| `v1-compat` | A version 1 guide still produces a report, with findings under `V1-` rule numbers |
| `fact-check` | A link that contradicts its sentence and a misspelled name are reported |

Run them from the repository root. Skills run `sgc` through Bash and write findings with Write, so both need a grant, and the scaffolds need `--scaffold`:

```
claude plugin eval plugins/blog-style-guide-creator --runs 1 --ablation none --scaffold \
  --allow-tools Write "Bash(python3 *)" WebSearch "WebFetch(domain:www.iana.org)"
```

`--ablation none` skips the run without the plugin, which cannot reach the plugin's agents. The `fact-check` case fetches iana.org from inside the eval sandbox; where the sandbox's network proxy refuses or cuts the connection, the fact-checker marks every claim unverifiable and two of its graders fail. Run that case where the sandbox allows the fetch, or test the fact-check on a real draft outside the eval.
