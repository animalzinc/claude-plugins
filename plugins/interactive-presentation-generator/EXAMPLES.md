# Interactive Presentation Generator - Examples

Detailed walkthroughs showing how to use this plugin for common scenarios.

---

## Example 1: Content Audit Presentation

**Scenario:** You've completed a content audit and need to present findings to stakeholders.

### Materials Setup

```
content-audit/
├── materials/
│   ├── audit-summary.md        # Executive summary
│   ├── publishing-trends.csv   # Historical publishing data
│   ├── topic-breakdown.json    # Content categorization
│   ├── top-performers.md       # Best performing articles
│   └── recommendations.md      # Strategic recommendations
└── brand/
    └── company-guidelines.md   # Brand colors and fonts
```

### Command

```bash
/create-presentation content-audit-2024 ./content-audit/materials/ --style-reference ./content-audit/brand/company-guidelines.md
```

### Process

1. **Material Validation**
   ```
   📊 Materials Found
   Directory: ./content-audit/materials/
   Files discovered: 5 files
   - Markdown: 4
   - CSV: 1
   - JSON: 1
   Style reference: ./content-audit/brand/company-guidelines.md
   ```
   ✅ You confirm

2. **Structure Proposal**
   ```
   📋 Proposed Structure
   Title: Content Audit 2024: Findings & Recommendations

   Sections:
   1. Executive Summary - Overview of audit scope and key findings
   2. Publishing Trends - Historical analysis with charts
   3. Topic Performance - Interactive breakdown by category
   4. Top Performers - Highlighting best content
   5. Recommendations - Strategic next steps

   Interactive Elements:
   - Line chart: Publishing frequency over 24 months
   - Pie chart: Content distribution by topic
   - Accordion: Detailed recommendations (12 items)
   - Tabs: Top 5 performers by different metrics

   Estimated length: 5 sections
   ```
   ✅ You approve

3. **Output**
   ```
   ✅ Presentation Complete!
   File: presentations/content-audit-2024.html
   Sections: 5
   Interactive elements: 4
   File size: 245 KB
   ```

---

## Example 2: Interview Research Synthesis

**Scenario:** Synthesize insights from 8 customer interviews into a presentation for product team.

### Materials Setup

```
customer-research/
├── materials/
│   ├── transcripts/
│   │   ├── interview-1.txt
│   │   ├── interview-2.txt
│   │   └── [... 6 more]
│   ├── research-objectives.md
│   └── customer-profile.md
```

### Command

```bash
/create-presentation customer-insights ./customer-research/materials/
```

### Process

1. **Material Validation**
   ```
   📊 Materials Found
   Directory: ./customer-research/materials/
   Files discovered: 10 files
   - Text: 8 (transcripts)
   - Markdown: 2 (objectives, profile)
   Style reference: None - will use default styling
   ```
   ✅ You confirm

2. **Structure Proposal**
   ```
   📋 Proposed Structure
   Title: Customer Interview Insights

   Sections:
   1. Research Overview - Objectives and methodology
   2. Key Themes - 5 major insights across all interviews
   3. Pain Points - Detailed breakdown with representative quotes
   4. Feature Requests - Organized by frequency and impact
   5. Recommendations - Product team next steps

   Interactive Elements:
   - Accordion: Theme details with supporting quotes
   - Tabs: Pain points by customer segment
   - Bar chart: Feature request frequency

   Estimated length: 5 sections
   ```

   💬 You suggest: "Let's add a 'Verbatim Quotes' section with the most compelling statements"

   ✅ Structure revised and approved

3. **Output**
   ```
   ✅ Presentation Complete!
   File: presentations/customer-insights.html
   Sections: 6
   Interactive elements: 3
   File size: 189 KB
   ```

---

## Example 3: A/B Test Results Presentation

**Scenario:** Present results from testing 3 email subject line variants.

### Materials Setup

```
ab-test/
├── materials/
│   ├── test-setup.md           # Hypothesis and methodology
│   ├── variant-a.md            # Subject line A details
│   ├── variant-b.md            # Subject line B details
│   ├── variant-c.md            # Subject line C details
│   ├── performance-data.csv    # Open rates, click rates, conversions
│   └── screenshots/
│       ├── variant-a.png
│       ├── variant-b.png
│       └── variant-c.png
```

### Command

```bash
/create-presentation email-test-results ./ab-test/materials/
```

### Process

1. **Structure Proposal**
   ```
   📋 Proposed Structure
   Title: Email Subject Line A/B Test Results

   Sections:
   1. Test Overview - Hypothesis, sample size, duration
   2. Variant Comparison - Side-by-side presentation
   3. Performance Analysis - Detailed metrics breakdown
   4. Winner & Insights - Results and learnings
   5. Next Steps - Recommendations for future tests

   Interactive Elements:
   - Tabs: Compare all 3 variants side-by-side with screenshots
   - Bar chart: Open rate, click rate, conversion rate comparison
   - Accordion: Detailed performance breakdown by segment

   Estimated length: 5 sections
   ```
   ✅ You approve

2. **Interactive Element Preview**
   ```
   🎨 Interactive Elements Added
   1. Section 2: Tabbed comparison of 3 email variants (with screenshots)
   2. Section 3: Bar chart showing performance metrics
   3. Section 3: Accordion with segment performance (6 items)

   Would you like to adjust any interactive elements?
   ```
   ✅ Looks good

