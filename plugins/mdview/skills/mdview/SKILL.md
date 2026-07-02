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

Cross-platform: on macOS it opens via `open` (and honors `--browser`); on Linux/Windows it opens via the OS default browser. Requires Python 3 (standard library only).

When the user asks to "show me the markdown" and there is one obvious file in play (the one just produced or edited this session), run it on that file without asking. If the target is ambiguous, ask which file.

## What the page gives the user

- **Rendered reading view.** GFM: headings, lists, tables, task lists, code blocks, blockquotes, images. Light/dark toggle, plus a color / black-and-white palette toggle. Local images are inlined as data URIs at generate time (≤ 4 MB each), so the HTML is fully self-contained and images survive rich-text copy.
- **Copy as rich text.** Copies the rendered content as formatted text for pasting into email, a doc, or a notes app (not the markdown syntax).
- **Inline comments.** Hover any block, click the `+` next to the text column to comment; select text first to quote a specific phrase. Comments show as numbered markers beside the text and in a side panel. A "+ General note" adds doc-wide feedback. Comments persist per file across reloads.
- **Inline edits.** Double-click any paragraph, heading, list item, or blockquote to edit its text in place (code blocks, tables, and image blocks are comment-only). The change is tracked like a comment — highlighted block, numbered marker, panel card showing old → new — and lands in the copied feedback as a precise Replace instruction. Esc cancels while editing; "Discard" in the panel restores the original text. Edits persist per file like comments; after a reload the doc shows the source text again, with the pending edit still listed in the panel.
- **Copy feedback.** Assembles every comment and edit into a paste-ready prompt and copies it. The user pastes it back into the chat.
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

## Notes and limits

- **No HTML sanitization** of the rendered markdown. This is intended for the user's own trusted local files; rendering untrusted markdown through it is out of scope.
- **Local images are inlined** as data URIs at generate time (≤ 4 MB per image; larger ones fall back to `<base>`-relative loading, which works locally but not after pasting elsewhere). Remote (`http(s)`) images are left as URLs. Image references inside code fences are never rewritten.
- **Relative links** resolve against the source file's directory (via `<base>`) and open in a new tab so the review is never navigated away. Relative links to *other* `.md` files open as raw text.
- **Brand fonts are referenced, not embedded.** The font stack names specific fonts first and falls back to system fonts, so nothing is downloaded and generated files stay small.
