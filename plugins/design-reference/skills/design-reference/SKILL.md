<!-- SYNC: Personal version at ~/.claude/skills/design-reference/SKILL.md -->
---
name: design-reference
description: "Iterative design research: brief → references → feedback → principles → prototype → approve. Use when starting a design phase for any frontend project, or when the user says things like 'design pass', 'design phase', 'collect references', 'design research'."
disable-model-invocation: false
allowed-tools: []
---

# Design reference

Structured design research process that builds visual direction from reference review and stakeholder feedback. Produces a `DESIGN_RESEARCH.md` document and an approved prototype.

**The problem this solves:** Design conversations tend to be vague ("make it look modern") or skip straight to prototyping without establishing shared visual language. This process forces explicit reference review and feedback capture before any prototyping begins.

## Arguments

$ARGUMENTS - Optional: path(s) to input files (voice memo transcripts, text notes, design brief). If not provided, ask user to describe their design direction.

## Core rules

1. **Never skip ahead.** No prototyping until principles are synthesized and approved (Step 5 complete).
2. **Capture everything.** Record exact quotes and specific reactions per reference. "Like the brightness" and "like the layout" are different signals — both matter.
3. **Always checkpoint.** Each step ends with explicit user confirmation before proceeding.
4. **Multiple rounds.** Always do at least 2 rounds of references. Round 1 = broad exploration. Round 2+ = focused based on Round 1 patterns.
5. **Accumulate patterns.** Maintain a running list of likes/dislikes/patterns that grows with each reference reviewed.

Display current step number prominently: `**[Step X/8: Name]**`

## Process

### Step 1: Receive brief

Read provided file(s) or ask user to describe their design direction. Extract:

- **Project type:** website, desktop app, mobile app, terminal UI, dashboard, etc.
- **Vibe/tone:** any aesthetic preferences mentioned (dark, bright, minimal, bold, etc.)
- **Anti-references:** anything explicitly disliked or to avoid
- **Functional constraints:** layout requirements, must-have elements, platform
- **Existing design context:** current visual state, colors in use, design system, related projects
- **Who uses it:** target audience

Summarize back in bullet points using the user's own words where possible.

**Checkpoint:** "Is this an accurate summary of your design direction? Anything to add or correct?"

### Step 2: Search references (Round 1)

Based on the brief and project type, use WebSearch to find 8-15 reference sites/apps. Search strategy:

- **Same category:** search for well-designed apps/sites in the same category (e.g., "best designed terminal apps 2026", "modern personal websites")
- **Adjacent category:** 2-3 references from adjacent categories that match the stated vibe (e.g., for a terminal app, also look at code editors and dev tools)
- **Anti-category:** if the user mentioned anti-references, avoid that aesthetic in searches
- **Vibe-matching:** if a specific tone was mentioned, search for apps known for that quality (e.g., "bright and bold app design", "minimal but warm interfaces")

For each reference found, use WebFetch to load the homepage/main page. Capture: what it is, visual style at a glance, why it's relevant to this brief.

Present the full list:

```
## Round 1 references (X found)

1. **Name** (url) — What it is. Visual style notes. Why included.
2. ...
```

**Checkpoint:** "Ready to review these one by one? I'll show you each and capture your reaction."

### Step 3: Per-reference review (Round 1)

Go through each reference one at a time. For each:

1. Present the reference name and URL
2. Ask: "What do you think of this one? Likes, dislikes, anything specific that catches your eye?"
3. Record feedback verbatim in this format:
   - **Name** (url) — "exact quote from user"
   - Likes: [specific elements praised]
   - Dislikes: [specific elements criticized]

After all references reviewed, present a pattern summary:

```
### Round 1 patterns
- [Pattern with evidence from specific references]
- ...

### Anti-patterns (consistently rejected)
- [Anti-pattern with evidence]
- ...
```

**Checkpoint:** "Do these patterns capture your preferences accurately? Anything I'm reading wrong?"

