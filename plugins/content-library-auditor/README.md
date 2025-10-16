# Content Library Auditor

**Analyze WordPress XML, CMS JSON, or CSV exports for content insights**

Created by [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) | Published by [Animalz](https://animalz.co)

---

## Overview

Turn CMS exports into actionable insights. Analyze publishing trends, author contributions, topic distribution, and identify content opportunities - all with interactive HTML reports and charts.

### Key Features

- 📊 **Multi-Format Support** - WordPress XML, JSON, CSV
- 📈 **Publishing Trends** - Month-by-month analysis with trend detection
- ✍️ **Author Breakdown** - Contribution analysis and rankings
- 🏷️ **Topic Analysis** - Category distribution and content gaps
- 📉 **Interactive Reports** - HTML dashboards with Chart.js visualizations
- ⚡ **Fast Analysis** - Hundreds of posts analyzed in minutes

---

## Quick Start

```bash
/plugin marketplace add animalzinc/claude-plugins
/plugin install content-library-auditor

# Analyze WordPress export
/audit-content wordpress-export.xml --output-html
```

---

## What It Does

1. **Parses Export** - Auto-detects format (XML/JSON/CSV)
2. **Analyzes Trends** - Publishing cadence, seasonality, velocity
3. **Breaks Down Authors** - Who's writing what, how much, how often
4. **Classifies Topics** - Category distribution, gaps, opportunities
5. **Generates Reports** - Terminal, Markdown, or Interactive HTML

---

## Commands

### `/audit-content [file] [--format] [--output-html]`

Comprehensive content library analysis.

**Analyzes:**
- Publishing trends (last 6, 12, 24 months)
- Author contributions (posts, frequency, length)
- Topic distribution (categories, tags, gaps)
- Content opportunities (underserved topics)

**Outputs:**
- Terminal view with ASCII charts
- Markdown report
- Interactive HTML dashboard (recommended)

**Example:**
```bash
/audit-content content-export.xml --output-html
```

---

## Supported Formats

| Format | Use Case |
|--------|----------|
| **WordPress XML** | Standard WP export (Tools → Export) |
| **JSON** | Headless CMS exports (Contentful, Strapi, etc.) |
| **CSV** | Analytics exports, custom data |

**Auto-detection** works for all standard formats.

---

## Sample Outputs

### Terminal View
```
Publishing Trends (Last 12 Months)
═══════════════════════════════════
Jan 2024  ████████░░ 12 posts
Feb 2024  ██████░░░░  9 posts
Mar 2024  ███████████ 15 posts
```

### HTML Report Includes
- Line chart: Publishing over time
- Bar chart: Top authors
- Pie chart: Topic distribution
- Interactive tables: All posts, sortable

---

## Use Cases

**For Content Teams:**
- Audit content velocity and consistency
- Identify prolific vs inactive authors
- Find content gaps in topic coverage
- Benchmark against goals (posts/month)

**For Agencies:**
- Client content audit deliverables
- Identify opportunities for new content
- Author performance analysis
- Topic strategy recommendations

**For Marketers:**
- Analyze competitor content (if you have their data)
- Historical performance review
- Editorial calendar planning
- Resource allocation (author assignments)

---

## Tips for Best Results

### WordPress Export
1. WordPress Admin → Tools → Export
2. Select "All content"
3. Download XML file
4. Run `/audit-content export.xml --output-html`

### Headless CMS
- Export with metadata (author, dates, categories)
- Include content for word count analysis
- JSON or CSV format works best

### CSV Format
**Minimum columns:**
- title
- date (YYYY-MM-DD)
- author

**Optional columns:**
- category, tags, word_count, url, status

---

## Requirements

- Claude Code
- Content export file (XML/JSON/CSV)
- Web browser (for viewing HTML reports)

---

## Examples

See [EXAMPLES.md](./EXAMPLES.md) for walkthroughs of:
- WordPress content audit
- Headless CMS analysis
- Multi-year trend analysis

---

## The Agents

| Agent | Role |
|-------|------|
| **data-parser** | Parses XML/JSON/CSV into structured data |
| **publishing-analyzer** | Calculates trends and author stats |
| **topic-classifier** | Analyzes categories and identifies gaps |
| **visualization-generator** | Creates interactive HTML reports |

---

## License

MIT License - Copyright (c) 2025 Tim Metz

---

## Support

- **Issues**: https://github.com/animalzinc/claude-plugins/issues
- **Email**: contact@animalz.co