3. **Output**
   ```
   ✅ Presentation Complete!
   File: presentations/email-test-results.html
   Sections: 5
   Interactive elements: 3
   File size: 312 KB (includes 3 screenshots)
   ```

---

## Example 4: Quarterly Performance Report

**Scenario:** Transform quarterly metrics into interactive dashboard for leadership team.

### Materials Setup

```
q4-report/
├── materials/
│   ├── traffic-data.csv        # Monthly traffic metrics
│   ├── conversion-data.csv     # Conversion funnel data
│   ├── content-metrics.csv     # Content performance
│   ├── highlights.md           # Major wins and initiatives
│   └── goals-vs-actuals.md     # Performance against targets
└── style/
    └── brand-colors.md         # Company colors for charts
```

### Command

```bash
/create-presentation q4-performance ./q4-report/materials/ --style-reference ./q4-report/style/brand-colors.md
```

### Process

1. **Structure Proposal**
   ```
   📋 Proposed Structure
   Title: Q4 2024 Performance Dashboard

   Sections:
   1. Executive Summary - High-level performance overview
   2. Traffic & Engagement - Visitor and engagement metrics
   3. Conversion Performance - Funnel analysis
   4. Content Performance - Top performers and trends
   5. Goals vs. Actuals - Performance against targets
   6. Key Wins - Major achievements this quarter

   Interactive Elements:
   - Line chart: Traffic trends over Q4
   - Bar chart: Month-over-month conversion rates
   - Pie chart: Traffic sources
   - Accordion: Top 10 content pieces with detailed metrics

   Estimated length: 6 sections
   ```
   ✅ You approve

2. **Output**
   ```
   ✅ Presentation Complete!
   File: presentations/q4-performance.html
   Sections: 6
   Interactive elements: 4
   File size: 198 KB
   ```

---

## Common Workflows

### Workflow 1: Quick Presentation (No Branding)

For internal updates or quick stakeholder summaries:

```bash
# 1. Organize materials in a folder
mkdir presentation-materials
mv report.md data.csv presentation-materials/

# 2. Generate presentation
/create-presentation quick-update ./presentation-materials/

# 3. Review, share via email or Slack
```

**Time:** 5-10 minutes

---

### Workflow 2: Branded Presentation

For client deliverables or executive presentations:

```bash
# 1. Organize materials
mkdir project-deliverable
mkdir project-deliverable/materials
mkdir project-deliverable/brand

# 2. Add content and brand guidelines
# [copy files]

# 3. Generate with branding
/create-presentation client-report ./project-deliverable/materials/ --style-reference ./project-deliverable/brand/guidelines.md

# 4. Review output, request adjustments if needed
# 5. Export to PDF using browser print (Cmd+P)
```

**Time:** 15-20 minutes

---

### Workflow 3: Research Synthesis

For synthesizing large amounts of qualitative data:

```bash
# 1. Organize transcripts and supporting docs
research-project/
├── materials/
│   ├── transcripts/ (10+ interview transcripts)
│   ├── methodology.md
│   └── research-goals.md

# 2. Generate presentation
/create-presentation research-synthesis ./research-project/materials/

# 3. Review proposed structure
# 4. Provide feedback: "Add a 'Methodology' section at the beginning"
# 5. Finalize and share
```

**Time:** 20-30 minutes (for large datasets)

---

## Tips & Best Practices

### For Best Results

1. **Name Files Clearly**
   - ✅ `customer-pain-points.md`
   - ❌ `notes_v3_final.md`

2. **Group Related Content**
   - Use subdirectories (transcripts/, data/, images/)
   - Keep materials focused on one topic

3. **Provide Context Documents**
   - Include research goals, ICP, or project brief
   - Helps the plugin understand intended narrative

4. **Use Consistent Data Formats**
   - CSV for tabular data
   - JSON for structured data
   - Markdown for narrative content

### Interactive Element Selection

**Choose Tabs when:**
- Comparing 2-5 distinct options
- Content is mutually exclusive (view one at a time makes sense)

**Choose Accordions when:**
- You have 6+ items in a list
- Details are optional (not everyone needs to see everything)
- Content is hierarchical

**Choose Charts when:**
- Showing trends over time
- Comparing quantities across categories
- Displaying proportions or distributions

---

## Troubleshooting

### Issue: "Insufficient materials" warning

**Problem:** Only 1-2 files in materials folder

**Solution:**
- Add more source materials (3+ recommended)
- Combine related content into materials folder
- Or proceed anyway for simple presentations

### Issue: Interactive elements not working

**Problem:** JavaScript disabled or browser compatibility

**Solution:**
- Check browser console for errors
- Ensure you're opening the HTML file directly (not viewing source)
- Try different browser (Chrome, Firefox, Safari all work)

### Issue: Charts not displaying

**Problem:** Network connection required for Chart.js CDN

**Solution:**
- Ensure internet connection when first opening presentation
- Charts will load from CDN (embedded in HTML)
- Once loaded, presentation works offline

---

## Real-World Results

**Time Savings:**
- Manual PowerPoint creation: 3-4 hours
- With this plugin: 15-20 minutes
- **Speedup: 10-15x faster**

**Quality Improvements:**
- Consistent professional styling
- Automatically accessible (keyboard nav, ARIA labels)
- Mobile responsive without extra work
- Interactive elements that would be complex in PowerPoint

---

## Questions?

- **Issues**: https://github.com/animalzinc/claude-plugins/issues
- **Email**: contact@animalz.co
- **More examples**: See README.md for additional use cases
