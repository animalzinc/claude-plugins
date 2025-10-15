---
description: Generate editorial style guide by analyzing published blog articles
argument-hint: [brand-name] [blog-url-or-directory]
---

# Generate Style Guide for Brand

Generate a comprehensive house style guide for **$1** based on sample articles.

## Step 1: Collect Sample Articles

**If $2 is a URL (blog/website):**
- Use WebFetch to analyze the blog at $2
- Identify and fetch 15-20 representative articles spanning multiple years
- Look for variety in topics, formats, and publication dates
- Save articles to `brands/$1/source-articles/`

**If $2 is a directory path:**
- Read all markdown files from the directory $2
- Verify there are at least 15 articles (warn if fewer)
- Articles should already be in `brands/$1/source-articles/`

## Step 2: Validate Inputs

Before proceeding:
- Confirm at least 15 articles are available for analysis
- Create brand directory if it doesn't exist: `brands/$1/`
- Create subdirectories: `brands/$1/source-articles/`, `brands/$1/articles/original/`, `brands/$1/articles/edited/`

## Step 3: Launch Style Guide Generator Agent

Use the Task tool with the general-purpose subagent to analyze all collected articles.

**Provide the agent with:**
- The style guide generator prompt from `.claude/prompts/style-guide-generator.md`
- All collected article contents
- Brand name: $1
- Instruction to create comprehensive 8-section style guide

**The agent should analyze articles and create a style guide with:**

1. Voice & Tone
2. Grammar & Usage
3. Punctuation
4. Formatting
5. Technical Standards
6. Content Patterns
7. Industry-Specific Terms
8. Quick Reference Checklist

## Step 4: Save Style Guide

- Save the generated style guide to `brands/$1/style-guide.md`
- Include metadata: last updated date, number of articles analyzed, version 1.0
- Create a README in `brands/$1/source-articles/README.md` documenting:
  - Number of articles analyzed
  - Date range of articles
  - Topics covered
  - Any notable patterns or decisions

## Step 5: Validation & Summary

After generation:
- Verify the style guide has all 8 sections
- Verify it includes 50+ specific rules
- Verify it has clear examples (✅ DO / ❌ DON'T format)
- Verify Quick Reference Checklist is complete

**Report to user:**
```markdown
## Style Guide Generated Successfully

**Brand:** $1
**Source:** $2
**Articles Analyzed:** [number]
**Output Location:** brands/$1/style-guide.md

**Style Guide Contents:**
- ✅ Section 1: Voice & Tone
- ✅ Section 2: Grammar & Usage
- ✅ Section 3: Punctuation
- ✅ Section 4: Formatting
- ✅ Section 5: Technical Standards
- ✅ Section 6: Content Patterns
- ✅ Section 7: Industry-Specific Terms
- ✅ Section 8: Quick Reference Checklist

**Total Rules:** [number]
**Examples Provided:** [number]

**Next Steps:**
1. Review the generated style guide at brands/$1/style-guide.md
2. Test it on an article: `/style-check $1 [article-path]`
3. Refine the guide based on edge cases
```

## Special Instructions

**If updating existing style guide:**
- Check if `brands/$1/style-guide.md` already exists
- If yes, read the existing guide first
- Preserve core brand guidelines
- Add new patterns discovered from additional articles
- Increment version number
- Add changelog note at bottom

**Error Handling:**
- If fewer than 15 articles available, warn user and ask if they want to proceed anyway
- If blog URL is inaccessible, provide clear error message
- If brand directory creation fails, report the issue

## Usage Examples

```bash
# Generate style guide from blog URL
/generate-style-guide animalz https://www.animalz.co/blog

# Generate style guide from local directory
/generate-style-guide hubspot brands/hubspot/source-articles/

# Update existing style guide with new articles
/generate-style-guide animalz brands/animalz/source-articles/
```
