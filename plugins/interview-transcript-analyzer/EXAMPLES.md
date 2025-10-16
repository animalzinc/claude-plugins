# Interview Transcript Analyzer - Examples

Detailed walkthroughs for common use cases.

---

## Example 1: Customer Research Analysis (12 Interviews)

**Scenario:** Product team conducted 12 customer interviews to understand pain points.

### Setup

```
customer-research/
├── interviews/
│   ├── 2024-01-customer-1.txt
│   ├── 2024-01-customer-2.txt
│   └── ... (10 more)
└── context/
    ├── icp.md
    └── research-goals.md
```

### Command

```bash
/analyze-interviews product-feedback ./customer-research/interviews/ --context-file ./customer-research/context/icp.md
```

### Process

**1. Transcript Discovery**
```
📁 Transcripts Discovered
Directory: ./customer-research/interviews/
Transcripts found: 12 files
Total size: 2.4 MB
Estimated tokens: ~85k tokens

Context documents found:
- ICP document: icp.md
```
✅ User confirms

**2. Agent Strategy**
```
🤖 Agent Strategy
Based on 12 transcripts totaling ~85k tokens, I recommend using 5 parallel agents.

Agent assignments:
- Agent 1: Transcripts 1-3
- Agent 2: Transcripts 4-6
- Agent 3: Transcripts 7-9
- Agent 4: Transcripts 10-11
- Agent 5: Transcript 12

Estimated time: 12-15 minutes
```
✅ User approves

**3. Theme Extraction (in progress)**
```
🔍 Extracting Themes
- ✅ Agent 1: Complete (found 5 themes)
- ✅ Agent 2: Complete (found 4 themes)
- ✅ Agent 3: Complete (found 6 themes)
- ✅ Agent 4: Complete (found 4 themes)
- ✅ Agent 5: Complete (found 3 themes)
```

**4. Consolidated Themes**
```
🎯 Top Themes Identified

### Theme 1: Onboarding Complexity
Mentioned in: 10 of 12 transcripts (83%)
Relevance: High (core ICP pain point)
Key insight: Users struggle with initial setup, taking 2-3x longer than expected

Representative quote:
> "The onboarding took me three days when I thought it would be a few hours. I almost gave up."
> — Customer interview #7

### Theme 2: Pricing Transparency
Mentioned in: 9 of 12 transcripts (75%)
[etc...]
```
✅ User approves final report

**5. Output**
```
✅ Analysis Complete!
Report location: analysis/product-feedback-analysis.md
Transcripts analyzed: 12
Themes identified: 7 major themes, 15 total
Top insights: 5

Next steps:
1. Review the full report
2. Use /extract-quotes "onboarding" to find more examples
3. Use /rank-insights to re-rank by impact
```

**Time:** 14 minutes

---

## Example 2: Quote Extraction for Article

**Scenario:** Content marketer needs compelling quotes about "AI adoption challenges" for article.

### Command

```bash
/extract-quotes "AI adoption challenges" ./enterprise-interviews/ --max-quotes 10
```

### Output

```
💬 Quotes About: "AI adoption challenges"

Found 23 relevant quotes across 8 transcripts.
Showing top 10 by quality score.

---

### Quote 1 (Score: 9/10)
> "The technology isn't the hard part—it's getting people to trust it. Our team was skeptical for months until we showed them it actually saved time rather than creating more work."

Source: Participant #12 - enterprise-tech-lead.txt
Context: Discussing internal rollout of AI tools
Sub-theme: Change management and trust

---

### Quote 2 (Score: 8/10)
> "We had the budget and the tech chops, but we underestimated the training needed. You can't just throw AI at problems and expect magic."

Source: Participant #5 - saas-vp-product.txt
Context: Lessons learned from failed AI initiative
Sub-theme: Training and expectations

[8 more quotes...]

---

## Quote Breakdown

By sub-theme:
- Change management: 8 quotes
- Training needs: 6 quotes
- Technical integration: 5 quotes
- ROI justification: 4 quotes

By sentiment:
- Negative/Pain point: 15
- Mixed: 6
- Positive: 2
```

**Time:** 3 minutes

---

## Example 3: Re-Ranking by Business Value

**Scenario:** Initial analysis ranked by frequency, but team wants to prioritize by revenue potential.

### Command

```bash
/rank-insights analysis/customer-research-analysis.md --criteria "business value"
```

### Process

