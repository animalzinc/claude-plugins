# Interactive Presentation Generator

**Transform data, reports, and findings into self-contained interactive HTML presentations**

Created by [Tim Metz](https://www.linkedin.com/in/metztim/) ([@timmetz](https://x.com/timmetz)) | Published by [Animalz](https://animalz.co)

**Connect:** [Substack](https://weeatrobots.substack.com/) | [LinkedIn](https://www.linkedin.com/in/metztim/) | [X/Twitter](https://x.com/timmetz)

---

## Overview

Turn thick data reports, content audit results, research findings, or copy variations into beautiful, interactive, self-contained HTML presentations that stakeholders can open directly in their browser.

### Key Features

- 📊 **Interactive Elements** - Tabs, accordions, charts for engaging data presentation
- 🎨 **Brand Customization** - Apply your brand guidelines automatically
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- 🖨️ **Print-Friendly** - Built-in print styles for PDF export
- 🚀 **Self-Contained** - Single HTML file, no external dependencies
- ✨ **Professional Output** - Polished, stakeholder-ready presentations

---

## Quick Start

### Installation

```bash
/plugin marketplace add animalzinc/claude-plugins
/plugin install interactive-presentation-generator
```

### Basic Usage

```bash
# Create presentation from materials folder
/create-presentation content-audit ./audit-materials/

# With brand styling
/create-presentation q4-report ./reports/q4/ --style-reference ./brand/style-guide.md
```

---

## What It Does

### Step-by-Step Workflow

1. **Validates Materials** - Scans your materials folder and confirms what's available
2. **Proposes Structure** - Analyzes content and suggests presentation sections (you approve)
3. **Builds Content** - Transforms raw materials into polished, narrative sections
4. **Applies Styling** - Adds professional CSS (branded or default)
5. **Adds Interactivity** - Implements tabs, charts, accordions as appropriate
6. **Delivers HTML** - Outputs single, self-contained HTML file

### User Collaboration Checkpoints

You're involved at key decision points:
- ✅ Approve materials before processing
- ✅ Review and adjust proposed structure
- ✅ Provide feedback on interactive elements before finalizing

---

## Commands

### `/create-presentation [name] [materials-dir] [--style-reference]`

Generate interactive HTML presentation from materials.

**Arguments:**
- `name` - Presentation name (used for output filename)
- `materials-dir` - Path to folder containing source materials
- `--style-reference` - (Optional) Path to brand guidelines or style reference

**Example:**
```bash
/create-presentation stakeholder-report ./project/materials/ --style-reference ./brand/guidelines.md
```

---

## Interactive Elements

The plugin intelligently selects interactive components based on your content:

| Element | Use Case | Example |
|---------|----------|---------|
| **Tabs** | Compare 2-5 options | A/B test results, content variants |
| **Accordions** | Lists of 6+ items | Detailed findings, FAQs |
| **Charts** | Trends and data viz | Publishing trends, performance metrics |
| **Side-by-Side** | Direct comparisons | Before/after, competitive analysis |
| **Filters** | Large datasets | 20+ items that need categorization |

---

## Project Structure

### Recommended Setup

```
project/
├── materials/              # Your source content
│   ├── report.md
│   ├── data.csv
│   ├── findings.txt
│   └── screenshots/
├── brand/                  # Optional brand guidelines
│   └── style-guide.md
└── presentations/          # Generated HTML files (created automatically)
    └── my-presentation.html
```

---

## Use Cases

### For Content Marketers

- **Content Audits** - Turn audit findings into interactive stakeholder presentations
- **Research Synthesis** - Transform interview data into compelling insights decks
- **Copy Testing** - Present multiple copy variants side-by-side for review
- **Performance Reports** - Create interactive dashboards from analytics exports

### For Teams

- **Project Summaries** - Compile project materials into single shareable presentation
- **Stakeholder Updates** - Transform scattered updates into cohesive story
- **Knowledge Sharing** - Make internal research accessible and engaging
- **Client Deliverables** - Package findings into professional presentations

---

## Output Features

Every generated presentation includes:

- **Sticky Navigation** - Easy section jumping
- **Smooth Scrolling** - Professional transitions
- **Print Button** - One-click PDF export
- **Responsive Design** - Works on all devices
- **Accessibility** - Keyboard navigation, ARIA labels, screen reader support
- **Fast Loading** - Optimized assets, single file

---

## Tips for Best Results

### Materials Organization

✅ **Do:**
- Use clear, descriptive file names
- Group related materials in subdirectories
- Include images/charts if available
- Provide context documents (strategy, ICP)

❌ **Don't:**
- Mix unrelated projects in one folder
- Use cryptic file names (data1.txt, report_final_v3.md)
- Include drafts or outdated materials

### Style References

Good style references include:
- Brand guidelines (colors, fonts, visual style)
- Previous presentations (for consistency)
- Design systems or pattern libraries

The plugin extracts:
- Color palettes (primary, secondary, accent)
- Typography (font families, weights, sizes)
- Visual preferences (border radius, shadows, spacing)

---

## Requirements

- Claude Code
- Materials in common formats (markdown, txt, CSV, JSON, images)
- Optional: Brand guidelines for customized styling

---

## Examples

See [EXAMPLES.md](./EXAMPLES.md) for detailed walkthroughs of:
- Content audit presentation
- Research synthesis
- A/B test results presentation
- Quarterly performance report

---

## The Agents

This plugin uses 4 specialized agents:

| Agent | Role |
|-------|------|
| **structure-planner** | Analyzes materials and proposes presentation structure |
| **html-generator** | Builds semantic HTML from content |
| **style-applier** | Creates professional CSS styling |
| **interactive-element-creator** | Implements tabs, charts, accordions |

---

## Contributing

To improve the plugin:

1. Share feedback at https://github.com/animalzinc/claude-plugins/issues
2. Suggest new interactive elements
3. Report bugs or edge cases
4. Share example use cases

---

## License

MIT License - Copyright (c) 2025 Tim Metz

See LICENSE file for details.

---

## About the Author

**Tim Metz** is a content marketing strategist and AI automation specialist who built this plugin to streamline presentation creation for content marketing teams.

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
