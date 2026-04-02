# Structured Article Writer

**Structured 8-phase writing process for thought leadership articles**

Human fills the blank page — AI enforces discipline, challenges weak thinking, and guards quality gates. Built on editorial principles from Animalz, Zinsser, Stephen King, Robert Caro, and others.

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) at [Animalz](https://animalz.co)

---

## Overview

A `/write` slash command that guides you through a structured 8-phase process for writing thought leadership articles. The core philosophy: **the human fills the blank page.** Claude acts as a strict editor — questioning, challenging, and enforcing quality gates — but never originates the ideas. The process compensates for what AI lacks (taste, conviction, lived experience) by front-loading human input and using AI for discipline enforcement.

## Quick start

Install the plugin:

```bash
/plugin install structured-article-writer
```

Start a new article:

```bash
/write ai-content-quality
```

Resume the most recent article:

```bash
/write
```

---

## The 8 phases

| Phase | Name | Goal | Output |
|---|---|---|---|
| 1 | **Foundation** | Define reader, purpose, quality bar | `state.md` |
| 2 | **Idea & Thesis** | Crystallize an arguable thesis from earned experience | `thesis.md` |
| 3 | **Structure** | Headers that tell the complete argument | `outline-10.md` |
| 4 | **Research** | Gather evidence, perspectives, supporting material | `research/` |
| 5 | **30% Outline** | Mini-thesis + supporting points per section | `outline-30.md` |
| 6 | **Introduction Craft** | Hook, sinker, and a line that carries throughout | `introduction.md` |
| 7 | **Drafting** | Human writes, AI supports | `draft.md` |
| 8 | **Review & Refinement** | Thesis drift check, ABCD review, ruthless cuts | `review-notes.md` |

Each phase has quality gates that must pass before advancing. No skipping.

---

## Companion commands

### `/write-rescue` — Mid-process entry

Have an existing draft or outline that isn't working? `/write-rescue` diagnoses the problem, maps it against the 8 phases, identifies the failure point (thesis drift, missing earned secret, outline-to-draft jump, etc.), and creates a `state.md` so `/write` can pick up from the right phase.

```bash
/write-rescue path/to/broken-draft.md
```

### `/write-status` — Quick status check

See where an article stands in the process, or get an overview of all in-progress articles.

```bash
/write-status ai-content-quality    # Single article
/write-status                       # All articles
```

---

## Article folder structure

Each article creates a folder with tracked state:

```
articles/{slug}/
  state.md              # Process state (YAML frontmatter + process log)
  thesis.md             # Thesis, earned secret, antithesis
  outline-10.md         # Headers only (10% outline)
  outline-30.md         # Supporting points (30% outline)
  research/             # Research findings
  introduction.md       # Hook, sinker, line
  draft.md              # Full draft
  review-notes.md       # Editor review findings
```

State is tracked automatically. Resume any article across sessions.

---

## Quality gates

| Phase | Gate | Requirement |
|---|---|---|
| 2 | Thesis validity | Claude attempts a genuine objection — if none found, thesis is too obvious |
| 2 | Thesis-antithesis | Thesis must survive the writer's own self-examination |
| 3 | Header logic | H2s alone must tell the complete argument |
| 5 | 30% discipline | Outline word count must be under 30% of target article length |
| 6 | Pattern interrupt | First sentence must be unpredictable |
| 6 | Line continuity | Hook concept must return at 2+ points in the article |

---

## Tips for best results

- **Have an earned secret.** If you don't know something from direct experience that your audience doesn't, the process will stall in Phase 2. That's by design.
- **Know your reader.** Not "marketing professionals" — a specific person in a specific moment with a specific frustration.
- **Trust the outline phases.** Phases 3 and 5 feel slow but make drafting fast. The hard thinking happens in the outline, not the draft.
- **Stay skeletal in Phase 5.** The 30% outline is notes-to-self, not polished prose. If it reads like paragraphs, you've gone too far.
- **Read your own sources.** AI can find and summarize research, but AI summaries don't count as having read the source. Writers need to become researchers first.
- **Earn the introduction.** Phase 6 comes after research for a reason. You can't write a great hook until you deeply understand what you're arguing.

---

## Requirements

- Claude Code

---

## License

MIT — see [LICENSE](./LICENSE)

---

## About

Built by **Tim Metz** at **[Animalz](https://animalz.co)**.

- [LinkedIn](https://www.linkedin.com/in/metztim/)
- [X/Twitter @timmetz](https://x.com/timmetz)
- [We Eat Robots](https://weeatrobots.substack.com/)
