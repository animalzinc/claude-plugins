# Blog Style Guide Creator

**AI-powered editorial style guide generation from blog content**

Created by [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) | Published by [Animalz](https://animalz.co)

**Connect:** [Substack](https://weeatrobots.substack.com/) | [LinkedIn](https://www.linkedin.com/in/metztim/) | [X/Twitter](https://x.com/timmetz)

---

## Overview

Generate comprehensive editorial style guides by analyzing published blog articles, then review content with 8 specialized AI agents running in parallel. Originally developed for Animalz but designed to work with any blog or publication.

### Key Features

- 🤖 **Automated Style Guide Generation**: Analyze 15+ blog articles to extract consistent editorial patterns
- 🔍 **Multi-Agent Review System**: 8 specialized agents review articles in parallel (4-5x faster than manual)
- 📊 **Batch Processing**: Review entire article portfolios with compliance reporting
- 🎯 **Blog-Focused**: Optimized for analyzing blog content, not broader brand materials
- ⚡ **One-Command Workflows**: Custom slash commands for all operations

---

## Quick Start

### Installation

```bash
/plugin marketplace add animalzinc/claude-plugins
/plugin install blog-style-guide-creator
```

### Generate a Style Guide

```bash
/generate-style-guide brand-name https://example.com/blog
```

### Review an Article

```bash
/style-check brand-name path/to/article.md
```

---

## What It Does

### Phase 1: Style Guide Generation

1. Collect 15-20 representative blog articles
2. Analyze patterns across 8 editorial dimensions
3. Generate comprehensive style guide with rules, examples, and checklist

**Style Guide Sections:**
1. Voice & Tone
2. Grammar & Usage
3. Punctuation
4. Formatting
5. Technical Standards
6. Content Patterns
7. Industry Terms
8. Quick Reference Checklist

### Phase 2: Article Review

1. Launch 8 specialized AI agents in parallel
2. Each agent reviews article against one section of style guide
3. Agents report violations with line numbers and corrections
4. Optionally apply corrections automatically

---

## Commands

### `/generate-style-guide [brand-name] [blog-url-or-directory]`

Generate editorial style guide by analyzing published blog articles.

**Examples:**
```bash
# From blog URL
/generate-style-guide hubspot https://blog.hubspot.com

# From local directory
/generate-style-guide contentful brands/contentful/source-articles/
```

**What it does:**
- Fetches/reads 15-20 representative articles
- Analyzes patterns across 8 editorial dimensions
- Generates comprehensive style guide with examples
- Saves to `brands/[brand-name]/style-guide.md`

**Time:** 1-2 hours (mostly AI analysis)

---

### `/style-check [brand-name] [article-path] [--auto-apply]`

Review blog article against editorial style guide using 8 specialized agents.

**Examples:**
```bash
# Review only
/style-check animalz brands/animalz/articles/original/my-article.md

# Review and auto-apply corrections
/style-check animalz brands/animalz/articles/original/my-article.md --auto-apply
```

**What it does:**
- Launches 8 agents in parallel (one per style guide section)
- Each agent identifies violations with line numbers
- Generates comprehensive review report
- Optionally applies corrections automatically

**Time:** 5-10 minutes (with parallel agents) vs. 40+ minutes (manual)

---

### `/batch-review [brand-name] [directory-path] [--auto-apply]`

Batch review multiple blog articles against editorial style guide.

**Examples:**
```bash
# Review all articles
/batch-review animalz brands/animalz/articles/original/

# Review and auto-apply corrections
/batch-review animalz brands/animalz/articles/original/ --auto-apply
```

**What it does:**
- Scans directory for markdown files
- Reviews each article sequentially
- Generates portfolio compliance report
- Shows most common violations across all articles

**Time:** ~10 minutes per 3 articles

---

## The 8 Review Agents

Each agent specializes in one editorial dimension:

| Agent | Focus | Common Violations |
|-------|-------|-------------------|
| **1. Voice & Tone** | Active voice, pronouns, contractions | Passive voice, pronoun inconsistency |
| **2. Grammar & Usage** | Oxford commas, Title Case, numbers | Missing commas, capitalization |
| **3. Punctuation** | Em dashes, quotation marks, lists | Em dash spacing, list punctuation |
| **4. Formatting** | Headings, lists, bold/italics, links | Heading hierarchy, hyperlink text |
| **5. Technical Standards** | Dates, times, percentages, currency | Date formats, percentage spacing |
| **6. Content Patterns** | Titles, openings, CTAs, bylines | Missing byline/CTA, weak opening |
| **7. Industry Terms** | Acronyms, product names, terminology | Undefined acronyms, wrong capitalization |
| **8. Quick Reference** | Comprehensive final check | Cross-category issues |

---

## Performance

| Operation | Time | Speedup |
|-----------|------|---------|
| **Style guide generation** | 1-2 hours | N/A (automated) |
| **Single article review** | 5-10 min | 4-5x vs manual (40+ min) |
| **Batch review (10 articles)** | ~30-50 min | Depends on parallel processing |

---

## Project Structure

```
brands/
└── [brand-name]/
    ├── style-guide.md           # Generated style guide
    ├── source-articles/          # Articles used to generate guide
    │   └── *.md
    └── articles/
        ├── original/             # Articles to review
        │   └── *.md
        └── edited/               # Auto-corrected articles
            └── *_edited.md
```

---

## Adding a New Brand

1. Create brand directory: `brands/your-brand/`
2. Add 15+ blog articles to `brands/your-brand/source-articles/`
3. Run: `/generate-style-guide your-brand brands/your-brand/source-articles/`
4. Review generated style guide at `brands/your-brand/style-guide.md`
5. Test on an article: `/style-check your-brand [article-path]`

---

## Use Cases

### For Content Teams
- **Onboard new writers** with brand-specific style guides
- **Maintain consistency** across large content portfolios
- **Scale content review** without hiring more editors
- **Identify common mistakes** across all content

### For Agencies
- **Generate client style guides** quickly from existing content
- **Deliver consistent quality** across all client work
- **Reduce editorial overhead** with automated reviews
- **Create value-add deliverable** (custom style guide)

### For Bloggers & Publishers
- **Document your editorial voice** automatically
- **Ensure consistency** as your publication grows
- **Train guest contributors** with clear guidelines
- **Batch-review backlogs** efficiently

---

## Requirements

- Claude Code (claude.ai/code)
- Blog articles in markdown format
- Access to blog URL (for fetching) or local article copies

---

## Example: Animalz

The `brands/animalz/` directory (in parent project) contains a complete example:
- Full 8-section style guide generated from 18 articles
- Sample articles (original and edited versions)
- Demonstrates all features of the system

---

## Contributing

To improve the plugin:

1. **Add new agents** in `agents/` for additional review dimensions
2. **Enhance commands** in `commands/` with new features
3. **Share feedback** at https://github.com/animalzinc/claude-plugins/issues
4. **Document improvements** in pull requests

---

## License

MIT License - Copyright (c) 2025 Tim Metz

See LICENSE file for details.

---

## About the Author

**Tim Metz** is a content marketing strategist and AI automation specialist. He built this plugin to streamline editorial workflows at Animalz and open-sourced it to help other content teams maintain editorial consistency at scale.

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
