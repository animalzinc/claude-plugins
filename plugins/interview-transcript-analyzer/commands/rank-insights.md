---
description: Re-rank insights from previous analysis with different criteria
argument-hint: [analysis-file] [--criteria]
---

# Re-Rank Insights

Re-rank insights from a previous analysis using different criteria (frequency, impact, relevance, or custom).

## Step 1: Load Previous Analysis

**Read the analysis file ($1):**
- Parse all themes/insights from the file
- Extract frequency data
- Note any existing rankings

**Report to user:**
```markdown
## 📊 Analysis Loaded

**File:** $1
**Themes found:** [number]
**Current ranking:** [Current criteria if specified]

**Available themes:**
1. [Theme name] - Currently ranked #1
2. [Theme name] - Currently ranked #2
[etc.]

How would you like to re-rank these insights?
```

---

## Step 2: Select Ranking Criteria

**Present options to user:**
```markdown
## 🎯 Ranking Criteria Options

Choose how to rank insights:

1. **Frequency** - Most mentioned themes first
   - Best for: Understanding what came up most often
   - Data available: ✅

2. **Impact** - Highest impact/severity first
   - Best for: Prioritizing what to act on
   - Requires: Manual input or impact assessment

3. **Relevance to ICP** - Best fit with ideal customer profile
   - Best for: Focusing on target audience needs
   - Requires: ICP document for comparison

4. **Business Value** - Revenue/strategic opportunity size
   - Best for: ROI-focused prioritization
   - Requires: Business context assessment

5. **Ease of Implementation** - Quick wins first
   - Best for: Tactical planning
   - Requires: Feasibility assessment

6. **Custom** - Provide your own criteria
   - Example: "Rank by technical complexity" or "Rank by customer segment"

Which criteria would you like to use? [1-6 or describe custom]
```

**Wait for user selection.**

---

## Step 3: Apply Ranking Criteria

Based on user's choice:

### If Frequency (Option 1):
- Simply re-sort themes by mention count
- No additional analysis needed

### If Impact (Option 2):
Use the **insight-ranker** agent to:
- Review each theme
- Assess potential impact (pain point severity, opportunity size)
- Rank accordingly

### If Relevance to ICP (Option 3):
**Ask for ICP document:**
```
Please provide path to your ICP document, or I'll look for:
- icp.md
- ideal-customer-profile.md
- customer-profile.md
in the analysis directory
```

Then use **insight-ranker** agent to:
- Read ICP document
- Score each theme by alignment with ICP characteristics
- Rank by relevance score

### If Business Value (Option 4):
**Prompt user for context:**
```
To rank by business value, I need to understand:
1. Revenue impact indicators (which themes suggest upsell/retention opportunities?)
2. Strategic priorities (which align with company goals?)

Please provide:
- Business goals document, OR
- Quick description of strategic priorities

Or I can make best-effort assessment based on theme content.
```

### If Custom (Option 6):
**Ask user to clarify:**
```
Please describe your custom ranking criteria:
Example: "Rank by technical complexity, easiest first"
Example: "Rank by enterprise vs SMB relevance"
Example: "Rank by urgency based on competitive pressure"
```

Then use **insight-ranker** agent with custom instructions.

---

## Step 4: Present Re-Ranked Results

```markdown
## ✅ Insights Re-Ranked: [Criteria]

### New Ranking:

#### #1: [Theme Name]
**Previous rank:** #[old position]
**Score:** [Score based on criteria] / 10
**Why this ranking:** [Brief explanation of why it ranks here]

**Key insight:** [One sentence summary]

---

#### #2: [Theme Name]
[Same format...]

---

[Continue for all themes]

---

## Ranking Changes

**Moved up:**
- [Theme]: #[old] → #[new] (↑[change])

**Moved down:**
- [Theme]: #[old] → #[new] (↓[change])

**Stayed same:**
- [Theme]: #[position]

---

## Next Steps

Would you like to:
1. Save this new ranking to file (updates original or creates new)
2. Compare rankings side-by-side (original vs new)
3. Try different criteria
4. Export top 3 insights as summary
```

---

## Step 5: Save or Export (Optional)

**If user chooses to save:**
```markdown
Options:
1. ✅ Update original file ($1) with new ranking
2. 📄 Save as new file (analysis/$1-reranked-[criteria].md)
3. 📋 Just show me the ranking (don't save)

Which would you prefer?
```

---

## Error Handling

**If analysis file doesn't exist:**
```
❌ Analysis file not found: $1

Available analysis files in current directory:
- [file1]
- [file2]

Usage: /rank-insights [analysis-file] [--criteria]
```

**If insufficient data for chosen criteria:**
```
⚠️ Not enough data to rank by "[criteria]"

This ranking method requires:
- [What's needed]

Would you like to:
1. Choose different criteria
2. Provide required context
3. Cancel
```

---

## Usage Examples

```bash
# Rank by frequency (simplest)
/rank-insights analysis/customer-research-analysis.md --criteria frequency

# Rank by ICP relevance
/rank-insights analysis/interviews-analysis.md --criteria relevance

# Custom ranking
/rank-insights analysis/feedback-analysis.md --criteria "urgency based on churn risk"
```

---

## Tips for Effective Ranking

**Frequency ranking:**
- Good for: Identifying consensus themes
- Watch out for: Silent but critical minority opinions

**Impact ranking:**
- Good for: Prioritizing action items
- Consider: Both pain severity and opportunity size

**Relevance ranking:**
- Good for: Focusing on target audience
- Requires: Well-defined ICP

**Custom ranking:**
- Most flexible
- Best when you have specific strategic context
- Examples: "competitive urgency", "implementation cost", "customer segment"
