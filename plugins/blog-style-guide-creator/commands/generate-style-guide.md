---
description: Generate editorial style guide by analyzing published blog articles
argument-hint: [brand-name] [blog-url-or-directory]
---

# Generate Style Guide for Brand

Generate a comprehensive house style guide for **$1** based on sample articles.

## Step 1: Collect Sample Articles

Users can combine any of these input methods:

**Directory of local files**
- If a directory path is provided, read all markdown/text files (*.md, *.txt)
- Gives full control over which articles to analyze

**URLs pasted directly**
- If URLs are provided, use WebFetch to retrieve each article
- URLs can be space-separated or on separate lines
- **CRITICAL:** Use this exact WebFetch prompt: "Extract the COMPLETE article content verbatim as markdown. Include the full title, all body paragraphs, all headings and subheadings, all lists, all quotes, and any author/date metadata. Preserve all formatting: bold, italics, hyperlinks (as markdown links), code blocks, and block quotes. Do NOT summarize or paraphrase. Return the entire article exactly as written."
- Save fetched articles to `brands/$1/source-articles/`

**Blog URL with guidance**
- If a blog URL is provided, attempt to discover and fetch articles
- User can include guidance like "only articles from 2024 or later" or "focus on technical content"
- Follow user's guidance when selecting which articles to fetch
- **CRITICAL:** When fetching each discovered article, use this exact WebFetch prompt: "Extract the COMPLETE article content verbatim as markdown. Include the full title, all body paragraphs, all headings and subheadings, all lists, all quotes, and any author/date metadata. Preserve all formatting: bold, italics, hyperlinks (as markdown links), code blocks, and block quotes. Do NOT summarize or paraphrase. Return the entire article exactly as written."

**Combining inputs**
- All methods can be combined in a single command
- Example: local directory + a few extra URLs + guidance for additional discovery

## Step 2: Validate Inputs

Before proceeding:
- Confirm at least 5 articles are available for analysis
  - If 5-9 articles: Proceed, but note "10-15 articles recommended for best results"
  - If <5 articles: Warn that results may be unreliable, ask user to confirm
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
- If fewer than 5 articles: Warn and ask user to confirm before proceeding
- If 5-9 articles: Note recommendation for 10-15, but proceed
- If any URL is inaccessible, report which URLs failed and continue with others
- If brand directory creation fails, report the issue

## Usage Examples

```bash
# From local directory
/generate-style-guide animalz brands/animalz/source-articles/

# From pasted URLs
/generate-style-guide animalz https://example.com/blog/post-1 https://example.com/blog/post-2 https://example.com/blog/post-3

# Blog URL with guidance
/generate-style-guide acme https://acme.com/blog - only use articles from 2024 or later, focus on thought leadership pieces

# Combined: directory + extra URLs
/generate-style-guide animalz brands/animalz/source-articles/ https://example.com/blog/new-post-1 https://example.com/blog/new-post-2

# Combined: URLs + blog with guidance
/generate-style-guide hubspot https://blog.hubspot.com/post-1 https://blog.hubspot.com/post-2 - also grab 5 more recent marketing articles from the blog
```
