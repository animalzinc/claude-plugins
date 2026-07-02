# mdview

**A clean, rendered reading view for markdown, with an inline-comment to paste-ready-feedback loop**

Turns a markdown file into a formatted page in your browser (no raw syntax), lets you drop inline comments, and hands those comments back as a paste-ready prompt for the next revision.

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) at [Animalz](https://animalz.co)

---

## What it does

When Claude produces a markdown document, reading it as raw syntax in the terminal is painful. mdview renders it into a clean, self-contained HTML page and opens it in your browser. You read the formatted document, drop inline comments on any block (or quote a specific phrase), and click one button to copy all your feedback as a structured prompt. Paste that back into the chat and Claude applies the changes.

It sits between a throwaway HTML preview and a full collaborative editor: no server, no login, no live sync. Just a file, rendered, in your browser.

## When to use it

- Reviewing a doc, spec, brief, or draft that Claude just wrote
- You want to read the rendered output, not the markdown source
- You want to give precise, located feedback and hand it back in one paste
- You want to copy the rendered content as rich text into email, a doc, or notes

## Quick start

Install the plugin:

```bash
/plugin install mdview
```

Then just ask, in natural language:

```
show me the markdown
render this doc so I can read it
mdview ./notes/spec.md
```

Claude runs the bundled generator on the file, which writes a self-contained HTML file and opens it in your default browser.

---

## What the page gives you

- **Rendered reading view.** Full GitHub-flavored markdown: headings, lists, tables, task lists, code blocks, blockquotes, images. Light/dark toggle plus a color / black-and-white palette toggle. Local images are embedded into the file, so the page is fully self-contained.
- **Copy as rich text.** Copies the rendered content as formatted text (including embedded images) for pasting into email, a doc, or a notes app.
- **Inline comments.** Hover any block and click the `+` to comment, or select text first to quote a specific phrase. Comments appear as numbered markers beside the text and in a side panel. A "+ General note" adds doc-wide feedback. Comments persist per file across reloads.
- **Inline edits.** Double-click any paragraph, heading, list item, or blockquote and just retype it. The change is tracked alongside your comments and lands in the copied feedback as a precise replace instruction, so small wording fixes don't need a comment at all.
- **Copy feedback.** Assembles every comment and edit into a single paste-ready prompt. Paste it back into the chat and Claude applies the changes to the source.
- **Clear all.** Wipes the saved comments and edits for a file so the next review starts clean, with a one-tap Undo.

## The feedback loop

1. Claude writes a markdown file.
2. You open it with mdview and read the rendered version.
3. You drop inline comments where you want changes, and directly retype anything small.
4. You click **Copy feedback** and paste the result back into the chat.
5. Claude revises the source. Repeat until it is right.

---

## Requirements

- Claude Code
- Python 3 (standard library only, nothing to install)
- A desktop browser (macOS opens via `open`; Linux and Windows use the OS default)

## Notes and limits

- Intended for your own trusted local files. The rendered markdown is not sanitized, so do not use it on untrusted content.
- Local images up to 4 MB are embedded as data URIs; larger ones load from their original location (works locally, but not after pasting elsewhere). Remote images stay remote.
- Relative link paths resolve against the source file's directory and open in a new tab. Relative links to other markdown files open as raw text.
- Code blocks, tables, and blocks containing images can be commented on but not edited inline.
- Nothing is downloaded at view time and no fonts are embedded, so generated files stay small and work offline.

---

## License

MIT, see [LICENSE](./LICENSE)

---

## About

Built by **Tim Metz** at **[Animalz](https://animalz.co)**.

- [LinkedIn](https://www.linkedin.com/in/metztim/)
- [X/Twitter @timmetz](https://x.com/timmetz)
- [We Eat Robots](https://weeatrobots.substack.com/)
