# Workflow Guide

Complete workflows for generating style guides, reviewing articles, and managing the brand style guide system.

## Table of Contents

1. [Generating a New Style Guide](#generating-a-new-style-guide)
2. [Reviewing a Single Article](#reviewing-a-single-article)
3. [Batch Processing Articles](#batch-processing-articles)
4. [Updating an Existing Style Guide](#updating-an-existing-style-guide)
5. [Understanding the Multi-Agent Review](#understanding-the-multi-agent-review)
6. [Troubleshooting](#troubleshooting)

---

## Generating a New Style Guide

### Overview

Create a comprehensive editorial style guide by analyzing 15-20 sample articles from a brand.

### Prerequisites

- 15-20 published blog articles (markdown format)
- Articles should span multiple years and topics
- Articles should be representative of target brand voice

### Workflow

#### Option A: Generate from Blog URL

```bash
/generate-style-guide [brand-name] [blog-url]
```

**Example:**
```bash
/generate-style-guide contentful https://www.contentful.com/blog/
```

**What happens:**
1. System fetches 15-20 articles from the blog URL
2. Converts to markdown if needed
3. Saves to `brands/[brand-name]/source-articles/`
4. Analyzes all articles for patterns
5. Generates 8-section style guide
6. Saves to `brands/[brand-name]/style-guide.md`

**Time:** 1-2 hours

#### Option B: Generate from Local Articles

1. **Collect articles manually:**
   ```bash
   mkdir -p brands/hubspot/source-articles
   # Copy 15-20 markdown files to this directory
   ```

2. **Run generator:**
   ```bash
   /generate-style-guide hubspot brands/hubspot/source-articles/
   ```

3. **Wait for analysis** (1-2 hours)

4. **Review output** at `brands/hubspot/style-guide.md`

### What Gets Generated

The style guide will include 8 sections:

1. **Voice & Tone** - Active voice preference, pronoun usage, contractions, formality
2. **Grammar & Usage** - Oxford comma, capitalization, hyphenation, numbers, acronyms
3. **Punctuation** - Em dashes, quotation marks, colons, list punctuation
4. **Formatting** - Headings, lists, bold/italics, hyperlinks, captions
5. **Technical Standards** - Dates, time, percentages, currency formatting
6. **Content Patterns** - Article titles, openings, CTAs, bylines
7. **Industry Terms** - Approved acronyms, product names, terminology standards
8. **Quick Reference** - Pre-publication checklist of critical rules

### Quality Checklist

After generation, verify:

- ✅ All 8 sections are present and comprehensive
- ✅ 50+ specific, actionable rules
- ✅ Clear examples for each major rule (✅ DO / ❌ DON'T)
- ✅ Quick Reference Checklist is complete
- ✅ Rules accurately reflect observed patterns
- ✅ Metadata includes: articles analyzed, date range, version number

### Next Steps

1. **Review the style guide** for accuracy
2. **Test on an article** not in the training set
3. **Refine if needed** based on edge cases
4. **Document source articles** in README

---

## Reviewing a Single Article

### Overview

Use 8 specialized AI agents to review an article against a brand's style guide in parallel.

### Prerequisites

- Style guide must exist for the brand
- Article in markdown format
- Article path (local file)

### Workflow

#### Step 1: Review Only (No Auto-Apply)

```bash
/style-check [brand-name] [article-path]
```

**Example:**
```bash
/style-check animalz brands/animalz/articles/original/my-article.md
```

**What happens:**
1. System launches 8 agents in parallel
2. Each agent reviews article against one section of style guide
3. Agents report violations with line numbers and corrections
4. System aggregates findings
5. Generates comprehensive report
6. Saves report to `docs/logs/`

**Time:** 5-10 minutes

**Output:**
- Console: Summary of violations by category
- File: Detailed report at `docs/logs/[date]_style-check_[brand]_[article].md`

#### Step 2: Review with Auto-Apply

```bash
/style-check [brand-name] [article-path] --auto-apply
```

**Example:**
```bash
/style-check animalz brands/animalz/articles/original/my-article.md --auto-apply
```

**What happens:**
1. Same as above, plus:
2. System applies all corrections automatically
3. Saves edited version with `_edited` suffix
4. Generates before/after summary

**Output:**
- Original: `brands/animalz/articles/original/my-article.md` (unchanged)
- Edited: `brands/animalz/articles/original/my-article_edited.md`
- Report: `docs/logs/[date]_style-check_animalz_my-article.md`

### Understanding the Report

The review report includes:

**Summary Section:**
```markdown
- Voice & Tone: 3 violations
- Grammar & Usage: 9 violations
- Punctuation: 3 violations
- Formatting: 5 violations
- Technical Standards: 0 violations
- Content Patterns: 4 violations
- Industry Terms: 2 violations
```

**Detailed Findings:**
Each violation includes:
- Line number
- Description of issue
- Current text (exact quote)
- Suggested correction
- Relevant style guide rule

**Priority Recommendations:**
- High Priority: Brand voice/structural issues
- Medium Priority: Consistency/formatting issues
- Low Priority: Minor polish

### The 8 Review Agents

Each agent specializes in one dimension:

| Agent | Focus Area | Common Violations |
|-------|-----------|-------------------|
| 1 | Voice & Tone | Passive voice, pronoun inconsistency, contraction errors |
| 2 | Grammar & Usage | Missing Oxford commas, Title Case errors, number formatting |
| 3 | Punctuation | Em dash spacing, list punctuation inconsistency |
| 4 | Formatting | Heading hierarchy, hyperlink anchor text, parallel structure |
| 5 | Technical Standards | Date formats, percentage spacing, currency |
| 6 | Content Patterns | Missing byline/CTA, weak opening, title length |
| 7 | Industry Terms | Undefined acronyms, product name capitalization |
| 8 | Quick Reference | Comprehensive final check across all sections |

### Best Practices

1. **Review report first** before applying corrections
2. **Spot-check a few corrections** to verify accuracy
3. **Apply manually for first article** to understand patterns
4. **Use --auto-apply** once confident in the system
5. **Keep original files** - never overwrite originals

---

## Batch Processing Articles

### Overview

Review multiple articles at once and generate portfolio compliance report.

### Prerequisites

- Style guide exists for brand
- Multiple articles in a directory
- Articles in markdown format

### Workflow

#### Step 1: Organize Articles

Place all articles to review in a directory:

```bash
brands/[brand-name]/articles/original/
├── article-1.md
├── article-2.md
├── article-3.md
└── ...
```

#### Step 2: Run Batch Review

```bash
/batch-review [brand-name] [directory-path]
```

**Example:**
```bash
/batch-review animalz brands/animalz/articles/original/
```

**What happens:**
1. System scans directory for markdown files
2. Excludes files already processed (`*_edited.md`)
3. Asks for confirmation
4. Reviews each article sequentially
5. Generates individual reports
6. Creates portfolio compliance report

**Time:** ~10 minutes per 3 articles

#### Step 3: Review Portfolio Report

The portfolio report includes:

**Overall Statistics:**
- Total articles reviewed
- Compliance distribution (fully compliant, minor issues, major issues)
- Total violations by category
- Average violations per article

**Most Common Violations:**
- Ranked list of most frequent issues
- How many articles each issue appears in

**Article-by-Article Summary:**
- Table with all articles
- Violation count per article
- Status (✅/⚠️/❌)
- Priority level

**Priority Recommendations:**
- High-priority articles to review first
- Common patterns to address
- Suggested style guide updates

#### Step 4: Apply Corrections

**Option A: Review and apply selectively**
```bash
# Review individual reports, then apply to specific articles
/style-check animalz brands/animalz/articles/original/article-1.md --auto-apply
```

**Option B: Batch auto-apply**
```bash
/batch-review animalz brands/animalz/articles/original/ --auto-apply
```

This will automatically correct all articles and save edited versions.

### Interpreting Results

**Fully Compliant (0 violations):**
- ✅ Article follows all style guide rules
- Can be used as exemplar for future content
- No action needed

**Minor Issues (1-5 violations):**
- ⚠️ Small formatting or consistency issues
- Low priority for correction
- Acceptable for publication with minor polish

**Moderate Issues (6-15 violations):**
- ⚠️ Multiple rule violations across categories
- Should be reviewed before publication
- May indicate writer needs style guide training

**Major Issues (16+ violations):**
- ❌ Significant style guide non-compliance
- High priority for correction
- May indicate style guide misalignment or inadequate training

### Best Practices

1. **Start with small batch** (5-10 articles) to test
2. **Review portfolio report** before bulk corrections
3. **Identify patterns** - are certain violations common across all articles?
4. **Consider style guide updates** if many articles violate same "rule"
5. **Use as training tool** - share common violations with writers
6. **Track improvement** - re-run periodically to measure compliance trends

---

## Updating an Existing Style Guide

### Overview

Refresh a brand's style guide based on new articles or evolved brand voice.

### When to Update

- Brand voice has evolved
- New content formats emerged
- Existing guide has gaps or conflicts
- Quarterly/annual review cycle

### Workflow

#### Step 1: Add New Sample Articles

Add recent articles to the source-articles directory:

```bash
brands/[brand-name]/source-articles/
├── (existing articles)
├── 2025-08-new-article-1.md
├── 2025-09-new-article-2.md
└── 2025-09-new-article-3.md
```

Aim for 5-10 new articles for meaningful updates.

#### Step 2: Regenerate Style Guide

```bash
/generate-style-guide [brand-name] brands/[brand-name]/source-articles/
```

**What happens:**
1. System detects existing style guide
2. Reads current rules
3. Analyzes all articles (old + new)
4. Preserves core brand guidelines
5. Adds new patterns discovered
6. Flags any conflicts for review
7. Increments version number

#### Step 3: Review Changes

Use git to see what changed:

```bash
git diff brands/[brand-name]/style-guide.md
```

Look for:
- **New rules added** - Do they make sense?
- **Rules modified** - Are changes intentional?
- **Conflicts flagged** - Need manual resolution?

#### Step 4: Document Changes

Update metadata in style guide:

```markdown
**Last Updated:** October 2025
**Version:** 2.0
**Based on analysis of:** 25 blog articles from 2021-2025

## Changelog

### Version 2.0 (October 2025)
- Added section on AI terminology (7.4)
- Updated CTA guidelines for softer approach (6.3)
- Refined active voice examples (1.2)
- Analyzed 7 new articles from 2025
```

#### Step 5: Re-test

Test updated guide on a recent article:

```bash
/style-check [brand-name] [recent-article-path]
```

Verify violations make sense given updated rules.

### Best Practices

1. **Version control** - Commit before regenerating
2. **Review diffs carefully** - Not all changes are improvements
3. **Manual override** - Edit style guide manually if needed
4. **Document rationale** - Explain major changes in changelog
5. **Communicate** - Share updates with content team
6. **Update gradually** - Don't change too much at once

---

## Understanding the Multi-Agent Review

### Why 8 Agents?

**Specialization improves accuracy:**
- Each agent is expert in one domain
- Deep focus vs. shallow broad coverage
- Reduces false positives

**Parallel execution is faster:**
- 8 agents run simultaneously
- 4-5x faster than sequential review
- Same quality, less time

**Easier to debug and refine:**
- Isolate which section has issues
- Update one agent without affecting others
- Clear separation of concerns

### How Agents Work Together

```
                    Article + Style Guide
                            |
                ┌───────────┴───────────┐
                |   Orchestrator        |
                └───────────┬───────────┘
                            |
        ┌──────┬────┬────┬─┴─┬────┬────┬────┬──────┐
        |      |    |    |   |    |    |    |      |
        ▼      ▼    ▼    ▼   ▼    ▼    ▼    ▼      ▼
    Agent1 Agent2 A3  A4  A5  A6  A7  A8
    Voice  Grammar Punc Form Tech Cont Ind  Quick
                            |
                ┌──────┬────┴────┬────┬────┐
                ▼      ▼         ▼    ▼    ▼
           Findings from each agent
                            |
                    ┌───────┴────────┐
                    | Aggregator     |
                    └───────┬────────┘
                            |
                    ▼
            Deduplicated Report
```

### Agent Prompts

Each agent has a dedicated prompt in `.claude/prompts/`:

- `voice-tone-agent.md`
- `grammar-usage-agent.md`
- `punctuation-agent.md`
- `formatting-agent.md`
- `technical-standards-agent.md`
- `content-patterns-agent.md`
- `industry-terms-agent.md`
- `quick-reference-agent.md`

**Customizing agents:**
1. Edit the relevant prompt file
2. Add new rules to check
3. Refine output format
4. Test on sample article
5. Iterate based on results

### Handling Overlaps

Some rules may be checked by multiple agents (e.g., Title Case by both Grammar and Formatting agents).

**This is intentional:**
- Reduces chance of missing violations
- Different perspectives can catch different patterns
- Aggregator deduplicates findings

---

## Troubleshooting

### "Style guide not found"

**Problem:** Running `/style-check` but no style guide exists.

**Solution:**
```bash
/generate-style-guide [brand-name] [source]
```

### "Not enough articles for analysis"

**Problem:** Fewer than 15 articles in source directory.

**Solutions:**
- Add more articles
- Run anyway (may produce less accurate guide)
- Use blog URL to fetch more articles automatically

### "Too many violations found"

**Problem:** Review finds 50+ violations in a well-written article.

**Possible causes:**
- Style guide is too strict
- Style guide doesn't match article's intended voice
- Training articles were inconsistent

**Solutions:**
1. Review a few violations manually - are they valid?
2. If many false positives: Refine style guide
3. If article truly doesn't match: May need different brand or style guide update

### "Agents missing obvious issues"

**Problem:** Review didn't catch a clear violation.

**Solutions:**
1. Check which agent should catch it
2. Review that agent's prompt in `.claude/prompts/`
3. Add explicit rule to agent prompt
4. Re-run review to verify fix

### "Conflicting rules in style guide"

**Problem:** Style guide contradicts itself.

**Solutions:**
1. Review source articles - were patterns actually consistent?
2. Manually edit style guide to resolve conflict
3. Add note about edge cases
4. Document decision in style guide

### "Auto-apply made incorrect changes"

**Problem:** Automatic corrections introduced errors.

**Solutions:**
1. Revert to original (always keep originals!)
2. Review specific violations that were wrong
3. Update relevant agent prompt to improve accuracy
4. Apply corrections manually for this article
5. File issue in `docs/decisions/` about the pattern

---

## Advanced Workflows

### Creating Custom Agents

Add a new review dimension:

1. **Create agent prompt** in `.claude/prompts/new-agent.md`
2. **Follow template** from existing agents
3. **Update slash command** to include new agent
4. **Test on sample article**
5. **Refine based on results**

### Comparing Style Guides

See how brands differ:

```bash
diff brands/animalz/style-guide.md brands/hubspot/style-guide.md
```

Useful for:
- Understanding industry standards
- Informing new brand guidelines
- Identifying unique brand differentiators

### Automating with CI/CD

Integrate into publishing workflow:

```bash
# In CI pipeline
/style-check $BRAND_NAME $ARTICLE_PATH

# If violations found, fail build or create PR comment
```

---

## Questions?

- **Project structure**: See [README.md](../README.md)
- **Adding brands**: See [brands/README.md](../brands/README.md)
- **Session logs**: See [docs/logs/](logs/)
- **Technical decisions**: See [docs/decisions/](decisions/)
