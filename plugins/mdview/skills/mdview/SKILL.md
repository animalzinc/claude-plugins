<!-- SYNC: Personal version at ~/.claude/skills/mdview/SKILL.md -->
---
name: mdview
description: Open a clean, rendered (not raw) view of a markdown file in the browser for fast reading, with rich-text copy and an inline-comment to paste-ready-feedback loop. Use when the user says "show me the markdown", "render this markdown", "open that doc so I can read it", "let me review the markdown", "mdview <file>", or asks to view, read, or proof a .md file you produced.
disable-model-invocation: false
allowed-tools: []
---

# mdview

Renders a markdown file into a clean, self-contained HTML reading view and opens it in the default browser. The point: the user reads the *rendered* doc, not the raw syntax, with one command, and can hand back inline comments as a paste-ready prompt. It replaces the "spin up a throwaway HTML file just to read it" step.

This is a lightweight middle ground between a one-off HTML preview and a full collaborative editor. No server, no auth, no live agent editing.

## How to invoke

Run the generator bundled with this skill (it sits next to this file as `generate.py`), passing the **absolute** path of the markdown file (resolve it first, so this works from any project):

```
python3 <this-skill-dir>/generate.py /abs/path/to/file.md
```

That writes a self-contained file to `~/.cache/mdview/<hash>.html` and opens it in the browser. Nothing else to start or stop. Flags (rarely needed): `--browser <AppName>` to force a specific app (macOS only), `--no-open` / `--print-path` to just build and print the path.

To read two files side by side, pass the second with `--against`:

```
python3 <this-skill-dir>/generate.py /abs/path/to/current.md --against /abs/path/to/other.md
```

The file named first is the **working** document (right pane, fully commentable and editable). The file passed to `--against` is the **reference** (left pane, read-only). Get that order right — it decides which document the feedback prompt asks to change.

Cross-platform: on macOS it opens via `open` (and honors `--browser`); on Linux/Windows it opens via the OS default browser. Requires Python 3 (standard library only).

When the user asks to "show me the markdown" and there is one obvious file in play (the one just produced or edited this session), run it on that file without asking. If the target is ambiguous, ask which file.

## What the page gives the user

