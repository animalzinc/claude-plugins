# Copywriting Coach

**Structured 7-phase copywriting process for short-form conversion copy**

Human writes, AI coaches. Built on Harry Dry's Three Laws, Luke Sullivan's advertising principles, and Joanna Wiebe's Money Words framework.

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) at [Animalz](https://animalz.co)

---

## Overview

A `/copywrite` slash command that guides you through a structured copywriting process for landing pages, ads, emails, taglines, social posts, and product descriptions.

The core philosophy: **the human fills the blank page.** Claude acts as a copywriting coach — questioning, challenging, and testing quality — but never originates the core message. The command compensates for what AI lacks (taste, conviction, lived experience) by front-loading human input and using AI for quality enforcement.

## Quick start

Install the plugin:

```bash
/plugin install copywriting-coach
```

Start a new project:

```bash
/copywrite saas-landing-page
```

Resume the most recent project:

```bash
/copywrite
```

---

## The 7 phases

| Phase | Name | Goal | Output |
|---|---|---|---|
| 1 | **Brief** | Define deliverable, audience, attitude shift | `brief.md` |
| 2 | **Strategy** | Find core truth, define SOCO/SOCA | `strategy.md` |
| 3 | **Research** | Competitive landscape, customer language, reference copy | `research/` |
| 4 | **Exploration** | Generate volume — human writes 15+ variants | `variants.md` |
| 5 | **Selection** | Apply three laws, Money Words check, pick winners | Updated `variants.md` |
| 6 | **Full Copy** | Write the complete deliverable in context | `copy.md` |
| 7 | **Review** | Ruthless refinement — every word earns its place | `review-notes.md` |

Each phase has quality gates that must pass before advancing. No skipping.

---

## Copy types supported

- **Landing page** — hero section or full page (hero + features + proof + CTA)
- **Ad** — headline + body + CTA (print, social, billboard)
- **Email** — subject line + preview text + body + CTA
- **Tagline / slogan** — standalone phrase
- **Social post** — platform-native format
- **Product description** — feature or benefit-focused

Phase 6 adapts its structure based on the copy type selected in Phase 1.

---

## Coach mode

Two modes control how proactive Claude is with suggestions:

| Mode | Behavior | Default? |
|---|---|---|
| **Strict** | Claude asks and waits. You always propose first. Claude only reacts: challenging, testing, pushing back. | Yes |
| **Helpful** | Claude can offer suggestions alongside questions and participate as a thinking partner. | No |

Toggle anytime during the process:
- "switch to strict"
- "switch to helpful"

In strict mode, Claude never says "I think X would work" before you've offered your own version. In helpful mode, Claude may propose candidates alongside questions ("Based on the brief, a strong candidate might be X — but what's your instinct?").

---

## Project structure

Each project creates a folder with tracked state:

```
copy/{slug}/
  state.md              # Process state (YAML frontmatter + process log)
  brief.md              # Deliverable, audience, attitude shift, constraints
  strategy.md           # Core truth, SOCO, SOCA, positioning
  research/             # Competitive copy, VOC, references
  variants.md           # All variants with three-laws scoring
  copy.md               # Final copy
  review-notes.md       # Review findings (if reviewer used)
```

State is tracked automatically. Resume any project across sessions.

---

## Frameworks used

This command distills principles from 10+ copywriting experts into actionable quality gates:

**Harry Dry** (Marketing Examples) — The backbone of the evaluation framework. His three laws ("Can I visualize it? Can I falsify it? Can nobody else say this?") are applied to every variant in Phase 5. His volume mandate ("Write 20+ headlines. Gold only shows in the last few") drives Phase 4. Kaplan's Law ("Any word not working for you is working against you") powers the Phase 7 audit.

**Luke Sullivan** (*Hey Whipple, Squeeze This*) — The bar test and counterargument test anchor Phase 2 strategy. His concepting lenses (Invert, Exaggerate, Metaphor, Before/after, Omit, Reframe, Passage of time) unlock new directions when the human hits a wall in Phase 4. The visual-verbal rule ("never show what you're saying or say what you're showing") guides ad copy in Phase 6.

**Joanna Wiebe** (Copyhackers) — The Money Words framework drives Phase 5 evaluation: the You Rule (make the consumer the grammatical subject), "get" as a money word, "and" as a lose-money word, and the interference check against category clichés.

**Also:** Harry Beckwith ("If it's this hard to write the ad, the product is flawed"), Geoffrey Moore (positioning statement template), David Ogilvy (write a letter, not a stadium address), Joe Sugarman (two-line ad structure), Lisa Cron (visualization test), Kevin Kelly (start from the headline), Pete Barry (print as figure drawing of advertising).

---

## Quality gates

| Phase | Gate | Requirement |
|---|---|---|
| 2 | Bar test | Core truth passes Sullivan's bar test — not generic marketing speak |
| 2 | SOCO singularity | No "and," "but," "or" in the SOCO — one message only |
| 3 | Competitive intelligence | 3+ competitors' actual copy collected, category clichés listed |
| 3 | Customer language | Real customer/prospect language captured |
| 4 | Volume | 20+ total variants, 15+ human-generated |
| 4 | Diversity | 3+ different angles/approaches |
| 4 | Concreteness | All variants pass the Zoom In test |
| 5 | Systematic evaluation | Three laws table completed for all variants |
| 5 | Human selection | Human (not Claude) picks the finalists |

---

## Agents

| Agent | Role | Model |
|---|---|---|
| `copy-reviewer` | Fresh-context reviewer: three-laws check, Money Words audit, interference analysis, cut recommendations | Sonnet |

The copy-reviewer is optional — offered in Phase 7 for a fresh-eyes review of the finished copy.

---

## Tips for best results

- **Have a product truth.** If you don't know the truest thing about what you're selling, the command will stall in Phase 2. That's by design.
- **Know your audience.** Not "SaaS decision-makers" — a specific person in a specific moment.
- **Bring customer language.** The best copy uses the customer's own words. Bring quotes from sales calls, support tickets, reviews, or social media.
- **Commit to the volume.** Phase 4 asks for 15+ human-written variants. This is where the real work happens. Don't rush it.
- **Start in strict mode.** It's harder, but it forces better thinking. Switch to helpful mode if you genuinely need a thinking partner.

---

## Requirements

- Claude Code

---

## Examples

See [EXAMPLES.md](./EXAMPLES.md) for detailed walkthroughs.

---

## License

MIT — see [LICENSE](./LICENSE)

---

## About

Built by **Tim Metz** at **[Animalz](https://animalz.co)**.

- [LinkedIn](https://www.linkedin.com/in/metztim/)
- [X/Twitter @timmetz](https://x.com/timmetz)
- [We Eat Robots](https://weeatrobots.substack.com/)