**1. Analysis Loaded**
```
📊 Analysis Loaded
File: analysis/customer-research-analysis.md
Themes found: 7
Current ranking: Frequency

How would you like to re-rank these insights?
```

**2. User selects "Business Value"**

**3. Context prompt**
```
To rank by business value, I need to understand:
1. Revenue impact indicators
2. Strategic priorities

Please provide business goals document, OR quick description of strategic priorities.
```

User provides: "Focus on reducing churn and enabling upsell to enterprise tier"

**4. Re-ranked Results**
```
✅ Insights Re-Ranked: Business Value

### #1: Enterprise Feature Gaps
Previous rank: #4
Score: 9/10
Why this ranks #1: Directly blocks upsell to enterprise tier (mentioned as blocker by 6 of 8 enterprise prospects)

### #2: Support Response Time
Previous rank: #6
Score: 8/10
Why this ranks #2: Primary churn driver (4 customers mentioned considering switching due to slow support)

### #3: Onboarding Complexity
Previous rank: #1 (by frequency)
Score: 7/10
Why this ranks #3: Delays time-to-value but doesn't directly impact churn or upsell

[etc...]

---

## Ranking Changes
Moved up:
- Enterprise Feature Gaps: #4 → #1 (↑3)
- Support Response Time: #6 → #2 (↑4)

Moved down:
- Onboarding Complexity: #1 → #3 (↓2)
```

**Time:** 5 minutes

---

## Example 4: Large-Scale Analysis (25 Transcripts)

**Scenario:** Annual customer feedback study with 25 hour-long interviews.

### Setup

```
annual-study/
└── transcripts/
    ├── jan-interviews/ (8 files)
    ├── feb-interviews/ (9 files)
    └── mar-interviews/ (8 files)
```

### Command

```bash
/analyze-interviews annual-study-2024 ./annual-study/transcripts/
```

### Process

**Agent Scaling Decision**
```
🤖 Agent Strategy
Based on 25 transcripts totaling ~220k tokens, I recommend using 8 parallel agents.

Agent assignments:
- Agents 1-7: 3 transcripts each
- Agent 8: 4 transcripts

Estimated time: 20-25 minutes
```

**Result:** All 25 transcripts analyzed in 22 minutes using 8 parallel agents

---

## Common Workflows

### Workflow 1: Full Analysis Pipeline

```bash
# 1. Initial analysis
/analyze-interviews q1-research ./interviews/ --context-file ./icp.md

# 2. Extract quotes for top theme
/extract-quotes "pricing concerns" ./interviews/

# 3. Re-rank by impact
/rank-insights analysis/q1-research-analysis.md --criteria impact

# 4. Get more quotes on #1 ranked theme
/extract-quotes "enterprise features" ./interviews/ --max-quotes 15
```

---

### Workflow 2: Competitive Research

```bash
# Analyze competitor user interviews
/analyze-interviews competitive-intel ./competitor-research/

# Extract quotes about specific competitor
/extract-quotes "switching from [Competitor X]" ./competitor-research/

# Rank by strategic value
/rank-insights analysis/competitive-intel-analysis.md --criteria "competitive urgency"
```

---

## Tips & Tricks

### Getting Better Theme Extraction

**✅ Do:**
- Include diverse interviews (different user types, use cases)
- Provide ICP document for relevance filtering
- Use consistent interview structure across sessions

**❌ Don't:**
- Mix customer types (B2B and B2C) in one analysis
- Include off-topic conversations
- Forget to de-identify sensitive information

### Quote Quality

**For presentations:** Use quotes scored 8-10

**For reports:** Quotes 6-10 work well

**For context:** Lower-scored quotes still useful for understanding

### Agent Scaling

**System decides automatically, but you can:**
- Request more agents for very large datasets (30+)
- Request fewer agents if system resources limited
- Split very large datasets into batches (analyze separately, then compare)

---

## Real-World Results

**Time Savings:**
- Manual analysis: 1-2 hours per transcript = 12-24 hours for 12 interviews
- With plugin: 15 minutes total
- **Speedup: 48-96x faster**

**Quality Improvements:**
- Catches patterns across all transcripts (humans might miss cross-cutting themes)
- Consistent scoring and ranking
- No recency bias (later interviews don't overshadow earlier ones)

---

## Questions?

- **Issues**: https://github.com/animalzinc/claude-plugins/issues
- **Email**: contact@animalz.co
- **More info**: See README.md for feature details