### Step 4: Focused references (Round 2+)

Based on Round 1 patterns, search for 4-8 more focused references. Explain the search rationale:

"Based on Round 1, you consistently liked [X] and disliked [Y]. Searching for references that are [specific direction]."

Repeat the per-reference review from Step 3 for each new reference.

After review, present the combined patterns from all rounds — what's strengthened, what's new, any contradictions.

If patterns are still unclear or contradictory, propose a Round 3 with even more focused references. Otherwise, move to synthesis.

**Checkpoint:** "Patterns feel solid enough to synthesize into principles? Or should we do another round?"

### Step 5: Synthesize design principles

Generate a numbered table of 8-12 design principles. Each principle must cite specific feedback as evidence:

| # | Principle | Evidence |
|---|-----------|----------|
| 1 | **[Principle name]** | [Specific quote/reference that supports this] |
| 2 | ... | ... |

Follow the principles table with:

**Visual direction** — a prose paragraph covering:
- Color palette direction (with specific inspiration sources)
- Layout pattern (with reference to which app inspired it)
- Typography direction
- Key "avoid" list (sourced from anti-references and rejections)

**Top references ranked** — the 5-7 most relevant references ranked by relevance, with a one-line rationale each.

**Checkpoint:** "Review these principles carefully. Each one will guide the prototype. Want to adjust, add, or remove any?"

### Step 6: Prototype

Ask user which prototyping approach they prefer:

- **A: HTML prototype** — create a self-contained HTML file for quick visual reference
- **B: Framework prototype** — build in the project's existing framework (React, Vue, etc.)
- **C: Other** — user describes a different approach

Whichever approach:

1. Pass the full design principles, visual direction, and top references as context
2. Request 4 variations for the first round (broad exploration of the design space within the approved principles)
3. Present all variations and capture detailed feedback per variation

**Checkpoint:** "Which variation is closest? What would you change?"

### Step 7: Iterate prototype

Based on Step 6 feedback, refine. Typical iteration pattern:

- **Round 2:** 2 variations, focused on the preferred direction with specific changes requested
- **Round 3+:** 1-2 variations, fine-tuning details

After each round, capture:
- What improved
- What regressed (flag regressions explicitly — they happen and must be caught)
- What still needs work

Continue until user signals satisfaction.

**Checkpoint:** "Is this the approved design? If yes, I'll document everything."

### Step 8: Save artifacts

Create a `docs/planning/` directory in the project if it doesn't exist.

**Always create: `docs/planning/DESIGN_RESEARCH.md`**

Use this structure:

```markdown
# Design Research: [Project Name]

## Design direction (from brief)
[Bullet points from Step 1, using user's own words]

---

## Reference review: Round 1

[Per-reference feedback from Step 3, format:]
- **Name** (url) — "user's quote"

### Round 1 patterns
[Pattern summary]

---

## Reference review: Round 2

[Per-reference feedback from Step 4]

### Round 2 patterns
[Updated combined pattern summary]

---

## Synthesized design principles

| # | Principle | Evidence |
|---|-----------|----------|
[Full principles table from Step 5]

## Visual direction
[Prose paragraph from Step 5]

## Top references (ranked by relevance)
[Ranked list from Step 5]

---

## Prototype iteration

### Round 1
[Variations explored, per-variation feedback, decision]

### Round 2
[Refinements, feedback, decision]

### Round N (approved)
[Final refinements, what was approved and why]

---

## Approved design specification
[Layout decisions, design tokens/colors, typography, spacing, component-level notes, avoid list]
```

Present file paths and confirm.

**Checkpoint:** "Design research saved. Ready to move to implementation?"

## Notes

- Steps are a guide, not rigid — revisiting earlier steps is fine
- For projects with an existing design system (e.g., building a new feature within an established app), skip Steps 2-4 and derive principles from the existing system + new requirements
- The DESIGN_RESEARCH.md file is the source of truth for all subsequent design decisions. Reference it during implementation.
