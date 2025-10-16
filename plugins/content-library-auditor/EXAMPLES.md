# Content Library Auditor - Examples

## Example 1: WordPress Blog Audit

**Scenario:** 3 years of blog content, need to analyze performance and find gaps.

### Export Process
1. WordPress → Tools → Export → All content
2. Download `export.xml` (8.2 MB, 247 posts)

### Command
```bash
/audit-content export.xml --output-html
```

### Results
```
✅ Content Audit Complete!

Analysis period: Jan 2021 - Dec 2023
Total content: 247 posts
Authors: 8
Categories: 12

Key Findings:
- Publishing declined 35% in 2023 (2.1 posts/month vs 3.2 in 2022)
- Top author (Alice) wrote 42% of all content
- "Product Updates" category has 89 posts, "Use Cases" only 12
- Q4 consistently slowest quarter (seasonal pattern)

Reports Generated:
- HTML: reports/export-audit.html
```

**Time:** 3 minutes

---

## Example 2: Multi-Year Trend Analysis

**Scenario:** Analyze 5 years of content to understand evolution.

### Insights from HTML Report

**Publishing Velocity:**
- 2019: 18 posts (startup phase)
- 2020: 45 posts (ramp up)
- 2021-2022: ~60 posts/year (plateau)
- 2023: 48 posts (decline)

**Author Evolution:**
- Early years: 2 authors (founders)
- 2021: Team grew to 6 authors
- 2023: 3 active authors (3 inactive)

**Topic Shifts:**
- 2019-2020: Product-focused (65%)
- 2021-2022: Use cases and education (55%)
- 2023: Thought leadership (40%)

**Recommendations:**
1. Hire to replace inactive authors
2. Return to 5 posts/month goal
3. Balance thought leadership with practical content

---

## Example 3: CSV Analytics Export

**Scenario:** Export from Google Analytics showing all published URLs with metadata.

### CSV Format
```csv
url,title,publish_date,author,pageviews,word_count
/blog/post-1,Title 1,2024-01-15,Alice,1250,1800
/blog/post-2,Title 2,2024-01-20,Bob,890,1200
```

### Command
```bash
/audit-content analytics-export.csv --format csv
```

### Additional Analysis
With pageview data:
- Identify top performers by traffic
- Correlate word count with engagement
- Find high-traffic topics for more content

---

## Common Workflow

```bash
# 1. Export from WordPress
# (Tools → Export → Download)

# 2. Run audit
/audit-content wordpress-export.xml --output-html

# 3. Open HTML report in browser
open reports/wordpress-export-audit.html

# 4. Review findings:
# - Check publishing consistency
# - Identify author imbalances
# - Find topic gaps

# 5. Plan next quarter based on insights
```

---

## Tips

**For accurate analysis:**
- Export all content (not just published)
- Include full date range
- Verify author attribution is consistent

**For better insights:**
- Run quarterly to track trends
- Compare year-over-year
- Cross-reference with traffic data

---

## Real-World Results

**Time Savings:**
- Manual spreadsheet analysis: 2-3 hours
- With plugin: 3-5 minutes
- **Speedup: 25-40x faster**

**Insights uncovered:**
- Seasonal patterns teams didn't notice
- Author burnout (declining output)
- Topic clusters that perform well
- Content gaps competitors are filling