- **Rendered reading view.** GFM: headings, lists, tables, task lists, code blocks, blockquotes, images. Light/dark toggle, plus a color / black-and-white palette toggle. Local images are inlined as data URIs at generate time (≤ 4 MB each), so the HTML is fully self-contained and images survive rich-text copy.
- **Frontmatter as a metadata card.** YAML frontmatter is split out of the body and rendered above the title as a labelled key/value card in the UI font, not as the doc's opening paragraph. Each value is a normal block: commentable, inline-editable, and it lands in the copied feedback like any other. Frontmatter that isn't a flat `key: value` mapping is shown verbatim in the same card; a doc that merely opens with a `---` rule is left alone.
- **Mermaid diagrams.** A ```` ```mermaid ```` fence is rendered as a diagram in place of the code, with a button to toggle back to the mermaid source. The source stays the comment anchor, so feedback on a diagram quotes its markdown. The mermaid library is only bundled into the HTML when the document actually contains a mermaid fence, so ordinary docs stay small.
- **Copy as rich text.** Copies the rendered content as formatted text for pasting into email, a doc, or a notes app (not the markdown syntax).
- **Inline comments.** Hover any block, click the `+` next to the text column to comment; select text first to quote a specific phrase. Comments show as numbered markers beside the text and in a side panel. A "+ General note" adds doc-wide feedback. Comments persist per file across reloads.
- **Table cells are blocks.** A single `td`/`th` is commentable and editable like any paragraph, so feedback lands on one cell rather than the whole table. Hovering outlines the cell and puts the `+` on its top-left corner; markers for cells in the same row stack instead of overlapping. Every cell comment and edit records its row label and column header, so it survives reloads, is never confused with an identically-worded cell elsewhere, and reaches the chat as `On "Nothing" (table row "Data collection", column "What's needed")`.
- **Inline edits.** Double-click any paragraph, heading, list item, blockquote, or table cell to edit its text in place (code blocks and image blocks are comment-only). The change is tracked like a comment — highlighted block, numbered marker, panel card showing old → new — and lands in the copied feedback as a precise Replace instruction. Esc cancels while editing; "Discard" in the panel restores the original text. Edits persist per file like comments; after a reload the doc shows the source text again, with the pending edit still listed in the panel.
- **Copy feedback.** Assembles every comment and edit into a paste-ready prompt and copies it. The user pastes it back into the chat.
- **Split view (`--against`).** Two panes under one toolbar, each scrolling on its own. The reference pane is read-only; hovering any block there reveals `→` to carry that block into the feedback, `→ §` on a heading to carry its whole section (everything down to the next heading of the same or higher level), and `⧉` to copy that block's markdown to the clipboard. Carried-over blocks keep a coloured spine in the reference pane, so a long pass can be picked up where it left off, and they land in the panel under "Bring across" showing the exact source markdown. A sync button in the toolbar keeps the panes aligned by matching heading text — headings with no counterpart on the other side are left alone rather than guessed at, so an unmatched stretch simply stops tracking until the next shared heading. Feedback in split view is saved per *pair*, so it never mixes with the comments from viewing either file on its own.
- **Clear all.** A button at the top of the panel (next to "+ General note") wipes the saved comments and edits for this file so the next review starts clean (with a one-tap Undo in the toast). Because feedback persists per file, after a revise-and-reopen cycle the previous round is still there until cleared.

## Consuming pasted-back feedback

When the user pastes the feedback prompt back, it looks like:

```
Feedback on `file.md`:

1. On "<quoted text>":
   <their note>
2. Replace:
   "<old block text>"
   with:
   "<new block text>"

General notes:
3. <doc-wide note>

Please revise accordingly. For Replace items, keep the block's existing markdown formatting (links, emphasis) where it still applies.
```

Treat each numbered "On" item's quote as the *location* in the file and the note as the *requested change*; apply them to the source markdown. "Replace" items come from inline edits: find the block whose text matches the old text and replace it with the new text, preserving that block's markdown formatting (links, bold, list markers) wherever the wording still contains it. "General notes" apply document-wide. If the user instead just says the doc looks good with no comments, ship it as-is.

A split-view round adds a "Bring across" section:

```
Bring across from `other.md`:
4. Section "Fail-fast policy":
~~~markdown
## Fail-fast policy
…
~~~
```

That markdown is verbatim from the reference file and is meant to be reinstated in the working file. Place each item where it belongs in the *current* structure rather than at the position it held in the reference — adapt heading levels and connecting wording to fit, keep the substance intact, and say where you put each one. If an item duplicates something the working file already covers in different words, say so and propose a merge instead of pasting it in twice.

Items that carry a `(table row "…", column "…")` suffix target one cell of a markdown table: find the row by its label and the cell by its column header, and change only that cell. Don't reword neighbouring cells, and don't add or drop columns or rows unless the note explicitly asks for it.

## Notes and limits

- **No HTML sanitization** of the rendered markdown. This is intended for the user's own trusted local files; rendering untrusted markdown through it is out of scope.
- **Local images are inlined** as data URIs at generate time (≤ 4 MB per image; larger ones fall back to `<base>`-relative loading, which works locally but not after pasting elsewhere). Remote (`http(s)`) images are left as URLs. Image references inside code fences are never rewritten.
- **Relative links** resolve against the source file's directory (via `<base>`) and open in a new tab so the review is never navigated away. Relative links to *other* `.md` files open as raw text.
- **Brand fonts are referenced, not embedded.** The font stack names specific fonts first and falls back to system fonts, so nothing is downloaded and generated files stay small.
