---
description: Extract themes and insights from interview transcripts with intelligent agent scaling
argument-hint: [output-name] [transcripts-directory] [--context-file]
---

# Analyze Interview Transcripts

Analyze all interview transcripts in a directory, extract themes, rank insights, and generate a comprehensive report.

## Step 1: Discover and Validate Transcripts

**Scan the transcripts directory ($2):**
- Find all text files (.txt, .md, .doc, .docx)
- Count total transcripts
- Calculate total file size and estimated token count
- Identify any context files (ICP, research goals, methodology docs)

**Look for context file ($3):**
- If --context-file argument provided, read that file
- If not provided, look for common files in directory:
  - `icp.md` or `ideal-customer-profile.md`
  - `research-goals.md` or `objectives.md`
  - `methodology.md`
  - `customer-profile.md` or `persona.md`

**Report to user:**
```markdown
## 📁 Transcripts Discovered

**Directory:** $2
**Transcripts found:** [number] files
**Total size:** [size in MB]
**Estimated tokens:** ~[number]k tokens

**Files:**
- [filename 1] ([size])
- [filename 2] ([size])
- [etc.]

**Context documents found:**
- [ICP/research goals/methodology if found, or "None"]

Would you like to proceed with analysis?
```

**Wait for user confirmation.**

---

## Step 2: Determine Agent Scaling Strategy

Based on workload, intelligently determine how many parallel agents to use:

**Agent Scaling Logic:**

```
If 1-3 transcripts:
  → Use 1 agent (sequential analysis is fine)

If 4-8 transcripts:
  → Use 3 parallel agents
  → Divide transcripts evenly (e.g., Agent 1: transcripts 1-3, Agent 2: 4-6, Agent 3: 7-8)

If 9-15 transcripts:
  → Use 5 parallel agents
  → Divide transcripts evenly

If 16+ transcripts:
  → Use 8 parallel agents (optimal for most systems)
  → Divide transcripts evenly

ALSO consider total token count:
If total tokens > 150k:
  → Increase agent count by 1-2
  → Example: 6 transcripts but 200k tokens → use 5 agents instead of 3

If total tokens < 30k:
  → Decrease agent count
  → Example: 10 short transcripts with 25k tokens → use 3 agents instead of 5
```

**Present strategy to user:**
```markdown
## 🤖 Agent Strategy

Based on [number] transcripts totaling ~[number]k tokens, I recommend using **[number] parallel agents** for efficient analysis.

**How it works:**
- Each agent will analyze [number] transcripts
- Agents work simultaneously (faster than sequential)
- All findings will be synthesized into final report

**Agent assignments:**
- Agent 1: [transcript names]
- Agent 2: [transcript names]
- [etc.]

**Estimated time:** [minutes] minutes

Would you like to:
1. ✅ Proceed with this strategy
2. 🔄 Adjust agent count (tell me your preference)
3. ❌ Cancel
```

**Wait for user approval or adjustment.**

---

## Step 3: Launch Theme Extraction Agents

For each agent, use the Task tool with the **theme-extractor** agent:

**Provide each agent with:**
- Its assigned transcripts (full text)
- Context file contents (if available)
- Instructions to identify 3-5 major themes
- Request supporting quotes for each theme

**Track progress:**
```markdown
## 🔍 Extracting Themes

- ✅ Agent 1: Complete (found 4 themes)
- ✅ Agent 2: Complete (found 5 themes)
- 🔄 Agent 3: In progress
- ⏳ Agent 4: Pending
- ⏳ Agent 5: Pending
```

**Once all agents complete, collect results:**
- All themes from all agents
- Supporting quotes
- Frequency counts (how many transcripts mentioned each theme)

---

## Step 4: Synthesize and Rank Themes

Use the **insight-ranker** agent to:

**Consolidate themes:**
- Merge duplicate/similar themes across agents
- Example: "Pricing concerns" + "Cost barriers" → "Pricing and cost concerns"

**Rank themes by:**
1. **Frequency** - How many transcripts mentioned it
2. **Relevance** - Alignment with ICP/research goals (if context provided)
3. **Impact** - Magnitude of the insight (pain point severity, opportunity size)

