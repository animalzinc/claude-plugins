<!-- SYNC: Source at animalz-intelligence-os/modules/image-prompt-creator/.claude/skills/image-prompt/SKILL.md -->
---
name: image-prompt
description: "Create production-quality image generation prompts for Nano Banana (Google's AI image generator). Guides through brand selection, concept exploration, prompt crafting, and iterative revision. Use when asked to 'create an image prompt', 'make a featured image', 'generate image for blog', or similar."
---

# Image Prompt Creator

Create production-quality image generation prompts for Nano Banana (Google's AI image generator).

$ARGUMENTS — Optional: brand name, or description of what's needed. If empty, start from brand selection.

## Plugin root

This skill is part of the `image-prompt-creator` plugin. Resolve all relative paths (`brands/`, `docs/`, `examples/`) from the plugin root — the directory containing this skill's `skills/` folder.

At the start: read `docs/nano-banana-guide.md` for prompting reference. Keep it loaded throughout.

---

## Phase 1: Brief

### Step 1 — Brand selection

List available brands by scanning `brands/*/brand-config.md`. Present them:

> **Which brand are you creating images for?**
> Available: {list of brand names from folder names}
> Or type a new brand name to set one up.

Always pause for the user to confirm — even if only one brand exists. The user may want to add a new brand or may have opened the skill by mistake.

If no brands exist yet, tell the user:

> **No brands configured yet.** Let's set one up. What's the brand name? I'll create the folder and guide you through the brand config. See `brands/README.md` for the full template.

If the user names a brand that doesn't exist yet, guide them through creating `brands/{slug}/brand-config.md` using the template in `brands/README.md`.

Read the selected `brands/{name}/brand-config.md`. Also check if `brands/{name}/references/` exists and scan for subfolders (e.g., `featured-blog-images/`, `social-graphics/`). These are curated style references from previous successful images — use them to inform your prompt writing and optionally recommend attaching them as style references.

If $ARGUMENTS includes a brand name, still confirm it but don't ask from scratch.

### Step 2 — Input intake

Ask:

> **What do you need?** Describe your image — what it's for, any ideas you have, and what source material you can share.
>
> Examples: "featured image for this blog article", "social ad showing our product", "infographic visualizing this data", "I have a rough idea for an illustration."
>
> You can provide article text, documents, other images, voice notes, or just a rough idea. Type `help` for more guidance.

If the user types `help`, show this expanded guidance:

> **Input types you can provide:**
> - Article or document text (paste or attach) — I'll extract visual metaphors and concepts
> - A specific concept or visual idea — I'll go straight to crafting the prompt
> - A vague direction ("something about growth" or "needs to feel technical") — I'll propose concepts
> - Reference images — competitors, mood boards, styles you like
> - Voice memo transcript — describe your idea verbally
> - An existing draft prompt you want improved
>
> **Image types you can create:**
> - Blog featured images (illustrated or photographic)
> - In-article diagrams and infographics
> - Social media graphics (LinkedIn, Twitter/X)
> - Ad creatives (photographic scenes, conceptual)
> - Landing page visuals
> - Presentation graphics
> - Newsletter header images
>
> **How this works:**
> After you share your input, I'll either go straight to crafting a prompt (if your concept is clear) or propose 3-4 visual concepts for you to choose from. Then I'll write a production-ready Nano Banana prompt with brand colors, composition details, and iteration notes.

If $ARGUMENTS includes a description, use it as the input and skip the question.

### Step 3 — Reference images

If the user hasn't mentioned reference images, ask:

> **Do you have any reference images to include?** These could be style references, mood boards, competitor examples, or related visuals. They're optional but help a lot for style consistency.
>
> If yes, share them and describe what each one should be used for (style reference, color reference, layout reference, etc.).

Also check the brand's `references/` folder. If reference images exist for the relevant image type (e.g., `references/featured-blog-images/` for a blog hero), mention them:

> I found {N} reference images in the brand folder for {image type}. I'll use these to inform the style direction, and may recommend attaching one as a style reference to Nano Banana.

### Checkpoint

Before proceeding, confirm:
- Brand: {name}
- Image intent: {what it's for, where it will appear}
- Concept clarity: {clear concept vs. needs exploration}
- Reference images: {listed with roles, or "none"}
- Aspect ratio: {derived from placement — 16:9 for blog hero, 4:3 for inline, etc.}

---

## Phase 2: Concept (conditional)

**If the user provided a clear visual concept:** Summarize it back in 2-3 sentences. Confirm. Move to Phase 3.

**If the concept is vague or the user wants ideas:** Generate 3-4 concepts. For each:

> **Concept {A/B/C/D}: "{Short title}"**
> {2-3 sentence visual description — what the viewer would see}
> Type: {illustrated / photographic / diagrammatic}
> Why: {How this concept serves the content and brand}

Draw on the source material (article text, brief, etc.) to find visual metaphors. Consider both illustrated and photographic approaches.

Ask the user to pick one or combine elements from multiple concepts.

### Checkpoint

Confirm the selected concept in 2-3 sentences before proceeding.

---

## Phase 3: Prompt craft

### Step 1 — Write the prompt

Craft a complete, production-ready Nano Banana prompt. The output has two parts:

**Part 1 — Setup block** (for the user's reference, NOT pasted into Nano Banana):

> **Reference images to attach:**
> 1. `{filename}` — {what it is}
> 2. `{filename}` — {what it is}
> 3. `{filename}` — {what it is}
>
> **Resolution:** {2K start -> 4K upscale}
> **Aspect ratio:** {ratio} ({placement context})

Pull from brand config's "Reference images to attach" table + any user-provided references + curated references from the brand's `references/` folder. Use your judgment on whether to include style references from the brand folder — they're powerful but risk over-indexing if the model copies them too literally.

**Part 2 — The prompt** (self-contained, copy-pasteable into Nano Banana):

The prompt must be completely self-contained. The user should be able to copy-paste it as one block. Structure it as:

1. **Opening paragraph — image role descriptions.** Tell Nano Banana what each attached image is for. Example: "I'm attaching three reference images. Image 1 is my color palette — use these exact hex codes. Image 2 shows my brand's character designs — match this line art style for any animal characters. Image 3 is a style reference only — match its illustration technique but do not copy its subject or composition."

2. **The scene description** — narrative sentences following the prompting principles from the guide:
   - Style direction (line work, color approach, mood)
   - Composition with spatial language (proportions, layout zones)
   - All colors by hex code from brand config
   - Mood and tone direction
   - Anti-instructions (what to avoid, what NOT to include)
   - Format and cropping notes

**After the prompt, add iteration notes** (for the user's reference, NOT pasted):
- What to check after Round 1
- Likely Round 2 adjustments
- Any known model quirks

### Step 2 — Brand enforcement

Before presenting the prompt, cross-check against `brand-config.md`:
- All hex codes match the brand palette (no made-up colors)
- Style vocabulary aligns with brand guidelines
- Mascot/critter usage matches brand guidelines
- Anti-patterns from brand config are covered in anti-instructions

### Checkpoint

Present the full output (setup block + prompt + iteration notes) to the user. Ask for feedback. Revise if needed. Continue revising until the user approves.

---

## Phase 4: Generate & Iterate

The user generates images in the Nano Banana web UI (Gemini app) using the prompt from Phase 3. This phase is a revision loop that continues until the user is happy.

### Step 1 — First generation

Tell the user:

> **Ready to generate.** Copy the prompt above into Nano Banana and attach the reference images listed in the setup section. Once you have the result, share the image here and I'll review it with you.

### Step 2 — Review the result

When the user shares the generated image:

1. **Your assessment.** Examine the image against the prompt and brand config. Look for:
   - Color accuracy (do hex codes match the brand palette?)
   - Composition (does the layout match the spatial description?)
   - Text legibility (if applicable — correct spelling, readable?)
   - Style adherence (matches the brand's aesthetic?)
   - Element accuracy (right number of items, correct content?)
   - Anti-pattern violations (anything that conflicts with brand config?)
   - Overall mood and quality

2. **Present findings.** Share what works and what needs fixing. Be specific:
   > **What works:** {specific positives}
   > **Issues to fix:** {numbered list of specific problems}

3. **Ask the user** if they see anything else they want changed. Combine your notes with theirs.

### Step 3 — Decide: iterate in conversation or new prompt?

This is a judgment call. Use these criteria:

**Stay in the same Nano Banana conversation (feedback prompt)** when:
- The composition and overall concept are right
- Issues are localized (wrong color on one element, text needs repositioning, one element too large/small)
- You're fixing 1-3 specific things
- The mood and style are correct

**Create a new prompt (fresh Nano Banana conversation)** when:
- The overall composition or layout is wrong
- The style/mood missed the mark significantly
- There are 4+ issues spread across the whole image
- The model went in a fundamentally different direction than intended
- Previous iterations in the same conversation are degrading quality (model losing context)

### Step 4 — Execute the revision

**If staying in conversation:** Write a concise feedback prompt for the user to copy-paste into the existing Nano Banana conversation. Present it clearly:

> **Paste this into your current Nano Banana conversation:**
>
> {Direct, specific editing instructions}

**If starting fresh:** Write a revised full prompt (same two-part format: setup block + self-contained prompt). Explain what changed and why. The user starts a new Nano Banana conversation with the revised prompt and reference images.

### Repeat

After each revision, return to Step 2. Continue until the user says they're happy with the result. Don't rush — most images need 2-3 rounds.

Keep track of each iteration: note which images the user shared (file paths from their system) and what feedback was given. You'll need this for Phase 5.

When the user approves the final image, move to Phase 5.

---

## Phase 5: Save (4 steps)

Announce the phase and its steps:

> **Phase 5: Save.** Four quick steps: name & save the final image -> add as brand reference -> save iterations -> save the prompt.

### Step 1 — Save and name the final image

Identify the final image file (from the path the user shared during Phase 4). Propose a descriptive filename:

> **Let's save the final image.** I'd suggest naming it: `{slug}-{image-type}-{concept-hint}.png`
> (e.g., `reddit-aeo-featured-rug-pull.png`)
>
> Where should I save it?
> 1. **A project folder** — share the path and I'll copy it there
> 2. **The brand folder** — I'll save it to `brands/{name}/exports/`
> 3. **Both**
>
> Does the name work, or do you want something different?

After copying to the chosen location(s), delete the original from the temporary location (e.g., Downloads) since it's now saved. Also delete any earlier iteration files the user downloaded — they'll be offered in Step 3 if the user wants to keep them.

Wait for the user to respond before proceeding.

### Step 2 — Add as brand reference?

> **This image turned out well. Do you want to add it as a style reference for future {image type} images?** If yes, I'll copy it to `brands/{name}/references/{image-type}/`. Next time you or a team member runs `/image-prompt` for a {brand} {image type}, I can use it as a style reference.

Wait for the user to respond before proceeding.

### Step 3 — Save iterations?

List the iterations from Phase 4 with brief notes:

> **You generated {N} versions during this session:**
>
> | Version | Notes |
> |---|---|
> | v1 | {brief description} |
> | v2 | {brief description} |
> | ... | |
>
> Want me to save any of these? I'd rename them to: `{final-name}-v1.png`, `{final-name}-v2.png`, etc. and save them alongside the final.

If the user declines, confirm the iteration files have already been cleaned up from their temporary location.

Wait for the user to respond before proceeding.

### Step 4 — Save the prompt?

> **Finally, do you want to save the prompt and revision log?** This documents the full process — concept, prompt text, iteration feedback, and what we learned. Useful if you want to create a similar image later or share the approach with a team member.
>
> 1. **Local markdown file** — alongside the image in the same folder
> 2. **Save to your preferred tool** — if you have a project management tool or wiki connected, I can help format it for saving there
> 3. **Skip**

If saving locally, the document includes: concept description, setup (resolution, aspect ratio, reference images), the final prompt text, all iteration feedback prompts, and the revision log.

For local saves: use the same filename as the image but with `.md` extension.

---

## Rules

- **Never generate images yourself.** You craft prompts; the user generates images in the Nano Banana web UI (Gemini app) and shares results back.
- **Brand fidelity is non-negotiable.** Every hex code, style choice, and anti-pattern must match the brand config.
- **Narrative prompts only.** No keyword lists, no bullet-point prompts. Full sentences.
- **Prompts must be self-contained.** The user copies one block of text. Reference image descriptions go inside the prompt as an opening paragraph, not as separate labels.
- **Don't skip phases.** Brief -> Concept -> Prompt -> Generate & Iterate -> Save. Don't save until the user is happy.
- **Always pause for brand selection.** Even with one brand, let the user confirm or add a new one.
- **Always review generated images.** When the user shares a result, give your honest assessment alongside their feedback.
- **Iteration is expected.** Most images need 2-3 rounds. Don't treat revision as failure.
- **Know when to start fresh.** If in-conversation feedback isn't converging after 2-3 rounds, or the base composition is wrong, recommend a revised prompt in a new Nano Banana conversation.
- **Use brand reference images.** Check `brands/{name}/references/` for curated style references from previous successful images. Use them to inform your prompt writing and recommend attaching as style references when appropriate.
- **Clean up temp files.** After saving the final image to its destination, delete the original from temporary locations (Downloads, etc.). Do the same for discarded iterations.
- **Step through Phase 5.** Present each save step one at a time, wait for the user's response before proceeding to the next.
- **Reference the guide.** When recommending techniques, draw from `docs/nano-banana-guide.md`.
- **Read examples when needed.** If unfamiliar with the expected prompt style, read `examples/` for reference before crafting.
