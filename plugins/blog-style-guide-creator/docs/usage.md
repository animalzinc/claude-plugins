# Usage guide

Each section covers one skill: its options, what it writes, and where. Skills are invoked as `/blog-style-guide-creator:<skill>`, or by asking in plain words ("check this draft against the Acme guide").

## Brand folder

Every brand has one folder, `<guides folder>/<brand>/`. The guides folder is the plugin's `guides_dir` setting, or `brands/` in the current project when that is empty.

```
acme/
  style-guide.md          the guide every check reads
  style-guide.v1.md       a 1.x guide's original text, after --upgrade
  sources/
    articles/             published articles, converted to Markdown
    docs/                 a style document; kit/ for a brand kit's saved JSON
    edits/<pair>/         original.md and edited.md for one edited draft
  builds/<date>/          one folder per build: counts, candidates, proposal, audit
  decisions.jsonl         findings rejected in earlier checks
```

`--guide <file>` on any skill uses a guide file directly; the brand folder still holds `decisions.jsonl` and builds.

## build-style-guide

```
build-style-guide <brand> [blog URL | article URLs | folder] [--from-kit [kit]] [--from-doc F] [--edits [folder]] [--kit-only] [--upgrade]
```

| Option | Does |
|---|---|
| sources | A blog URL (the skill lists recent articles and asks you to confirm), article URLs, or a folder of Markdown or HTML files |
| `--from-kit [kit]` | Imports a brand kit's persona, tone, global rules, and content-type rules through the AirOps connector, or from JSON saved in `sources/docs/kit/` |
| `--kit-only` | With `--from-kit`: the guide is compiled from the kit alone and marked as generated; patterns from articles or edits become kit-rule proposals in `builds/<date>/kit-candidates.md` |
| `--from-doc F` | Imports a style document: Markdown, text, HTML, or PDF |
| `--edits [folder]` | Learns from edited drafts (default `sources/edits/`) |
| `--upgrade` | Converts a 1.x guide |

Options combine. A run with an existing guide is an update: rules not touched by the new evidence stay word for word, changed rules show their before and after text, and a rule that goes is retired under its ID, never deleted.

What you approve: the diff of added, changed, and retired rules; for kit rules, which ones had their kit text change; and the conflicts the builder settled (for example, a kit rule that overruled what the articles do). You can accept all, none, or a list of rule IDs. After the guide is written, an auditor reads it for contradictions and vague rules and offers fixes through the same approval.

`builds/<date>/` keeps everything the build used: `profile.json` (pattern counts across the articles), `candidates/*.json` (each source's proposed rules with evidence), `proposal.json`, the rendered proposal, the guide as it was before (`style-guide.before.md`), and `audit.json`.

## style-check

```
style-check <brand> <article> [--type T] [--draft human|ai] [--facts] [--apply] [--guide F]
```

| Option | Default | Does |
|---|---|---|
| `--type T` | The article's frontmatter `content_type` | Which content type's rules apply. The skill asks when the guide scopes rules by type and the article does not say |
| `--draft human\|ai` | `human` | Rules the guide marks for AI drafts (`audience: ai-drafting`) are suggestions on a human draft and violations on an AI draft |
| `--facts` | Off | Adds the fact-check |
| `--apply` | Off | Offers fixes after the report |

The run folder is `<article name>.style-check/` next to the article:

| File | Holds |
|---|---|
| `report.md` | Violations by severity and line, suggestions, fact issues, and the count of dropped findings by reason |
| `findings/final.json` | Every finding in the report, with its ID, rule, line, quote, fix, and who found it |
| `findings/drops.json` | Every dropped finding and why |
| `article.numbered.md`, `outline.json` | The prepared draft the reviewers read |
| `packets/`, `verify/` | What each reviewer and verifier was given |
| `facts/` | With `--facts`: the ledger and the saved source pages |

Running the check again replaces the findings and keeps the previous report as `report.previous.md`.

### Fixes

With `--apply`, or when you ask after reading the report, the skill applies every certain code fix (a closed dash, a curly quote, a cased name) and offers the reviewers' fixes grouped by rule for you to accept or decline. Fixes go to `<article name>_edited.md`; ask for the article itself to be edited and it saves a `.bak` copy first. Two fixes on the same text are both held back so you can choose. Findings with only a comment (a missing source, a section to rewrite) are listed for the author.

Fixes you decline are written to the brand's `decisions.jsonl`, and later checks of any article for that brand leave the same finding on the same text out.

### Fact-check

With `--facts`, a fact-checker lists every statistic, quote, name, date, and product fact, plus every outbound link with the sentence it supports. It fetches a source for each (the linked page first, or the primary source it finds by search) and gives a verdict: confirmed, contradicted, unsupported, unverifiable, link dead, or link that does not support its sentence. Every excerpt it cites is checked against the saved page by code; an excerpt that is not on the page sends the row back once, and a row that still fails is reported as failed, never as confirmed.

## batch-review

```
batch-review <brand> <folder> [--type T] [--draft human|ai] [--facts] [--guide F]
```

Checks each Markdown draft in the folder, one after another, then writes `style-review-summary.md` in the folder: drafts ranked by violations with links to their reports, the ten rules broken most often, and any draft whose check stopped on an error. It never applies fixes. A rule broken in most drafts is either one writers miss or one the guide states badly; `validate-style-guide` helps tell which.

## validate-style-guide

```
validate-style-guide <brand> [--guide F]
```

Reports schema errors (duplicate IDs, unknown checks, invalid parameters, scopes that name no content type, a ✅ example the rule's own check would flag), then an audit for rules that contradict each other or their examples, rules too vague to apply, overlapping rules, check settings that disagree with the rule text, and rules scoped too wide or too narrow. Each audit finding comes with the smallest edit that resolves it. Nothing changes unless you ask, and then through `build-style-guide`'s approval step.

## Troubleshooting

- **"needs Python 3.9 or later":** install Python 3 from python.org. On Windows the skills run `py -3`.
- **No guide found:** the brand folder is `<guides folder>/<brand>/style-guide.md`; check the `guides_dir` setting, or pass `--guide`.
- **Every heading or dash flagged:** the guide's check parameters say the opposite of the brand's practice. Run `validate-style-guide`; the audit reports check settings that disagree with the rule text.
- **A finding keeps coming back:** decline it during `--apply`; declined findings are remembered per brand.
