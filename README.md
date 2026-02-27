# Animalz Claude Code Plugins

Official Claude Code plugins for content marketing workflows.

---

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add animalzinc/claude-plugins
```

Then browse and install available plugins:

```bash
/plugin
```

---

## Available Plugins

### Blog Style Guide Creator

**AI-powered editorial style guide generation from blog content**

Generate comprehensive editorial style guides by analyzing published blog articles, then review content with 8 specialized AI agents running in parallel.

**Install:**
```bash
/plugin install blog-style-guide-creator
```

**Features:**
- 🤖 Automated style guide generation from blog articles
- 🔍 Multi-agent review system (8 specialized agents in parallel)
- 📊 Batch processing with portfolio compliance reporting
- ⚡ One-command workflows via custom slash commands

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz))

**Learn more:** [Plugin Documentation](./plugins/blog-style-guide-creator/README.md)

---

### Interactive Presentation Generator

**Transform data and findings into self-contained interactive HTML presentations**

Turn thick data reports, content audit results, or research findings into beautiful, interactive presentations that stakeholders can open directly in their browser.

**Install:**
```bash
/plugin install interactive-presentation-generator
```

**Features:**
- 📊 Interactive elements (tabs, accordions, charts)
- 🎨 Brand customization support
- 📱 Fully responsive and print-friendly
- 🚀 Self-contained HTML (no dependencies)

**Use cases:** Content audits, research synthesis, copy testing, stakeholder reports

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz))

**Learn more:** [Plugin Documentation](./plugins/interactive-presentation-generator/README.md)

---

### Interview Transcript Analyzer

**Analyze interview transcripts with unlimited token limits**

Extract themes, rank insights by relevance, and find representative quotes from interview transcripts. Intelligently scales from 1 to 8 parallel agents based on workload.

**Install:**
```bash
/plugin install interview-transcript-analyzer
```

**Features:**
- 🤖 Intelligent agent scaling (1-8 agents based on volume)
- 📊 Theme extraction across unlimited transcripts
- 🎯 Smart ranking (frequency, impact, ICP relevance, custom)
- 💬 Quote mining with quality scoring
- ⚡ 15-20 transcripts analyzed in 15-20 minutes

**Use cases:** Customer research, product feedback, user interviews, podcast research

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz))

**Learn more:** [Plugin Documentation](./plugins/interview-transcript-analyzer/README.md)

---

### Content Library Auditor

**Analyze WordPress XML, CMS JSON, or CSV exports for content insights**

Reveal publishing trends, author contributions, topic distribution, and content gaps with interactive HTML reports and charts.

**Install:**
```bash
/plugin install content-library-auditor
```

**Features:**
- 📊 Multi-format support (WordPress XML, JSON, CSV)
- 📈 Publishing trend analysis with seasonality detection
- ✍️ Author contribution breakdowns
- 🏷️ Topic analysis and content gap identification
- 📉 Interactive HTML reports with Chart.js

**Use cases:** Content audits, editorial planning, author performance, competitive analysis

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz))

**Learn more:** [Plugin Documentation](./plugins/content-library-auditor/README.md)

---

### Copywriting Coach

**Structured 7-phase copywriting process for short-form conversion copy**

Human writes, AI coaches. A `/copywrite` command that guides you through Brief, Strategy, Research, Exploration, Selection, Full Copy, and Review — with quality gates at every phase built on Harry Dry's Three Laws, Sullivan's advertising principles, and Wiebe's Money Words.

**Install:**
```bash
/plugin install copywriting-coach
```

**Features:**
- 📝 7-phase structured process with quality gates you can't skip
- 🎯 Two coach modes: Strict (human always proposes first) or Helpful (AI offers suggestions)
- 📊 Three-laws evaluation table for every variant
- 💰 Money Words audit (Joanna Wiebe's framework)
- ✍️ Supports landing pages, ads, emails, taglines, social posts, product descriptions

**Use cases:** Landing page copy, ad headlines, email campaigns, taglines, A/B test variant generation

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz))

**Learn more:** [Plugin Documentation](./plugins/copywriting-coach/README.md)

---

## About Animalz

[Animalz](https://animalz.co) is a content marketing agency specializing in high-quality editorial content for B2B SaaS companies. These plugins were developed internally to streamline our workflows and open-sourced to benefit the wider content marketing community.

---

## Plugin Development

### Creating a Plugin

Want to contribute your own content marketing plugin? See the [Claude Code Plugin Documentation](https://docs.claude.com/en/docs/claude-code/plugins) for details.

### Submitting to This Marketplace

1. Fork this repository
2. Add your plugin to the `plugins/` directory
3. Update `.claude-plugin/marketplace.json` with your plugin details
4. Submit a pull request

**Requirements:**
- Plugin must be related to content marketing workflows
- Must include comprehensive README and examples
- Must follow Claude Code plugin standards
- Must be tested and functional

---

## Credits

All plugins created by **Tim Metz** and published by **Animalz**:

1. **Blog Style Guide Creator** - Editorial style guide generation
2. **Interactive Presentation Generator** - Data to HTML presentations
3. **Interview Transcript Analyzer** - Research synthesis at scale
4. **Content Library Auditor** - CMS export analysis
5. **Copywriting Coach** - Structured copywriting process

**License:** MIT (all plugins)

Connect with Tim:
- 📝 [Substack: We Eat Robots](https://weeatrobots.substack.com/)
- 💼 [LinkedIn](https://www.linkedin.com/in/metztim/)
- 🐦 [X/Twitter @timmetz](https://x.com/timmetz)

---

## Support

- **Issues:** https://github.com/animalzinc/claude-plugins/issues
- **Email:** contact@animalz.co
- **Website:** https://animalz.co

---

## License

Individual plugins may have their own licenses. See each plugin's LICENSE file.

This marketplace repository is maintained by Animalz Inc.
