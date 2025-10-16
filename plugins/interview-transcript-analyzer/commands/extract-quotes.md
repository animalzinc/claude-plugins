---
description: Find representative quotes on specific topics from interview transcripts
argument-hint: [topic] [transcripts-directory] [--max-quotes]
---

# Extract Quotes by Topic

Find the most representative and compelling quotes about a specific topic from interview transcripts.

## Step 1: Scan Transcripts

**Search directory $2 for transcripts:**
- Identify all transcript files
- Count total transcripts available

**Report to user:**
```markdown
## 📁 Transcripts Found

**Directory:** $2
**Transcripts:** [number] files

**Topic to search:** "$1"

Proceeding to extract relevant quotes...
```

---

## Step 2: Extract Relevant Quotes

Use the **quote-selector** agent to:

**For each transcript:**
1. Search for mentions of topic "$1" (and related terms)
2. Extract full quote with context
3. Rate quote quality (clarity, insight value, brevity)
4. Include speaker/participant attribution if available

**Quote selection criteria:**
- **Relevant** - Directly addresses the topic
- **Insightful** - Reveals something meaningful
- **Clear** - Standalone understandable
- **Concise** - Not overly long (prefer 1-3 sentences)
- **Authentic** - Conversational tone preserved

---

## Step 3: Rank and Present Quotes

**Default: Show top 10 quotes**
**If --max-quotes specified: Show that many**

**Present to user:**
```markdown
## 💬 Quotes About: "$1"

Found [total number] relevant quotes across [number] transcripts.
Showing top [$3 or 10] by quality score.

---

### Quote 1 (Score: [X]/10)
> "[Full quote text]"

**Source:** [Transcript name / Participant ID]
**Context:** [Brief context if helpful - when/why this was said]

---

### Quote 2 (Score: [X]/10)
[Same format...]

---

## Quote Categories

**By theme:**
- [Sub-theme 1]: [count] quotes
- [Sub-theme 2]: [count] quotes

**By sentiment:**
- Positive: [count]
- Negative/Pain point: [count]
- Neutral: [count]

---

## Usage Tips

**To find more quotes:**
```bash
/extract-quotes "[topic]" [directory] --max-quotes 20
```

**To search related terms:**
```bash
/extract-quotes "pricing or cost or budget" [directory]
```
```

---

## Step 4: Optional - Export Quotes

**Ask user:**
```
Would you like to:
1. Save these quotes to a file (quotes/$1-quotes.md)
2. Copy to clipboard for pasting elsewhere
3. Just view them here
```

**If user chooses save:**
- Create `quotes/` directory if needed
- Save as `quotes/$1-quotes.md` with all quotes in markdown format

---

## Error Handling

**If topic not found in any transcript:**
```
⚠️ No quotes found for topic: "$1"

Suggestions:
- Try broader search terms
- Check transcript file names to ensure they're included
- Try related terms: /extract-quotes "[alternative terms]"
```

**If no transcripts in directory:**
```
❌ No transcripts found in: $2

Please ensure:
- Directory path is correct
- Transcripts are in .txt or .md format
```

---

## Usage Examples

```bash
# Find quotes about pricing
/extract-quotes pricing ./interviews/

# Find more quotes with custom limit
/extract-quotes "product feedback" ./interviews/ --max-quotes 20

# Search multiple related terms
/extract-quotes "onboarding or getting started" ./customer-calls/
```

---

## Tips

**Effective search terms:**
- Single concepts: `pricing`, `features`, `support`
- Multi-word phrases: `"user experience"`, `"biggest challenge"`
- Related terms with OR: `"price or cost or budget"`

**Quote quality:**
- Scores 8-10: Exceptional quotes (use in presentations)
- Scores 6-7: Good quotes (use in reports)
- Scores 4-5: Useful context (reference material)
