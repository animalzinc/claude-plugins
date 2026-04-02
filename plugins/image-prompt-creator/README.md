# Image Prompt Creator

**5-phase workflow for creating production-quality AI image generation prompts**

Handles brand consistency, concept exploration, Nano Banana (Google's AI image generator) prompt crafting, iterative revision, and organized saving.

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) at [Animalz](https://animalz.co)

---

## Overview

A `/image-prompt` skill that guides you through creating production-ready image prompts for Nano Banana (NB Pro and NB2). You describe what you need, select a brand for visual consistency, and Claude crafts a detailed narrative prompt with hex colors, composition directions, and anti-instructions. You generate in the Nano Banana web UI (Gemini app), share results back, and Claude reviews and helps iterate until you're happy.

Includes a comprehensive Nano Banana prompting guide covering model selection, prompting principles, resolution strategy, and iteration techniques.

## Quick start

Install the plugin:

```bash
/plugin install image-prompt-creator
```

Start a new image prompt:

```bash
/image-prompt
```

Start with a brand and description:

```bash
/image-prompt acme "featured image for blog post about API security"
```

---

## The 5 phases

| Phase | Name | Goal | Output |
|---|---|---|---|
| 1 | **Brief** | Select brand, describe image need, gather references | Confirmed brief with brand, intent, aspect ratio |
| 2 | **Concept** | Explore visual direction (skipped if concept is clear) | Selected concept in 2-3 sentences |
| 3 | **Prompt craft** | Write production-ready Nano Banana prompt | Setup block + self-contained prompt + iteration notes |
| 4 | **Generate & Iterate** | User generates, Claude reviews, revise until happy | Approved final image |
| 5 | **Save** | Name, file, and document the image and prompt | Saved image + optional prompt log |

Each phase has checkpoints. No skipping.

---

## How brands work

The brand system ensures visual consistency across all images for a given brand. Each brand lives in `brands/{slug}/` with:

```
brands/{slug}/
  brand-config.md           # Colors (hex), typography, style, anti-patterns
  references/               # Curated style references from past images
    featured-blog-images/   # Organized by image type
    social-graphics/
  exports/                  # Final images (optional save location)
  *.pdf, *.png              # Visual assets to attach to Nano Banana
```

The `brand-config.md` is the key file. It tells Claude exactly which hex codes to use, what illustration/photo style to follow, and what to avoid. Every prompt is cross-checked against it before being presented.

---

## Adding a brand

1. Create `brands/{slug}/` (use a URL-friendly slug like `acme-corp`)
2. Add visual assets: brand guidelines PDF, color palette image, logo files, typography reference, mascot/character images, style references
3. Create `brand-config.md` using the template in `brands/README.md`

The template covers: colors (primary, secondary, neutrals with hex codes), typography, logo usage, mascots/critters, illustration style, photographic style, reference image mapping, and anti-patterns.

**Tips:**
- Be specific about hex codes — "#0CAFDF" not "blue"
- The anti-patterns section prevents common failure modes (e.g., "no corporate stock photo aesthetic")
- You don't need every section. Omit what doesn't apply.
- As you create images, save good ones to `references/` to build up style consistency over time

---

## What's in the box

| File | Purpose |
|---|---|
| `skills/image-prompt/SKILL.md` | The main skill — 5-phase guided workflow |
| `docs/nano-banana-guide.md` | Comprehensive prompting guide: NB Pro vs NB2, principles, resolution, iteration |
| `brands/README.md` | Brand config template and setup instructions |
| `examples/illustrated-prompt.md` | Annotated example: illustrated blog featured image |
| `examples/photographic-prompt.md` | Annotated example: photographic ad creative |

---

## Image types supported

- Blog featured images (illustrated or photographic)
- In-article diagrams and infographics
- Social media graphics (LinkedIn, Twitter/X)
- Ad creatives (photographic scenes, conceptual)
- Landing page visuals
- Presentation graphics
- Newsletter header images

---

## Tips for best results

- **Provide source material.** Article text, briefs, or even rough ideas give Claude more to work with for visual metaphors.
- **Reference images help a lot.** Competitors, mood boards, or style references dramatically improve first-generation quality.
- **Expect 2-3 rounds.** First generation is rarely final. The skill is designed for iteration.
- **Build your brand references.** After each successful image, save it as a style reference. Future prompts will be more consistent.
- **Use the examples.** Read `examples/` before your first run to understand the prompt style and level of detail expected.
- **Type `help` during the brief.** If you're unsure what input to provide, the skill shows detailed guidance on input types and image types.

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
