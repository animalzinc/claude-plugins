---
description: Comprehensive content library analysis from CMS export files
argument-hint: [export-file] [--format] [--output-html]
---

# Audit Content Library

Analyze WordPress XML, CMS JSON, or CSV exports to reveal publishing trends, author contributions, topic distribution, and content opportunities.

## Step 1: Detect and Parse Export File

**Read export file ($1):**
- Auto-detect format (XML/JSON/CSV) unless --format specified
- Validate file structure
- Count total items (posts, pages, etc.)

**Report to user:**
```markdown
## 📁 Content Export Detected

**File:** $1
**Format:** [WordPress XML / JSON / CSV]
**Items found:** [number] posts/pages
**Date range:** [earliest] to [latest]
**File size:** [size]

Would you like to proceed with analysis?
```

**Wait for user confirmation.**

---

## Step 2: Parse Content Data

Use **data-parser** agent to extract:

**For all formats:**
- Post titles
- Publication dates
- Authors
- Categories/tags
- Post length (word count)
- Status (published/draft)
- URLs/slugs

**Format-specific:**

**WordPress XML:**
```xml
<item>
    <title>Post Title</title>
    <pubDate>Date</pubDate>
    <dc:creator>Author</dc:creator>
    <category>Category</category>
    <content:encoded>Body content</content:encoded>
</item>
```

**JSON:**
```json
{
  "title": "Post Title",
  "date": "2024-01-15",
  "author": "Name",
  "categories": ["cat1", "cat2"],
  "content": "Body..."
}
```

**CSV:**
```csv
title,date,author,category,word_count
"Post Title","2024-01-15","Author","Category",1500
```

**Progress report:**
```
🔄 Parsing content...
- ✅ Posts extracted: [number]
- ✅ Authors identified: [number]
- ✅ Date range: [range]
- ✅ Categories: [number]
```

---

## Step 3: Analyze Publishing Trends

Use **publishing-analyzer** agent to calculate:

**Publishing Cadence:**
- Posts per month (last 6, 12, 24 months)
- Publishing frequency trends (increasing/decreasing)
- Seasonal patterns
- Content velocity

**Present to user:**
```markdown
## 📊 Publishing Trends

### Overall Stats
- Total posts: [number]
- Active period: [months/years]
- Average: [X] posts/month
- Trend: [Increasing 15% / Stable / Decreasing 10%]

### Recent Performance (Last 6 months)
- [Month]: [count] posts
- [Month]: [count] posts
[etc...]

### Publishing Patterns
- Peak month: [month] ([count] posts)
- Lowest month: [month] ([count] posts)
- Most active day: [day of week]

Would you like to continue with author and topic analysis?
```

**Wait for user approval.**

---

## Step 4: Author Contribution Breakdown

Use **publishing-analyzer** agent to:

**Calculate per author:**
- Total posts
- Percentage of total content
- Publishing frequency
- Average post length
- Active period (first to last post)

**Present breakdown:**
```markdown
## ✍️ Author Contributions

**Total authors:** [number]

### Top Contributors

#### 1. [Author Name]
- **Posts:** [number] ([percentage]% of total)
- **Avg length:** [words] words
- **Active:** [date range]
- **Cadence:** [X] posts/month

#### 2. [Author Name]
[Same format...]

---

### Long-tail Contributors
- [number] authors with 1-5 posts ([percentage]% of total)

Continue to topic analysis?
```

---

## Step 5: Topic & Category Analysis

Use **topic-classifier** agent to:

**Analyze categories/tags:**
- Distribution by category
- Most/least covered topics
- Topic combinations
- Content gaps

**Present analysis:**
```markdown
## 🏷️ Topic Distribution

### By Category
1. [Category 1]: [count] posts ([percentage]%)
2. [Category 2]: [count] posts ([percentage]%)
[etc...]

### Topic Insights
- **Most covered:** [topic] ([count] posts)
- **Underserved:** [topics with <5 posts]
- **Emerging:** [topics showing growth]

### Content Opportunities
- [Gap 1]: Only [X] posts, could expand
- [Gap 2]: [Related topics] covered, but [specific angle] missing

Proceed to generate report?
```

---

## Step 6: Generate Reports

**Ask user for output preference:**
```
📊 Report Format

Choose output format:
1. Terminal view (ASCII charts) - Quick review
2. Markdown file - For documentation
3. HTML report - Interactive charts (recommended)
4. All formats

Which would you like?
```

### Terminal View (ASCII Charts)

```
Publishing Trends (Last 12 Months)
═══════════════════════════════════
Jan 2024  ████████░░ 12 posts
Feb 2024  ██████░░░░  9 posts
Mar 2024  ███████████ 15 posts
[etc...]

Top Authors
═══════════════════════════════════
Alice Smith    ████████████████ 45 posts (35%)
Bob Johnson    ██████████░░░░░░ 28 posts (22%)
[etc...]
```

### Markdown Report

Save to `reports/[filename]-audit.md`:
```markdown
# Content Audit Report

**Analyzed:** [date]
**Source:** [filename]
**Period:** [date range]

## Executive Summary
[Key findings]

## Metrics
[Full breakdowns]
```

### HTML Report (with Charts)

Use **visualization-generator** agent to create:
- Line chart: Publishing trends
- Bar chart: Author contributions
- Pie chart: Topic distribution
- Interactive data tables

Save to `reports/[filename]-audit.html`

---

## Step 7: Deliver Results

**Report completion:**
```markdown
## ✅ Content Audit Complete!

**Analysis period:** [date range]
**Total content:** [number] posts
**Authors:** [number]
**Categories:** [number]

### Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

### Reports Generated
- Terminal summary: [displayed above]
- Markdown: reports/[name]-audit.md
- HTML: reports/[name]-audit.html (open in browser)

### Recommended Actions
1. [Action based on findings]
2. [Action based on findings]
3. [Action based on findings]

**Next steps:**
- Use `/publishing-trends` for deeper time-series analysis
- Use `/topic-analysis` to explore specific categories
```

---

## Usage Examples

```bash
# WordPress export
/audit-content wordpress-export.xml --output-html

# JSON export from headless CMS
/audit-content content-export.json

# CSV from analytics
/audit-content content-metrics.csv --format csv

# With specific output format
/audit-content export.xml --format wordpress --output markdown
```

---

## Supported Formats

| Format | Auto-detect | Notes |
|--------|-------------|-------|
| **WordPress XML** | ✅ | Standard WP export |
| **JSON** | ✅ | Any CMS JSON with title/date/author fields |
| **CSV** | ✅ | Must have title,date,author columns minimum |
| **Custom** | Specify with --format | Provide field mapping |

---

## Tips for Best Results

### Export Best Practices

**WordPress:**
1. Tools → Export → All content
2. Download XML file
3. Run audit

**Headless CMS:**
- Export with all metadata (author, dates, categories)
- Include content body for word count analysis
- JSON or CSV format preferred

**Analytics Export:**
- Include title, publish date, author, URL
- CSV works well for this

### Data Quality

✅ **Ensure export includes:**
- Publication dates (for trend analysis)
- Author names (for contribution breakdown)
- Categories/tags (for topic analysis)
- Content/word count (for depth analysis)

❌ **Watch out for:**
- Drafts mixed with published (can filter)
- Inconsistent date formats
- Missing author attribution
- Incomplete exports (verify date range)