**Present ranked themes to user:**
```markdown
## 🎯 Top Themes Identified

### Theme 1: [Theme Name]
**Mentioned in:** [X] of [Y] transcripts ([percentage]%)
**Relevance:** [High/Medium/Low based on ICP]
**Key insight:** [One sentence summary]

**Representative quote:**
> "[Quote from transcript]"
> — Participant [number/name]

---

### Theme 2: [Theme Name]
[Same format...]

---

[Continue for top 5-7 themes]

---

**Would you like me to:**
1. ✅ Proceed with final report generation
2. 🔎 Deep dive into specific themes (tell me which ones)
3. 🔄 Re-rank themes with different criteria
```

**Wait for user feedback.**

---

## Step 5: Generate Comprehensive Report

Create a structured markdown report with:

### Report Structure

```markdown
# Interview Analysis Report: [Output Name]

**Analysis date:** [Date]
**Transcripts analyzed:** [Number]
**Context:** [ICP/research goals summary if available]

---

## Executive Summary

[2-3 paragraph overview of most important findings]

---

## Methodology

**Transcripts:**
- [List of transcripts with dates if available]

**Analysis approach:**
- [Number] parallel agents
- Theme extraction and consolidation
- Ranking by frequency and relevance

**Context documents:**
- [List context files if used]

---

## Key Themes

### 1. [Theme Name] ([frequency]% of interviews)

**Summary:** [Detailed explanation of this theme]

**Why it matters:** [Relevance to ICP/business goals]

**Supporting quotes:**
1. "[Quote]" — Participant [ID]
2. "[Quote]" — Participant [ID]
3. "[Quote]" — Participant [ID]

**Recommendations:**
- [Actionable insight 1]
- [Actionable insight 2]

---

[Repeat for each major theme]

---

## Cross-Cutting Insights

[Patterns that span multiple themes]

---

## Recommendations

1. **[Priority]** [Recommendation based on findings]
2. **[Priority]** [Recommendation based on findings]
[etc.]

---

## Appendix: All Themes

[Comprehensive list of all themes found, including lower-frequency ones]

---

**Analysis performed by:** Interview Transcript Analyzer plugin for Claude Code
**Generated:** [Timestamp]
```

**Save report to:** `analysis/$1-analysis.md`

---

## Step 6: Deliver Results

**Report to user:**
```markdown
## ✅ Analysis Complete!

**Report location:** analysis/$1-analysis.md
**Transcripts analyzed:** [number]
**Themes identified:** [number] major themes, [number] total
**Top insights:** [number]

**Report sections:**
- Executive Summary
- Methodology
- [Number] Key Themes (with quotes and recommendations)
- Cross-cutting insights
- Actionable recommendations

**Next steps:**
1. Review the full report
2. Use `/extract-quotes [theme]` to find more quotes on specific themes
3. Use `/rank-insights` to re-rank with different criteria
```

---

## Error Handling

**If no transcripts found:**
```
❌ No transcripts found in directory: $2

Please ensure:
- Directory path is correct
- Transcripts are in supported formats (.txt, .md, .doc, .docx)
- Files are readable

Expected structure:
  interviews/
    ├── interview-1.txt
    ├── interview-2.txt
    └── context/
        └── icp.md
```

**If context file specified but not found:**
```
⚠️ Warning: Context file not found: $3

Would you like to:
1. Proceed without context (insights won't be ranked by ICP relevance)
2. Specify a different context file
3. Cancel and add context file first
```

**If agent fails during analysis:**
- Save partial results from completed agents
- Report which agent failed and why
- Offer to retry with fewer agents or different allocation

---

## Usage Examples

```bash
# Basic analysis
/analyze-interviews customer-feedback ./interviews/

# With ICP context for relevance ranking
/analyze-interviews product-research ./research/transcripts/ --context-file ./research/icp.md

# Large-scale analysis (automatically uses more agents)
/analyze-interviews enterprise-study ./enterprise-interviews/
```

---

## Tips for Best Results

**Organize transcripts clearly:**
- Use descriptive filenames (`interview-customer-name.txt`)
- Include dates if relevant (`2024-01-15-interview-acme-corp.txt`)
- Keep transcripts in dedicated directory

**Provide context:**
- ICP document helps rank insights by relevance
- Research goals ensure findings align with objectives
- Methodology doc helps interpret findings appropriately

**For large datasets:**
- The plugin will automatically scale agents (no manual config needed)
- More transcripts = more agents = faster analysis
- Expected speed: ~15-20 transcripts in 15-20 minutes with 8 agents
