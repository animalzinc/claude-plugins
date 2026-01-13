---
description: Batch review multiple blog articles against editorial style guide
argument-hint: [brand-name] [directory-path] [--auto-apply] [--dry-run]
---

# Batch Review: Process Multiple Articles

Review all articles in **$2** against the **$1** brand style guide.

## Step 1: Validate Inputs

Before proceeding:
- Verify style guide exists at `brands/$1/style-guide.md`
  - If missing: Error and suggest running `/generate-style-guide $1 [source]`
- Verify directory exists at $2
  - If missing: Error with clear message
- Check for `--auto-apply` flag (determines whether to apply corrections automatically)
- Check for `--dry-run` flag (shows what would be changed without modifying files)
- Note: `--dry-run` takes precedence over `--auto-apply` if both are specified

## Step 2: Discover Articles

Scan the directory at $2 for markdown files:
- Use Glob to find all `*.md` files in $2
- Exclude files ending with `_edited.md` (already processed)
- Exclude README.md files
- Sort by filename
- Report number of articles found

**If no articles found:**
- Provide clear message and exit

**If articles found:**
- Display list of articles to be reviewed
- Ask user to confirm: "Found [X] articles. Proceed with batch review? (yes/no)"

## Step 3: Process Each Article

For each article in the list:

### Option A: Sequential Processing (Default - More Reliable)
1. Display: "Processing article [N] of [total]: [filename]"
2. Run the equivalent of `/style-check $1 [article-path]` on this article
3. Collect findings
4. Handle based on flags:
   - If --dry-run: Show preview of changes for this article, no modifications
   - If --auto-apply: Apply corrections and save to `edited/` folder
   - If neither: Just report findings
5. Move to next article

### Option B: Parallel Processing (Faster but Resource-Intensive)
- If user confirms they want parallel processing:
- Batch articles into groups of 3
- Process each group in parallel
- Note: This will spawn 24 agents per batch (8 agents × 3 articles)

## Step 4: Aggregate Portfolio Results

After all articles processed, create portfolio compliance report:

```markdown
# Batch Review Report: $1

**Brand:** $1
**Source Directory:** $2
**Review Date:** [current date]
**Articles Reviewed:** [number]
**Auto-Apply:** [yes/no]

---

## Portfolio Compliance Summary

**Overall Statistics:**
- Total articles reviewed: [X]
- Fully compliant (0 violations): [X] articles ([%])
- Minor issues (1-5 violations): [X] articles ([%])
- Moderate issues (6-15 violations): [X] articles ([%])
- Major issues (16+ violations): [X] articles ([%])

**Total Violations Across Portfolio:**
- Voice & Tone: [X] violations
- Grammar & Usage: [X] violations
- Punctuation: [X] violations
- Formatting: [X] violations
- Technical Standards: [X] violations
- Content Patterns: [X] violations
- Industry Terms: [X] violations

**Average violations per article:** [number]

---

## Most Common Violations

1. [Most frequent issue]: [X] occurrences across [Y] articles
2. [Second most frequent]: [X] occurrences across [Y] articles
3. [Third most frequent]: [X] occurrences across [Y] articles
4. [etc.]

---

## Article-by-Article Summary

| Article | Total Violations | Status | Priority |
|---------|-----------------|--------|----------|
| [filename-1] | [X] | ✅/⚠️/❌ | High/Med/Low |
| [filename-2] | [X] | ✅/⚠️/❌ | High/Med/Low |
| [etc.] | [X] | ✅/⚠️/❌ | High/Med/Low |

**Legend:**
- ✅ Fully compliant (0 violations)
- ⚠️ Minor issues (1-5 violations)
- ❌ Needs attention (6+ violations)

---

## Priority Recommendations

### High Priority Articles (Review First)
[List articles with major brand voice/structural issues]

### Medium Priority Articles
[List articles with consistency/formatting issues]

### Low Priority Articles
[List articles with minor polish needed]

---

## Common Patterns to Address

**Voice & Tone Issues:**
[List common voice/tone violations seen across multiple articles]

**Grammar & Usage Issues:**
[List common grammar violations]

**Formatting Issues:**
[List common formatting violations]

[etc.]

---

## Next Steps

1. Review high-priority articles first
2. Consider updating style guide if new patterns emerge
3. For articles with 0 violations: Consider them as exemplars
4. For articles with many violations: May indicate style guide misalignment

**Files Generated:**
- Batch report: docs/logs/[date]_batch-review_$1.md
- Individual reports: docs/logs/[date]_style-check_$1_[article].md (for each article)
- Edited articles: $2/../edited/ (if --auto-apply used)
```

## Step 5: Save Reports

Save the following:
- **Portfolio report**: `docs/logs/[YYYY-MM-DD]_batch-review_$1.md`
- **Individual reports**: One per article in `docs/logs/`
- **Edited articles**: If --auto-apply, save to `brands/$1/articles/edited/` or `$2/../edited/`

## Step 6: Update Brand README

If `brands/$1/README.md` exists:
- Add note about this batch review
- Update "Last Reviewed" date
- Add summary statistics

If doesn't exist:
- Create basic README with review statistics

## Usage Examples

```bash
# Review all articles in directory (report only)
/batch-review animalz brands/animalz/articles/original/

# Preview all changes without modifying any files
/batch-review animalz brands/animalz/articles/original/ --dry-run

# Review and automatically apply corrections
/batch-review animalz brands/animalz/articles/original/ --auto-apply

# Review articles from any directory
/batch-review hubspot /Users/name/Documents/hubspot-drafts/
```

## Performance Estimates

**Sequential processing (default):**
- Time per article: ~5-10 minutes
- For 10 articles: ~50-100 minutes (1-2 hours)
- More reliable, less resource-intensive

**Parallel processing (if user requests):**
- Time for 3 articles (batch): ~10-15 minutes
- For 10 articles (4 batches): ~40-60 minutes
- Faster but more complex

## Agent Failure Recovery

If an agent fails during article review:

1. **Retry once** with the same inputs after a brief delay
2. **If retry fails**: Continue with remaining agents for that article
3. **Mark failed section** as "INCOMPLETE" in the individual article report
4. **Track failures** across batch: "Agent [X] failed on [Y] articles"
5. **Include in portfolio report**:
   ```
   Agent Reliability:
   - Agent 1 (Voice & Tone): 100% success (10/10 articles)
   - Agent 2 (Grammar & Usage): 90% success (9/10 articles)
   ...
   ```

Never fail the entire batch due to agent failures. Complete as much as possible.

## Error Handling

- **Style guide missing**: Provide helpful error with suggestion
- **Directory not found**: Check path and provide clear error
- **No articles found**: Inform user and suggest checking directory
- **Individual article failures**: Continue with remaining articles; note failures in report
- **Agent failures**: See "Agent Failure Recovery" section above
- **Permission issues**: Report which files couldn't be accessed

## Quality Assurance

After batch processing:
- Verify all articles were processed
- Check that reports were generated
- If --auto-apply: Verify edited files were created
- Count total violations vs. articles to ensure reasonable results
