<!-- SYNC: Source at animalz-intelligence-os/modules/image-prompt-creator/docs/nano-banana-guide.md -->

# Nano Banana Prompting Guide

**Last updated:** 2026-03-26

---

## Model selection: NB Pro vs NB2

Two models available. Pick based on the image type.

### Nano Banana Pro (Gemini 3 Pro Image)
Best for complex compositions and photorealism. Use for:
- **Complex multi-subject scenes** with intricate lighting interactions, depth, and perspective
- **Structured diagrams** with precise element positioning (numbered cards, grids, flows)
- **Identity preservation** (consistent character faces across a series)
- **Clean layouts** with structured educational graphics
- **Illustrations requiring exact brand fidelity** (precise color matching, controlled compositions)

Note: Pro often garbles text — for text-heavy images, NB2 is actually better.

Trade-off: 10-20 seconds at 1K, 30-60 seconds at 4K. $0.045-$0.151/image via API (resolution-dependent).

### Nano Banana 2 (Gemini 3.1 Flash Image)
~95% of Pro's quality, 2-3x faster, half the cost. Default model in Gemini app since Feb 2026. Use for:
- **Text in images** — significantly better text rendering than Pro (accurate, legible, multi-language)
- **Photographic scenes** (realistic photography, ad creatives)
- **Illustrations** (mood pieces, featured images, abstract concepts)
- **Speed/cost priority** (rapid iteration, batch generation)
- **Image Search Grounding** needed (rendering real-world logos, landmarks, products)
- **Multi-character scenes** (subject consistency up to 5 characters, 14 objects)
- **Conversational editing** — strong at iterative refinements within a conversation

Trade-off: 2-5 seconds at 1K, 15-30 seconds at 4K. $0.022-$0.076/image via API (resolution-dependent, batch pricing).

### Decision shortcut

| Image type | Recommended model |
|---|---|
| Blog featured image (illustrated, brand style) | NB Pro (complex) or NB2 (simpler) |
| Blog featured image (photographic) | NB2 |
| In-article diagram with labels/text | NB2 (better text rendering) |
| In-article diagram (complex layout, no text) | NB Pro |
| Social media graphic with text | NB2 |
| Ad creative (photographic) | NB2 |
| Infographic with text labels | NB2 |
| Complex multi-subject photorealistic scene | NB Pro |
| Concept exploration / rapid iteration | NB2 |

When unsure: start with NB2. Escalate to Pro if quality is insufficient.

---

## Shared prompting principles

These apply to both models.

### 1. Narrative sentences, not keyword lists
Both models respond significantly better to descriptive natural language than keyword-style prompts.

**Good:** "A wide-format illustrated scene on a warm cream background showing layered isometric shelves connected by flowing purple lines"
**Bad:** "isometric, shelves, purple, cream background, illustrated, wide format"

### 2. Quote exact text and specify typography
Any text that should appear in the image must be wrapped in quotation marks in the prompt. Don't paraphrase or describe it. Also specify font style ("bold sans-serif", "elegant serif", "modern geometric font") and placement ("centered at top", "bottom left corner", "integrated into layout").

### 3. Label reference image roles
When attaching reference images, tell the model what each one is for: "Image 1 is the color palette. Image 2 is the typography reference. Image 3 is a style/mood reference only — do not copy specific elements."

### 4. Specify layout structure explicitly
Describe composition with spatial language: "left quarter", "center-right", "top row of 4 cards, bottom row of 3 centered". Don't leave layout to chance.

### 5. Name colors by hex code
When the brand config has exact colors, use them: "purple (#9463EE)", "dark purple line work (#6933CC)". Don't say "a nice purple."

### 6. Include anti-instructions
State what NOT to do: "No text in the image", "Do not copy specific elements from the reference", "Not corporate or sterile." Prevents common failure modes.

### 7. Plan for iteration
First generation is rarely final. Structure prompts knowing you'll refine in follow-up turns.

### 8. Keep text items short
Both models handle medium-length text. Dense paragraphs will fail. For text-heavy images, use short labels and titles.

### 9. Use photography/cinematography language (especially NB2)
NB2 responds exceptionally well to specific photographic language. Naming real cameras, film stocks, lenses, and lighting setups produces precise visual behavior:
- Film stock: "Kodak Portra 400" (one of the most powerful single instructions for mood)
- Lens: "shot with 85mm portrait lens", "wide-angle 24mm"
- Lighting: "golden-hour lighting", "Rembrandt lighting", "soft diffused window light"
- Camera angle: "Dutch angle", "low-angle perspective", "overhead flat lay"

Treat photographic prompts like briefing a cinematographer.

---

## Resolution strategy

### NB Pro
- **Start at 2K** for complex layouts (avoids timeout on text-heavy or multi-element images)
- **Upscale to 4K** after approving the base composition
- 4K on first attempt risks timeout for complex scenes

