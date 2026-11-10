# Sources

Every source is saved into the brand folder before anything reads it, so counts and quotes come from the same files a later run can read again.

## Articles

Aim for 8 to 15 recent published articles across the brand's content types. With fewer than five, say the evidence is thin and that rules will rest on few examples.

- **Article URLs:** for each, `sgc extract <url> --out <brand_dir>/sources/articles/<slug>.md`, where the slug is the URL's last path segment. Extract keeps headings, emphasis, links, lists, block quotes, footnotes, and image alt text, which the counts need; a summarizing web fetch would lose punctuation and casing.
- **A blog index URL:** run `sgc extract <url> --out <build>/blog-index.md`, read the links in it, and pick the most recent articles on the blog's own domain (skip tag, author, and category pages). Show the list and confirm it with the user before extracting each one. When the index yields no article links (some blogs load their lists with JavaScript), ask the user for the article URLs.
- **A folder:** run `sgc extract` on each Markdown or HTML file into `sources/articles/`.

Articles already in `sources/articles/` are kept, so an update reads old and new articles together. A file name that already exists is skipped, not overwritten.

## Brand document

`--from-doc F` takes Markdown, plain text, HTML, or PDF. Copy a Markdown, text, or HTML file into `<brand_dir>/sources/docs/`; for a PDF, read it with the Read tool and write its text as Markdown into `sources/docs/<name>.md`, keeping headings and lists. For a Word file, ask the user for a PDF or Markdown export.

A document's explicit rules outrank article patterns, so the guide builder keeps the document's wording.

## Brand kit

`--from-kit [kit]` needs a connected brand kit tool, such as the AirOps connector's `get_brand_kit`. Without one, ask the user to save the kit's JSON export into `<brand_dir>/sources/docs/kit/` and continue from there.

With the AirOps connector:

1. Find the kit: `list_brand_kits`, matched to the `[kit]` argument or the brand name. Confirm the kit's name and ID with the user.
2. Read the active version in three calls, so no single response is too large:
   - `fields: ["id", "brand_name", "updated_at", "writing_persona", "writing_tone"]`
   - `includes: ["writing_rules"]`, `fields: ["writing_rules.id", "writing_rules.text"]`
   - `includes: ["content_types.writing_rules"]`, `fields: ["content_types.id", "content_types.name", "content_types.header_case"]`
3. Write each response, exactly as returned, to `<brand_dir>/sources/docs/kit/01-voice.json`, `02-rules.json`, and `03-content-types.json`, replacing earlier copies. `sgc kit-candidates` reads them as they are.

Read the kit's active version, never a draft, so the guide matches what the kit's other users see.

## Edits

`--edits [folder]` reads pairs of the same draft before and after an editor's pass: `<folder>/<pair>/original.md` and `edited.md` (default folder `<brand_dir>/sources/edits/`). Version 1's `articles/original/` and `articles/edited/` folders also work when the file names match; unmatched files are listed and skipped.

Rules from edits need at least two matching edits; one edit is an anecdote. With `--kit-only`, they become proposals for the kit's owner instead of guide rules.
