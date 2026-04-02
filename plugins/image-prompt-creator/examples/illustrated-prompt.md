<!-- SYNC: Source at animalz-intelligence-os/modules/image-prompt-creator/examples/illustrated-prompt.md -->

# Example: Illustrated Blog Featured Image

> This example shows the typical pattern for an illustrated featured image using a brand's custom style.

## Setup

- **Brand:** Example brand with hand-drawn illustration style
- **Model:** Nano Banana Pro (chosen for precise layout control and illustrated line art fidelity)
- **Resolution:** 2K start, upscale final to 4K
- **Aspect ratio:** 16:9 (blog hero placement)
- **Reference images attached:**
  1. Brand colors page — labeled as "Color palette reference — use these exact hex colors"
  2. Landing page hero illustration — labeled as "Mood/energy reference only — do NOT copy the botanical density or leaf shapes"

## The prompt

> A wide-format illustrated scene on a warm cream (#F9F7F6) background, showing a visual transition from left to right. The style is hand-drawn line art with soft, muted color fills — the line work should feel loose and human, not technical or diagrammatic.
>
> On the left quarter: a single clean prompt box drawn in light gray outline, with a few faint geometric shapes nearby — a small cube, a thin grid fragment, a couple of dotted lines drifting rightward. Sparse but composed.
>
> Moving rightward: the architecture builds and comes alive. Isometric shelves, containers, and platforms appear, connected by flowing purple (#6933CC) lines. Documents, folder icons, charts, and data nodes fill the structures. But the connections between elements aren't just straight lines — they curve and flow with energy, like streams or ribbons of teal (#32C8BE) and purple (#9463EE) winding between the geometric forms. Some of these flowing lines have small organic details — a curl at the end, a gentle wave, a subtle flourish — giving the whole system a sense of movement and life.
>
> On the right third: a dense, layered information architecture at full energy. Structures are stacked and interconnected, data flows visibly between them through those curving ribbon-like connections. Splashes of yellow (#FFD400) and peach (#FE844E) accent the documents and highlights. The flowing lines weave through and around the geometry, creating a sense of rhythm. A handful of small leaf or vine shapes (5-6 total) emerge naturally from the flowing lines — they feel like part of the movement, not decoration pasted on top.
>
> Line work in dark purple (#6933CC). Fills use lighter tints (#E9DFFB, #D2F9F6, #FCF5CF). The warm cream background should remain visible throughout — don't fill every gap.
>
> No text in the image. No animals or characters. The composition should work well when cropped to the right half or right two-thirds.

## What makes this prompt effective

- **Narrative structure:** Describes a scene with spatial progression (left to right), not a list of keywords
- **Hex colors from brand config:** Every color references the exact brand hex code
- **Style direction with boundaries:** "loose and human, not technical or diagrammatic" — tells the model what TO do and what NOT to do
- **Composition intent:** Explains how the image will be used (blog hero, cropped to right half)
- **Proportional language:** "left quarter", "right third" gives the model spatial targets
- **Anti-instructions:** "No text", "No animals", "don't fill every gap" prevent common failure modes

## Iteration notes

- **Round 1 result:** Layout was too flat/diagrammatic. Needed more flowing energy.
- **Round 2 feedback:** "Make the connecting lines more ribbon-like with curves and gentle waves. Add more variety in the flowing line shapes — not all the same curve."
- **Round 3:** Approved. Upscaled to 4K.

## Lessons learned

- Reference images for mood work well, but label them carefully to prevent the model from copying specific elements
- Botanical elements add warmth but can overwhelm — specify exact quantity ("5-6 total")
- A distinct background color is essential for brand recognition — explicitly mention it
