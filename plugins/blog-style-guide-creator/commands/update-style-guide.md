---
description: Update existing style guide with patterns from new articles
argument-hint: [brand-name] [new-articles-path]
---

# Update Style Guide

Incrementally update the **$1** style guide with patterns from new articles at **$2**.

## Step 1: Validate Existing Style Guide

Before proceeding:
- Verify style guide exists at `brands/$1/style-guide.md`
  - If missing: Error and suggest running `/generate-style-guide $1 [source]`
- Read and parse existing style guide
- Extract current rules, preferences, and exceptions from all 8 sections
- Note current version number (e.g., "1.0", "1.1")

## Step 2: Collect New Articles

- Read all markdown files from $2
- Verify at least 3 new articles provided
  - If fewer than 3: Warn that updates may be less reliable
- Check articles aren't already in `brands/$1/source-articles/` (avoid duplicates)
- If duplicates found: Warn user and exclude duplicates from analysis

## Step 3: Analyze New Patterns

Launch style guide generator agent (Opus model) with:
- Existing style guide content
- New article contents
- Special instruction: "Compare new articles against existing rules. Identify:
  1. NEW patterns not covered by existing rules
  2. Patterns that CONTRADICT existing rules
  3. Patterns that CONFIRM existing rules (strengthen confidence)"

The agent should categorize findings:
- **New Rules**: Patterns appearing in 95%+ of new articles that aren't in current guide
- **Rule Modifications**: Existing rules that new articles consistently contradict
- **Confirmed Rules**: Existing rules that new articles follow (no action needed)
- **Edge Cases**: Unusual patterns that may warrant adding exceptions

## Step 4: Generate Update Report

Create report showing proposed changes:

```markdown
# Style Guide Update Report: $1

**Current Version:** [X.X]
**Proposed Version:** [X.Y]
**New Articles Analyzed:** [number]
**Date:** [current date]

---

## Proposed Changes

### New Rules to Add

**Section [X] - [Section Name]:**
- **New Rule:** [description]
  - **Evidence:** Found in [X]/[Y] new articles
  - **Example:** [example from articles]

### Rules to Modify

**Section [X] - [Section Name]:**
- **Current Rule:** [existing text]
- **Proposed Change:** [new text]
- **Reason:** New articles show [pattern] in [X]/[Y] cases

### Rules Confirmed (No Changes)

- Section 1: [X] rules confirmed
- Section 2: [X] rules confirmed
- ...

### Potential Exceptions to Add

- **Rule:** [existing rule]
- **Exception:** [new exception based on articles]
- **Example:** [example showing valid exception]

---

## Summary

- New rules to add: [X]
- Rules to modify: [X]
- Rules confirmed: [X]
- Exceptions to add: [X]
```

## Step 5: Apply Updates (with confirmation)

**Present proposed changes to user:**
- Display the full update report
- Ask for confirmation: "Apply these updates to the style guide? (yes/no/review)"

**If user confirms:**
1. Update `brands/$1/style-guide.md` with approved changes
2. Increment version number:
   - Minor update (new rules only): 1.0 → 1.1
   - Major update (rule modifications): 1.0 → 2.0
3. Update "Last Updated" date in style guide
4. Add changelog entry at bottom of style guide:
   ```markdown
   ---
   ## Changelog

   ### Version [X.Y] - [Date]
   - Added: [list new rules]
   - Modified: [list changed rules]
   - Based on analysis of [X] additional articles
   ```
5. Copy new articles to `brands/$1/source-articles/`
6. Update source-articles README with new article count

**If user declines:**
- Save report to `docs/logs/[date]_style-guide-update-proposal_$1.md` for future reference
- Do not modify style guide

**If user wants to review:**
- Allow user to approve/reject individual changes
- Apply only approved changes

## Step 6: Validation

After applying updates:
- Run `/validate-style-guide $1` to check for contradictions
- Report any issues found
- If validation fails: Warn user and suggest manual review

## Usage Examples

```bash
# Update style guide with new articles
/update-style-guide animalz /path/to/new-articles/

# Update after publishing new content
/update-style-guide hubspot brands/hubspot/recent-posts/

# Update with articles from external source
/update-style-guide acme ~/Downloads/acme-blog-posts/
```

## Error Handling

- **Style guide not found**: Suggest creating one with `/generate-style-guide`
- **No new articles found**: Clear error with path suggestions
- **Duplicate articles detected**: Warn and exclude duplicates
- **Fewer than 3 new articles**: Warn about reliability but allow proceeding
- **Conflicting patterns in new articles**: Flag for manual review

## Best Practices

- Run updates quarterly or after publishing 5+ new articles
- Review proposed changes carefully before applying
- Keep changelog entries concise but informative
- After major updates, run `/batch-review` on recent articles to verify alignment
