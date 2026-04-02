# Adding a New Brand

## Steps

1. Create a folder: `brands/{customer-slug}/`
2. Add visual assets (whatever the brand has):
   - Brand guidelines PDF
   - Color palette image or screenshot
   - Logo files
   - Typography/font reference
   - Mascot/character reference images
   - Any style reference images
3. Create `brand-config.md` using the template below

## brand-config.md template

```markdown
# {Brand Name} — Visual Brand Config

## Colors

### Primary palette
| Name | Hex | Use |
|---|---|---|
| {Color name} | #{hex} | {Primary use} |

### Secondary palette
| Name | Hex | Use |
|---|---|---|
| {Color name} | #{hex} | {Use} |

### Neutrals
| Name | Hex | Use |
|---|---|---|
| {Color name} | #{hex} | {Use} |

## Typography

- **Headings:** {Font family, weight}
- **Body:** {Font family, weight}
- **Special:** {Any accent fonts}

## Logo

{Brief description of logo usage rules}

## Critters / mascots

{If applicable — describe characters, their colors, and drawing style}

## Illustration style

{Describe the brand's illustration aesthetic — line art vs. flat vector vs. 3D, color approach, mood}

## Photographic style

{Describe the brand's photo aesthetic — lighting, mood, composition preferences}

## Reference images to attach

| Image type | Attach | Label as |
|---|---|---|
| {Scenario} | {filename} | {How to label in prompt} |

## Anti-patterns

{What to avoid — styles, colors, aesthetics that conflict with the brand}
```

## Tips

- The `brand-config.md` is what the `/image-prompt` command reads. Keep it focused on what matters for image generation.
- Visual assets are for users to attach to Nano Banana as reference images — Claude doesn't read images each run.
- You don't need every section. If the brand doesn't have mascots, omit that section.
- Be specific about hex codes. "Blue" is ambiguous; "#0CAFDF" is not.