### NB2
- **Native 4K available** without the upscale workaround
- For simple compositions (photographic, single-subject): go straight to 4K
- For complex layouts (multiple elements, text): still safer to start at 2K and upscale
- Set resolution via `image_size` parameter, not by writing "4K" in the prompt (that doesn't change pixel dimensions)

### Aspect ratios
14 ratios supported via API: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9, auto.

Common use cases:
- **16:9** — blog heroes, landscape photos, ad creatives
- **4:3** — inline blog images, diagrams
- **1:1** — social media, profile images
- **9:16** — vertical/mobile, stories, reels
- **3:4** — vertical content, Pinterest
- **21:9** — ultra-wide banners, cinematic
- Be explicit in the prompt: "16:9 landscape format"

---

## NB2-specific features

### Thinking Mode
Three levels that trade speed for quality. Set via API parameter or model settings.

| Level | Speed | Best for |
|---|---|---|
| Minimal | Fastest | Quick iterations, concept exploration, simple compositions |
| Dynamic | Adaptive | General use — model decides how much to think based on complexity |
| High | Slowest | Complex scenes, precise compositions, when quality matters most |

Default is Minimal. Use Dynamic for general production work, High for complex scenes where quality matters most.

### Image Search Grounding
Pulls real-time reference images from Google Search during generation. NB2-only feature.

**When it helps:**
- Rendering real-world subjects (logos, landmarks, product packaging, public figures)
- When the prompt references specific real things the model might not have in training data

**When to disable:**
- You already have all reference images attached
- You want fully original/creative compositions
- Adding real-world references would conflict with brand style

### Subject consistency
NB2 can maintain character resemblance across images within a conversation:
- Up to 5 characters maintained consistently
- Up to 14 objects tracked for fidelity
- **Character sheet technique:** Generate a 360-degree character sheet first — multiple angles (front, left, right, back) in a single image. This gives the model a complete visual understanding to reference in follow-up prompts.
- Define character details (clothing, features, colors) in the first prompt, then reference by name in follow-ups
- Useful for: storyboards, series of social images, character-based campaigns

### Conversational editing
NB2 is strong at iterative edits within a conversation. Instead of regenerating from scratch:
- "Keep the composition but change the lighting to golden hour"
- "Replace the background with a neon-lit city street"
- "Remove the person on the left and extend the sidewalk"
- "Make the hiding gesture more exaggerated"

This works best when the base image is 80%+ correct — tweak rather than regenerate.

---

## NB Pro-specific notes

- Best with 6 or fewer reference images for high fidelity
- Fewer references = more focused output
- Do not attach example outputs as references (biases/constrains generation)
- Do not attach design briefs as separate documents — integrate instructions into the prompt
- Avoid search grounding when you already have all content (adds noise) — this is a Pro-specific issue since NB2 handles grounding more cleanly

---

## Iteration approach

### Round 1: Base generation
Generate with the full prompt. Evaluate:
- Layout and composition
- Color accuracy against brand
- Text legibility (if applicable)
- Overall mood and style

### Round 2: Refinement (usually needed)
Common follow-ups:
- Adjust font sizes for legibility
- Correct color matching to brand references
- Reposition elements ("move the card grid down", "make the character smaller")
- Fix text rendering issues
- Adjust density ("too cluttered" or "too sparse")

### Round 3: Polish (optional)
- Decorative element refinement
- Icon consistency
- Final composition tweaks
- Upscale to 4K if started at 2K

### Fallback: Two-stage approach
If the full prompt produces cluttered results (too much text, too many elements):
1. Generate layout only (composition, colors, shapes — no text)
2. Add text content in a follow-up turn

### Counting problem
Both models (and other AI image generators) struggle with exact counts. For numbered elements:
- Use structured grid layouts (4+3 rows) instead of radial/circular arrangements
- Explicitly number each element: "Card 1: Label A, Card 2: Label B..."
- Add: "IMPORTANT: There must be exactly N cards. No more, no less."
- Despite instructions, models may still generate wrong counts — be prepared to iterate

---

## What to avoid

### Both models
- Keyword-style prompts (use natural language)
- Example output images as references (biases the model)
- Splitting instructions across separate attachments (one unified prompt)
- Conflicting styles in one prompt ("pixel art and 4K photorealistic")
- Dense paragraphs of text in the image
- Writing "4K" or "HD" in the prompt to control resolution (use the `image_size` parameter)

### NB Pro specific
- 4K on first attempt for complex layouts (timeout risk)
- Search grounding when all content is already provided

### NB2 specific
- Relying on Image Search Grounding for brand-specific assets (it pulls generic results — attach your own)
- Expecting Pro-level precision on complex multi-subject compositions with intricate lighting
- Complex text rendering in non-Latin scripts (improved but still limited)
- Using Minimal thinking mode for production images that need high quality (switch to Dynamic or High)
