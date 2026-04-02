<!-- SYNC: Personal version in writing-assistant/.claude/commands/write-rescue.md -->

# /write-rescue

Diagnose an existing draft or outline that isn't working, map it against the structured writing process, and set it up so `/write` can take over.

## Arguments

$ARGUMENTS — Required: path to the existing draft, outline, or notes. Can be a file path or a slug for an existing article folder.

## Core rules

1. **Read everything first.** Don't diagnose until you've read all provided material completely.
2. **Be honest.** If the piece has problems, name them clearly.
3. **Don't fix yet.** This command diagnoses. `/write` fixes.
4. **DO NOT use AskUserQuestion.** Use plain text prompts for natural conversation.

## Process

### Step 1: Read and assess

Read the provided material completely. Classify what exists:

| Element | Status |
|---|---|
| Thesis (stated or implied) | EXISTS / WEAK / MISSING |
| Earned secret | EXISTS / WEAK / MISSING |
| Structure (outline or headers) | EXISTS / WEAK / MISSING |
| Research (citations, data, examples) | EXISTS / WEAK / MISSING |
| Introduction (hook, sinker, line) | EXISTS / WEAK / MISSING |
| Draft (partial or complete) | EXISTS / WEAK / MISSING |

### Step 2: Map to process phases

Present a diagnostic table:

**[DIAGNOSIS]**

| Phase | Status | Evidence |
|---|---|---|
| 1. Foundation | SOLID / WEAK / MISSING | What exists or what's absent |
| 2. Thesis | SOLID / WEAK / MISSING | ... |
| 3. Structure | SOLID / WEAK / MISSING | ... |
| 4. Research | SOLID / WEAK / MISSING | ... |
| 5. 30% Outline | SOLID / WEAK / MISSING | ... |
| 6. Introduction | SOLID / WEAK / MISSING | ... |
| 7. Draft | SOLID / WEAK / MISSING | ... |
| 8. Review | NOT STARTED | ... |

### Step 3: Identify the failure point

Name the most likely reason the piece isn't working. Common patterns:

- **Thesis drift:** Started arguing one thing, ended arguing another. The piece lacks a single through-line.
- **Missing earned secret:** The argument is built on recycled advice anyone could write, not on authentic experience.
- **Outline-to-draft jump:** Went straight from rough idea to prose, skipping the hard structural thinking. The draft meanders.
- **Research gap:** Assertions without evidence. The argument feels thin or unsupported.
- **Hook failure:** Generic opening that doesn't grab. No pattern interrupt.
- **30% overshoot:** The outline became a rough draft. Too much detail too early killed the ability to see the structure.
- **Writer-centric structure:** Organized by how the writer figured things out, not how the reader needs to receive them.
- **Soft middle:** Tried to be both tactical and strategic. Neither lands.

Be specific: "The piece drifts from 'AI makes writers lazy' in section 1 to 'here's how to use AI well' by section 4. These are different articles."

### Step 4: Recommend path forward

Based on the diagnosis:
- **Which phase to restart from** — usually the earliest WEAK or MISSING phase
- **What to preserve** — strong elements that should carry forward
- **What to rework** — weak elements that need attention
- **What to discard** — sections that don't serve the thesis (even if well-written)

### Step 5: Set up for `/write`

1. Ask for a slug if one doesn't exist
2. Create `articles/{slug}/` if needed
3. Create `state.md` with:
   - Phases marked as `complete` where diagnosis was SOLID
   - `current_phase` set to the restart point
   - Thesis, audience, etc. populated from what exists
   - Process log entry documenting the rescue diagnosis
4. Move existing materials into the appropriate files (draft -> `draft.md`, outline -> `outline-10.md` or `outline-30.md`, etc.)

Then tell the user: "Run `/write {slug}` to continue from Phase {X}."
