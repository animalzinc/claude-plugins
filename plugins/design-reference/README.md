# Design Reference

**Structured design research process that builds visual direction before prototyping**

Replaces vague design conversations with an iterative reference review that produces explicit principles and an approved prototype.

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) at [Animalz](https://animalz.co)

---

## What it does

A `/design-reference` skill that guides you through collecting visual references, capturing per-reference feedback, synthesizing design principles, and iterating on prototypes. The output is a `DESIGN_RESEARCH.md` document that serves as the source of truth for all subsequent design decisions.

## When to use it

- Starting a design phase for any frontend project
- You have a vague aesthetic direction ("modern", "clean", "bold") that needs to become specific
- Multiple stakeholders need to align on visual direction before building
- You want to avoid the "just make it look good" prototyping loop

## Quick start

Install the plugin:

```bash
/plugin install design-reference
```

Start a design research session:

```bash
/design-reference path/to/brief.md
```

Or start without a brief:

```bash
/design-reference
```

---

## The 8-step process

| Step | Name | What happens |
|---|---|---|
| 1 | **Brief** | Extract project type, vibe, constraints, audience |
| 2 | **Search references (Round 1)** | Find 8-15 reference sites/apps via web search |
| 3 | **Per-reference review** | Review each reference one by one, capture likes/dislikes/patterns |
| 4 | **Focused references (Round 2+)** | Search for 4-8 more references based on Round 1 patterns |
| 5 | **Synthesize principles** | Generate 8-12 design principles with evidence from feedback |
| 6 | **Prototype** | Create 4 variations using the approved principles |
| 7 | **Iterate** | Refine through focused rounds until approved |
| 8 | **Save artifacts** | Write `DESIGN_RESEARCH.md` with full research and approved spec |

Every step ends with a checkpoint. No skipping ahead -- principles must be approved before prototyping begins.

---

## Output

The process creates `docs/planning/DESIGN_RESEARCH.md` containing:

- Design direction from the brief
- Per-reference feedback from all rounds
- Pattern summaries
- Synthesized design principles table
- Visual direction (colors, layout, typography, avoid list)
- Ranked top references
- Prototype iteration log
- Approved design specification

---

## Tips

- **Be specific in feedback.** "I like the spacing" is more useful than "I like it." The process captures exact quotes, so specificity compounds.
- **Don't skip Round 2.** Round 1 is broad exploration. Round 2 is where preferences sharpen. The best principles come from focused references.
- **Use anti-references.** Knowing what you hate is as valuable as knowing what you like. Mention them in the brief.
- **Trust the checkpoint.** If principles feel wrong, say so. It's cheaper to fix principles than to iterate on a misdirected prototype.

---

## Requirements

- Claude Code
- WebSearch and WebFetch capabilities (for reference collection)

---

## License

MIT -- see [LICENSE](./LICENSE)

---

## About

Built by **Tim Metz** at **[Animalz](https://animalz.co)**.

- [LinkedIn](https://www.linkedin.com/in/metztim/)
- [X/Twitter @timmetz](https://x.com/timmetz)
- [We Eat Robots](https://weeatrobots.substack.com/)
