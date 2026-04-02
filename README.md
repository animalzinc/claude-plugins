# Animalz Claude Code Plugins

Official Claude Code plugins and skills for content marketing workflows.

**For a full guide on how to use these plugins and get started with Claude Code, read [Claude Code for Content Marketers](https://www.animalz.co/blog/claude-code) on the Animalz blog.**

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

## Featured Plugins

### Structured Article Writer

**8-phase structured writing process for thought leadership articles**

Human fills the blank page — Claude enforces discipline. Foundation → Thesis → Structure → Research → Outline → Introduction → Drafting → Review, with quality gates at every phase. Includes `/write-rescue` (diagnose a broken draft) and `/write-status` (quick progress check).

**Install:**
```bash
/plugin install structured-article-writer
```

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz))

**Learn more:** [Plugin Documentation](./plugins/structured-article-writer/README.md)

---

### Copywriting Coach

**Structured 7-phase copywriting process for short-form conversion copy**

Human writes, AI coaches. A `/copywrite` command that guides you through Brief, Strategy, Research, Exploration, Selection, Full Copy, and Review — with quality gates at every phase built on Harry Dry's Three Laws, Sullivan's advertising principles, and Wiebe's Money Words.

**Install:**
```bash
/plugin install copywriting-coach
```

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz))

**Learn more:** [Plugin Documentation](./plugins/copywriting-coach/README.md)

---

### Blog Style Guide Creator

**AI-powered editorial style guide generation from blog content**

Generate comprehensive editorial style guides by analyzing published blog articles, then review content with 8 specialized AI agents running in parallel.

**Install:**
```bash
/plugin install blog-style-guide-creator
```

**Created by:** [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz))

**Learn more:** [Plugin Documentation](./plugins/blog-style-guide-creator/README.md)

---

## Skills

### Design Reference

**Iterative design research process**

Brief → references → feedback → principles → prototype → approval. Builds visual direction from stakeholder input before any prototyping begins.

**Install:**
```bash
/plugin install design-reference
```

---

### Session Saver

**Save structured session summaries for multi-day projects**

Captures objectives, files changed, decisions, and generates a continuation prompt so you can pick up where you left off.

**Install:**
```bash
/plugin install session-saver
```

---

### Image Prompt Creator

**Guided workflow for creating AI image generation prompts**

5-phase process for Nano Banana (Google's AI image generator): Brief → Concept → Prompt Craft → Generate & Iterate → Save. Supports brand presets with color palettes, style guidelines, and reference images.

**Install:**
```bash
/plugin install image-prompt-creator
```

---

## About Animalz

[Animalz](https://animalz.co) is a content marketing agency specializing in high-quality editorial content for B2B SaaS companies. These plugins were developed internally to streamline our workflows and open-sourced to benefit the wider content marketing community.

**Read our full guide:** [Claude Code for Content Marketers](https://www.animalz.co/blog/claude-code)

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

1. **Structured Article Writer** — 8-phase thought leadership writing process
2. **Copywriting Coach** — 7-phase short-form copy process
3. **Blog Style Guide Creator** — Style guide generation and compliance review
4. **Design Reference** — Iterative design research
5. **Session Saver** — Session continuity for multi-day projects
6. **Image Prompt Creator** — AI image prompt workflow

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
