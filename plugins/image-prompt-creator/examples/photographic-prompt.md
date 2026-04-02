<!-- SYNC: Source at animalz-intelligence-os/modules/image-prompt-creator/examples/photographic-prompt.md -->

# Example: Photographic Ad Creative

> This example shows the typical pattern for realistic photographic images used in ad campaigns — no text on the image, story told through composition.

## Setup

- **Brand:** Example brand with warm color palette
- **Model:** Nano Banana Pro (chosen for realistic photography and controlled composition)
- **Resolution:** 2K start, upscale final to 4K
- **Aspect ratio:** 16:9 (landscape, for social placement)
- **Reference images attached:**
  1. Brand colors page — labeled as "Warm palette and purple accent reference"
- **Critical guardrail:** "Do not include any text, words, logos, labels, or typography anywhere in the image."

## The prompt

> This image is for an ad campaign for a content marketing agency. The ad's message is: "Some of our clients won't even tell their board how their content gets made." The image needs to visually tell the story of someone guarding a secret in a boardroom. This is a standalone photograph that will be paired with a separate text caption. Do not include any text, words, logos, labels, or typography anywhere in the image.
>
> Generate a realistic photograph in 16:9 landscape format of a corporate boardroom during a meeting. The composition is centered on one person who is the clear focal point of the image. This person is standing or half-standing at the table, holding a leather briefcase tightly behind their back with both hands, arms wrapped around it — an exaggerated, theatrical hiding gesture, like a kid caught with stolen cookies. Their expression is a forced casual smile, trying too hard to look innocent. The briefcase should be large and clearly visible behind them — not tucked away, but obviously being concealed.
>
> The other four or five people around the conference table are completely absorbed in the meeting — looking at laptops, taking notes, mid-conversation — totally oblivious to the person's ridiculous hiding act. This contrast is the joke.
>
> The person hiding the briefcase should be positioned at the center of the frame. Shoot it like a comedy scene — the audience is in on the secret. Warm, golden-hour lighting through large windows. Modern boardroom with subtle purple accents in the decor (chair cushions, a folder, wall art). The mood is conspiratorial and funny — not subtle, not stock photo.

## What makes this prompt effective

- **Story context first:** Explains the ad message and intent before describing the image — helps the model understand WHY each element matters
- **Comedy direction:** "theatrical", "like a kid caught with stolen cookies", "not subtle, not stock photo" — gives clear emotional and tonal targets
- **Explicit no-text guardrail:** Repeated at the start, prevents the model from adding typography
- **Composition direction:** "centered on one person", "shoot it like a comedy scene" — uses filmmaking language
- **Brand integration through environment:** Purple accents in decor rather than forcing brand colors onto a photo
- **Contrast as narrative device:** The oblivious colleagues vs. the conspicuous hider IS the joke

## Iteration notes

- **Common issue:** Model may add text labels or logos despite the guardrail. Follow up with: "Regenerate the same scene but remove all text, words, and labels from the image."
- **Composition tweaks:** If the "hiding" gesture isn't exaggerated enough, specify: "The briefcase should be comically large and the hiding gesture extremely theatrical."

## Key differences from illustrated prompts

| Aspect | Illustrated | Photographic |
|---|---|---|
| Color specification | Exact hex codes throughout | Brand colors as environmental accents only |
| Reference images | Colors, critters, fonts pages | Colors page only (or none) |
| Text in image | Sometimes (labels, titles) | Never — text goes in captions |
| Style language | "hand-drawn line art", "soft muted fills" | "realistic photograph", "comedy scene" |
| Composition language | Spatial ("left quarter", "right third") | Cinematic ("center of frame", "shallow depth of field") |
