# Claude Code Plugins Section (to add to article)

**Insert this section after "Use Case 3: Audit Your Content Library in Minutes" and before "Start Small, Think Big"**

---

## Supercharge These Workflows with Plugins

Since publishing this guide, we've turned each of these use cases into installable Claude Code plugins. Instead of starting from scratch each time, you can now install ready-to-use workflows with specialized agents and commands.

### What are Claude Code Plugins?

Plugins are packaged workflows that add custom slash commands and specialized agents to your Claude Code environment. Think of them as pre-built templates that you can install with a single command.

For example, instead of manually prompting Claude to analyze transcripts, you can install the Interview Transcript Analyzer plugin and use `/analyze-interviews` to run the entire workflow automatically.

### The Animalz Plugin Marketplace

We've open-sourced all three workflows (plus one bonus) as free plugins:

---

### 1. Interactive Presentation Generator

**For Use Case 1:** Turn data into interactive presentations

This plugin transforms the "interactive presentations" workflow into a one-command operation with user checkpoints for feedback.

**Install:**
```bash
/plugin marketplace add animalzinc/claude-plugins
/plugin install interactive-presentation-generator
```

**Use it:**
```bash
/create-presentation content-audit ./audit-materials/
```

The plugin guides you through:
- Proposing presentation structure (you approve)
- Building content sections
- Adding interactive elements (tabs, charts, accordions)
- Applying your brand styling
- Generating self-contained HTML

**What's included:** 4 specialized agents (structure planner, HTML generator, style applier, interactive element creator) that collaborate to build your presentation.

---

### 2. Interview Transcript Analyzer

**For Use Case 2:** Analyze interview transcripts at scale

This plugin handles interview analysis with intelligent parallel processing. It automatically scales from 1 to 8 agents based on your workload.

**Install:**
```bash
/plugin install interview-transcript-analyzer
```

**Use it:**
```bash
/analyze-interviews customer-research ./interviews/ --context-file ./icp.md
```

**Commands available:**
- `/analyze-interviews` - Full theme extraction and insight ranking
- `/extract-quotes [topic]` - Find compelling quotes on specific topics
- `/rank-insights` - Re-rank findings by different criteria

The plugin analyzes 15-20 transcripts in 15-20 minutes using parallel agents, with checkpoints for you to review themes and approve the analysis strategy.

**What's included:** 3 specialized agents (theme extractor, insight ranker, quote selector) plus intelligent workload distribution.

---

### 3. Content Library Auditor

**For Use Case 3:** Audit your content library

Turns the content audit workflow into automated analysis with interactive HTML reports.

**Install:**
```bash
/plugin install content-library-auditor
```

**Use it:**
```bash
/audit-content wordpress-export.xml --output-html
```

The plugin:
- Auto-detects format (WordPress XML, JSON, or CSV)
- Analyzes publishing trends, author contributions, and topic distribution
- Generates ASCII charts for terminal viewing
- Creates interactive HTML dashboard with Chart.js visualizations

**What's included:** 4 specialized agents (data parser, publishing analyzer, topic classifier, visualization generator) that turn raw exports into actionable insights.

---

### Bonus: Blog Style Guide Creator

We also created a fourth plugin for generating editorial style guides by analyzing your published content—perfect for maintaining consistency as your content library grows.

**Install:**
```bash
/plugin install blog-style-guide-creator
```

**Use it:**
```bash
/generate-style-guide your-brand https://yourblog.com
```

Analyzes 15+ articles to extract patterns and generates an 8-section style guide covering voice, grammar, punctuation, formatting, and more.

---

### Installing the Plugins

**One-time marketplace setup:**
```bash
/plugin marketplace add animalzinc/claude-plugins
```

**Then install any plugin:**
```bash
/plugin
# Browse available plugins and install with one command
```

All plugins are:
- **Free and open source** (MIT license)
- **Brand agnostic** (work with any company's content)
- **Well-documented** (comprehensive READMEs and examples)
- **Actively maintained** by the Animalz team

**View the source and contribute:**
[github.com/animalzinc/claude-plugins](https://github.com/animalzinc/claude-plugins)

---

### Why We Built These

After using Claude Code for months, we noticed we kept running the same workflows:
- Analyzing interview transcripts for podcast research
- Building presentations for stakeholder updates
- Auditing our content library quarterly

Rather than re-prompting Claude each time, we codified these workflows as plugins with specialized agents and user checkpoints. The result: workflows that are **10-50x faster** and **consistently higher quality**.

We're open-sourcing them because these aren't Animalz-specific workflows—they're common content marketing tasks that any team can benefit from.

**Try them out and let us know what you think:** contact@animalz.co

---

## Building Your Own Plugins

Want to turn your own Claude Code workflows into plugins? It's easier than you might think.

The process:
1. Identify a workflow you run repeatedly
2. Break it into logical steps with decision points
3. Create specialized agents for each step
4. Package as a plugin with commands and documentation

For a detailed walkthrough of how we built the Blog Style Guide Creator plugin, see [this LinkedIn post](https://www.linkedin.com/posts/metztim/...).

**Read the official docs:** [Claude Code Plugin Documentation](https://docs.claude.com/en/docs/claude-code/plugins)

---

[Continue with "Start Small, Think Big" section...]
