# Interview Transcript Analyzer

**Analyze interview transcripts with unlimited token limits - extract themes, rank insights, find quotes**

Created by [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) | Published by [Animalz](https://animalz.co)

**Connect:** [Substack](https://weeatrobots.substack.com/) | [LinkedIn](https://www.linkedin.com/in/metztim/) | [X/Twitter](https://x.com/timmetz)

---

## Overview

Analyze interview transcripts without hitting token limits. Extract themes across dozens of interviews, rank insights by relevance, and find the perfect quotes for your reports - all with intelligent parallel agent processing.

### Key Features

- 🤖 **Intelligent Agent Scaling** - Automatically uses 1-8 agents based on workload
- 📊 **Theme Extraction** - Identifies patterns across unlimited transcripts
- 🎯 **Smart Ranking** - Prioritize by frequency, impact, ICP relevance, or custom criteria
- 💬 **Quote Mining** - Find the most compelling quotes on any topic
- ✅ **User Collaboration** - Checkpoints at key decisions for your input
- ⚡ **Blazing Fast** - 15-20 transcripts analyzed in 15-20 minutes with parallel agents

---

## Quick Start

### Installation

```bash
/plugin marketplace add animalzinc/claude-plugins
/plugin install interview-transcript-analyzer
```

### Basic Usage

```bash
# Analyze all interviews in a folder
/analyze-interviews customer-research ./interviews/

# With ICP context for relevance ranking
/analyze-interviews product-study ./transcripts/ --context-file ./icp.md

# Find quotes on a specific topic
/extract-quotes pricing ./interviews/
```

---

## Commands

### `/analyze-interviews [name] [directory] [--context-file]`

Complete analysis of all interview transcripts - themes, insights, recommendations.

**What it does:**
1. Scans directory and counts transcripts
2. Intelligently scales agents (1-8) based on workload
3. Extracts themes with parallel agents
4. Consolidates and ranks insights
5. Generates comprehensive report

**User checkpoints:**
- Confirm transcripts before processing
- Approve agent scaling strategy
- Review themes before final report

**Example:**
```bash
/analyze-interviews q4-research ./customer-interviews/ --context-file ./icp.md
```

**Output:** `analysis/q4-research-analysis.md`

---

### `/extract-quotes [topic] [directory] [--max-quotes]`

Find the best quotes about a specific topic from your transcripts.

**What it does:**
1. Searches all transcripts for topic mentions
2. Rates quotes by quality (clarity, insight, conciseness)
3. Returns top quotes with attribution and context

**Example:**
```bash
/extract-quotes "onboarding challenges" ./interviews/ --max-quotes 15
```

---

### `/rank-insights [analysis-file] [--criteria]`

Re-rank insights from previous analysis with different criteria.

**Ranking options:**
- **Frequency** - Most mentioned first
- **Impact** - Highest severity/opportunity
- **Relevance** - Best fit with ICP
- **Business value** - Revenue/strategic potential
- **Ease** - Quick wins first
- **Custom** - Your own criteria

**Example:**
```bash
/rank-insights analysis/customer-research-analysis.md --criteria impact
```

---

## Intelligent Agent Scaling

The plugin automatically determines optimal agent count:

| Transcripts | Tokens | Agents | Time |
|-------------|--------|--------|------|
| 1-3 | Any | 1 | 5-10 min |
| 4-8 | <150k | 3 | 10-15 min |
| 4-8 | >150k | 5 | 10-15 min |
| 9-15 | Any | 5 | 15-20 min |
| 16+ | Any | 8 | 20-30 min |

**You're always asked to approve** the strategy before processing begins.

---

## Project Structure

### Recommended Setup

```
research-project/
├── interviews/              # Your transcript files
│   ├── interview-1.txt
│   ├── interview-2.txt
│   └── ...
├── context/                 # Optional context docs
│   ├── icp.md
│   ├── research-goals.md
│   └── methodology.md
├── analysis/                # Generated reports (created automatically)
│   └── project-analysis.md
└── quotes/                  # Extracted quotes (created automatically)
    └── topic-quotes.md
```

---

## Use Cases

### For Product Teams
- **Customer interviews** - Identify feature requests and pain points
- **User research** - Extract themes from usability studies
- **Feedback synthesis** - Analyze support tickets or feedback forms
- **Competitor research** - Synthesize competitive intelligence

### For Content Marketers
- **Podcast research** - Extract insights from episode transcripts
- **Expert interviews** - Find compelling quotes for articles
- **Audience research** - Understand customer needs and language
- **Case study research** - Pull quotes and themes from customer stories

### For Researchers
- **Qualitative analysis** - Code and analyze interview data
- **Focus group synthesis** - Extract themes from group discussions
- **Survey open-ends** - Analyze free-text survey responses
- **Academic research** - Thematic analysis at scale

---

## Analysis Output

Every analysis includes:

**Executive Summary** - Key findings at a glance

**Methodology** - What was analyzed and how

**Key Themes** - 5-7 major themes with:
- Frequency data
- Representative quotes
- Actionable recommendations
- Why it matters

**Cross-Cutting Insights** - Patterns spanning themes

**Recommendations** - Prioritized next steps

**Appendix** - Full theme list

---

## Tips for Best Results

### Organize Transcripts Well

✅ **Do:**
- Clear filenames (`2024-01-15-interview-acme-corp.txt`)
- Dedicated directory for each project
- Include participant metadata if helpful

❌ **Don't:**
- Mix unrelated interviews
- Use cryptic names (`transcript_final2.txt`)

### Provide Context

**ICP Document helps with:**
- Ranking insights by target customer relevance
- Focusing on themes that matter to your audience
- Filtering noise from edge cases

**Research Goals help with:**
- Ensuring findings align with objectives
- Highlighting unexpected discoveries
- Structuring recommendations appropriately

### Large Datasets

- Plugin scales automatically (you don't configure agents)
- 50+ transcripts? Works fine with 8 parallel agents
- Very long transcripts (100+ pages)? System handles it

---

## The Agents

This plugin uses 3 specialized agents:

| Agent | Role |
|-------|------|
| **theme-extractor** | Analyzes transcripts to find recurring patterns |
| **insight-ranker** | Prioritizes themes by various criteria |
| **quote-selector** | Finds high-quality quotes on specific topics |

---

## Requirements

- Claude Code
- Interview transcripts in common formats (.txt, .md, .doc, .docx)
- Optional: ICP or research goals document for better ranking

---

## Examples

See [EXAMPLES.md](./EXAMPLES.md) for detailed walkthroughs of:
- Customer research analysis (12 transcripts)
- Product feedback synthesis (25 transcripts)
- Competitive intelligence analysis
- Quote extraction workflows

---

## Contributing

To improve the plugin:

1. Share feedback at https://github.com/animalzinc/claude-plugins/issues
2. Suggest new ranking criteria
3. Report edge cases or bugs
4. Share example use cases

---

## License

MIT License - Copyright (c) 2025 Tim Metz

See LICENSE file for details.

---

## About the Author

**Tim Metz** is a content marketing strategist and AI automation specialist who built this plugin to analyze podcast interviews at scale.

**Connect with Tim:**
- 📝 [Substack: We Eat Robots](https://weeatrobots.substack.com/)
- 💼 [LinkedIn](https://www.linkedin.com/in/metztim/)
- 🐦 [X/Twitter @timmetz](https://x.com/timmetz)

**About Animalz:**
[Animalz](https://animalz.co) is a content marketing agency specializing in high-quality editorial content for B2B SaaS companies. This plugin was developed internally and open-sourced to benefit the wider content marketing community.

---

## Support

- **Issues**: https://github.com/animalzinc/claude-plugins/issues
- **Email**: contact@animalz.co
- **Documentation**: See EXAMPLES.md for detailed usage examples
