# Usage Examples

Real-world scenarios for using the Blog Style Guide Creator plugin.

---

## Table of Contents

1. [Generating Style Guides](#generating-style-guides)
2. [Reviewing Single Articles](#reviewing-single-articles)
3. [Batch Processing](#batch-processing)
4. [Common Workflows](#common-workflows)
5. [Sample Output](#sample-output)

---

## Generating Style Guides

### Example 1: Generate from Blog URL

**Scenario:** You want to create a style guide for HubSpot by analyzing their published blog content.

```bash
/generate-style-guide hubspot https://blog.hubspot.com
```

**What happens:**
1. Claude fetches 15-20 representative articles from the blog
2. Saves articles to `brands/hubspot/source-articles/`
3. Analyzes patterns across voice, grammar, punctuation, formatting, etc.
4. Generates comprehensive 8-section style guide
5. Saves to `brands/hubspot/style-guide.md`

**Time:** ~1-2 hours

**Output:**
- `brands/hubspot/style-guide.md` - Complete editorial guide
- `brands/hubspot/source-articles/` - 15-20 analyzed articles
- `brands/hubspot/source-articles/README.md` - Analysis metadata

---

### Example 2: Generate from Local Articles

**Scenario:** You already have 20 Contentful blog articles saved locally.

```bash
# First, organize your articles
mkdir -p brands/contentful/source-articles
# Copy your 20 markdown files there

# Then generate the style guide
/generate-style-guide contentful brands/contentful/source-articles/
```

**What happens:**
1. Claude reads all markdown files from the directory
2. Verifies you have enough articles (warns if < 15)
3. Analyzes editorial patterns
4. Generates style guide with specific examples from your content

**Best for:** When you have curated articles or want full control over the training set.

---

### Example 3: Update Existing Style Guide

**Scenario:** You generated a style guide 6 months ago and want to refresh it with newer articles.

```bash
# Add 5-10 new articles to your source directory
cp new-articles/*.md brands/animalz/source-articles/

# Regenerate the style guide
/generate-style-guide animalz brands/animalz/source-articles/
```

**What happens:**
1. Claude detects existing `brands/animalz/style-guide.md`
2. Reads current guide to preserve core rules
3. Analyzes ALL articles (old + new)
4. Updates patterns with new insights
5. Increments version number
6. Adds changelog note

**Best for:** Keeping style guides current as your editorial voice evolves.

---

## Reviewing Single Articles

### Example 4: Review Draft Article

**Scenario:** Writer just finished a draft blog post. You want to check it against your style guide before publication.

```bash
/style-check animalz brands/animalz/articles/original/new-draft.md
```

**What happens:**
1. Claude launches 8 specialized agents in parallel
2. Each agent reviews one dimension (voice, grammar, punctuation, etc.)
3. Agents report violations with exact line numbers
4. Generate comprehensive review report
5. Save report to `docs/logs/2025-10-15_style-check_animalz_new-draft.md`

**Time:** ~5-10 minutes

**Output:**
```markdown
## Summary by Section

- Voice & Tone: 2 violations
- Grammar & Usage: 5 violations
- Punctuation: 1 violation
- Formatting: 3 violations
- Technical Standards: 0 violations
- Content Patterns: 2 violations
- Industry Terms: 1 violation

**Total:** 14 violations (Medium priority)
```

---

### Example 5: Review and Auto-Apply Corrections

**Scenario:** You trust the style guide and want corrections applied automatically.

```bash
/style-check animalz brands/animalz/articles/original/my-article.md --auto-apply
```

**What happens:**
1. Same 8-agent review process
2. **Plus:** Claude applies all corrections automatically
3. Saves corrected version as `my-article_edited.md`
4. Generates before/after summary

**Best for:** High-confidence scenarios or when you need fast turnaround.

**⚠️ Caution:** Always spot-check the first few auto-corrected articles to ensure quality.

---

### Example 6: Review Article from Different Location

**Scenario:** Writer sent you a draft that's not in your standard directory.

```bash
/style-check contentful ~/Downloads/draft-article-from-writer.md
```

**What happens:**
- Claude reads the article wherever it lives
- Reviews against `brands/contentful/style-guide.md`
- Saves report to `docs/logs/`
- Does NOT move or modify the original file

**Best for:** Ad-hoc reviews of files from contributors.

---

## Batch Processing

### Example 7: Review Entire Content Backlog

**Scenario:** You have 25 blog articles that need style checking before republishing.

```bash
/batch-review animalz brands/animalz/articles/original/
```

**What happens:**
1. Claude scans directory and finds 25 markdown files
2. Asks for confirmation: "Found 25 articles. Proceed?"
3. Reviews each article sequentially
4. Generates individual report for each article
5. Creates portfolio compliance report

**Time:** ~10 minutes per 3 articles = ~80-90 minutes total

**Portfolio Report Includes:**
- Overall compliance stats (% fully compliant, minor issues, major issues)
- Most common violations across all articles
- Article-by-article summary table
- Priority recommendations

---

### Example 8: Batch Review with Auto-Apply

**Scenario:** You've validated the style guide and want to bulk-correct 15 articles.

```bash
/batch-review hubspot brands/hubspot/articles/original/ --auto-apply
```

**What happens:**
1. Reviews all 15 articles
2. **Plus:** Applies corrections to each one
3. Saves edited versions to `brands/hubspot/articles/edited/`
4. Generates portfolio report showing before/after stats

**Best for:** Large-scale content refreshes or when preparing backlogs for migration.

---

### Example 9: Identify Common Mistakes Across Portfolio

**Scenario:** You want to understand what writers consistently get wrong.

```bash
/batch-review animalz brands/animalz/articles/original/
```

**Look for this in the report:**

```markdown
## Most Common Violations

1. **Missing Oxford comma**: 42 occurrences across 18 articles
2. **Passive voice usage**: 28 occurrences across 12 articles
3. **Inconsistent heading capitalization**: 23 occurrences across 15 articles
4. **Missing byline format**: 10 occurrences across 10 articles
5. **Em dash spacing errors**: 19 occurrences across 8 articles
```

**Action:** Use these insights to update writer guidelines or provide targeted training.

---

## Common Workflows

### Workflow 1: Onboarding a New Client (Agency Use Case)

**Goal:** Create custom style guide and review first deliverable.

```bash
# Step 1: Generate style guide from client's blog
/generate-style-guide acme https://blog.acme.com

# Step 2: Review the generated guide
# (Manually review brands/acme/style-guide.md)

# Step 3: Write first article for client

# Step 4: Review article against style guide
/style-check acme brands/acme/articles/original/first-deliverable.md

# Step 5: Apply corrections
/style-check acme brands/acme/articles/original/first-deliverable.md --auto-apply

# Step 6: Send to client with style guide as value-add deliverable
```

---

### Workflow 2: Maintaining Consistency Across Large Team

**Goal:** Ensure 5 writers all follow the same editorial standards.

```bash
# Step 1: Generate or update company style guide
/generate-style-guide company brands/company/source-articles/

# Step 2: Share style guide with team
# (brands/company/style-guide.md)

# Step 3: Each writer reviews their drafts before submission
# Writer 1:
/style-check company drafts/writer1-article.md

# Writer 2:
/style-check company drafts/writer2-article.md

# Step 4: Editor does final batch review before publication
/batch-review company brands/company/articles/week-of-oct-15/
```

---

### Workflow 3: Content Audit & Refresh

**Goal:** Identify and fix style inconsistencies in 50 published articles.

```bash
# Step 1: Download all published articles from CMS
# (Save to brands/company/articles/published/)

# Step 2: Generate style guide from best-performing content
/generate-style-guide company brands/company/articles/top-performers/

# Step 3: Batch review entire published portfolio
/batch-review company brands/company/articles/published/

# Step 4: Review portfolio report to identify high-priority fixes
# (docs/logs/YYYY-MM-DD_batch-review_company.md)

# Step 5: Batch apply corrections to high-priority articles
/batch-review company brands/company/articles/published/high-priority/ --auto-apply

# Step 6: Manually review auto-corrected articles before republishing
```

---

## Sample Output

### Sample Style Check Report

```markdown
# Style Check Report: Animalz

**Article:** brands/animalz/articles/original/content-marketing-trends-2025.md
**Review Date:** October 15, 2025
**Total Violations:** 11

---

## Summary by Section

- Voice & Tone: 2 violations
- Grammar & Usage: 4 violations
- Punctuation: 2 violations
- Formatting: 1 violation
- Technical Standards: 0 violations
- Content Patterns: 1 violation
- Industry Terms: 1 violation

---

## Detailed Findings

### Agent 1 - Voice & Tone

**Violation 1:**
- **Line:** 45
- **Issue:** Passive voice used instead of active voice
- **Current:** "The survey was conducted by our team in March"
- **Correction:** "Our team conducted the survey in March"
- **Rule:** Section 1.2 - Active Voice (95%+ active voice required)

**Violation 2:**
- **Line:** 89
- **Issue:** Inconsistent pronoun usage
- **Current:** "You might think this is complex, but we've found it's straightforward"
- **Correction:** "This might seem complex, but it's straightforward"
- **Rule:** Section 1.3 - Pronoun Consistency (avoid mixing 'you' and 'we')

---

### Agent 2 - Grammar & Usage

**Violation 1:**
- **Line:** 23
- **Issue:** Missing Oxford comma
- **Current:** "We analyzed voice, tone and formatting"
- **Correction:** "We analyzed voice, tone, and formatting"
- **Rule:** Section 2.1 - Oxford Comma (ALWAYS use)

[... more violations ...]

---

## Priority Recommendations

**High Priority:**
- Fix passive voice in line 45 (affects brand voice)
- Add Oxford comma in line 23 (mandatory rule)

**Medium Priority:**
- Update heading capitalization (lines 12, 34, 67)
- Fix em dash spacing (line 78)

**Low Priority:**
- Consider rewording line 89 for consistency

---

## Next Steps

✅ Review complete with 11 violations found
📝 To apply corrections: /style-check animalz brands/animalz/articles/original/content-marketing-trends-2025.md --auto-apply
```

---

### Sample Batch Review Portfolio Report

```markdown
# Batch Review Report: Animalz

**Source Directory:** brands/animalz/articles/original/
**Review Date:** October 15, 2025
**Articles Reviewed:** 18

---

## Portfolio Compliance Summary

**Overall Statistics:**
- Fully compliant (0 violations): 3 articles (17%)
- Minor issues (1-5 violations): 8 articles (44%)
- Moderate issues (6-15 violations): 5 articles (28%)
- Major issues (16+ violations): 2 articles (11%)

**Total Violations Across Portfolio:**
- Voice & Tone: 24 violations
- Grammar & Usage: 67 violations
- Punctuation: 31 violations
- Formatting: 18 violations
- Technical Standards: 5 violations
- Content Patterns: 22 violations
- Industry Terms: 9 violations

**Average violations per article:** 9.8

---

## Most Common Violations

1. **Missing Oxford comma**: 24 occurrences across 15 articles (Grammar & Usage)
2. **Passive voice usage**: 18 occurrences across 11 articles (Voice & Tone)
3. **Incorrect em dash spacing**: 15 occurrences across 9 articles (Punctuation)
4. **Heading capitalization errors**: 14 occurrences across 12 articles (Grammar & Usage)
5. **Missing or incorrect byline**: 12 occurrences across 12 articles (Content Patterns)

---

## Article-by-Article Summary

| Article | Total | Status | Priority |
|---------|-------|--------|----------|
| article-001.md | 0 | ✅ | N/A |
| article-002.md | 3 | ⚠️ | Low |
| article-003.md | 8 | ⚠️ | Med |
| article-004.md | 21 | ❌ | High |
| article-005.md | 5 | ⚠️ | Low |
| article-006.md | 0 | ✅ | N/A |
[... etc ...]

---

## Priority Recommendations

### High Priority (Review First)
- article-004.md: 21 violations (major brand voice issues, missing structural elements)
- article-017.md: 18 violations (inconsistent grammar, formatting problems)

### Common Patterns to Address
- **Grammar:** Train writers on mandatory Oxford comma usage
- **Voice:** Remind team to use active voice 95%+ of the time
- **Content Patterns:** Update writer onboarding to include byline format requirements

---

## Next Steps

1. Fix high-priority articles first (articles 004, 017)
2. Consider style guide training session on Oxford commas
3. Update writer guidelines with passive voice examples
4. Set up pre-submission checklist for byline format
```

---

## Tips & Best Practices

### For Style Guide Generation
- **Use 15-20 articles** for best results
- **Choose diverse articles** spanning multiple years/topics
- **Include your best work** as training examples
- **Review the generated guide** before using it to review articles

### For Article Review
- **Start without --auto-apply** for first few reviews
- **Spot-check corrections** to build confidence
- **Use --auto-apply judiciously** once you trust the system
- **Keep original files** - never overwrite originals

### For Batch Processing
- **Start small** (5-10 articles) to test
- **Review portfolio report** before bulk corrections
- **Look for patterns** - what do writers consistently miss?
- **Update training** based on common mistakes

---

## Troubleshooting

**Q: Style guide seems too strict**
- Review the source articles used to generate it
- Regenerate with different/better articles
- Manually edit the style guide to adjust rules

**Q: Too many false positives in reviews**
- Refine the relevant section in the style guide
- Add exceptions for legitimate edge cases
- Update agent prompts if needed

**Q: Not enough articles to generate guide**
- Minimum 15 recommended
- Can proceed with 10-12 but quality may suffer
- Consider supplementing with competitor articles

---

For more information, see [README.md](README.md) or visit https://github.com/animalzinc/claude-plugins
