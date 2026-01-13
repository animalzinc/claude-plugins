---
description: Review blog article against editorial style guide using 8 specialized agents
argument-hint: [brand-name] [article-path] [--auto-apply] [--dry-run]
---

# Style Check: Multi-Agent Article Review

Review the article at **$2** against the **$1** brand style guide using 8 specialized agents running in parallel.

## Step 1: Validate Inputs

Before proceeding:
- Verify style guide exists at `brands/$1/style-guide.md`
  - If missing: Error and suggest running `/generate-style-guide $1 [source]`
- Verify article exists at $2
  - If missing: Error with clear message
- Check for `--auto-apply` flag (determines whether to apply corrections automatically)
- Check for `--dry-run` flag (shows what would be changed without modifying files)
- Note: `--dry-run` takes precedence over `--auto-apply` if both are specified

## Step 2: Read Required Files

Read the following files:
- Article to review: $2
- Brand style guide: `brands/$1/style-guide.md`
- All 8 agent prompts from `.claude/prompts/`:
  - voice-tone-agent.md
  - grammar-usage-agent.md
  - punctuation-agent.md
  - formatting-agent.md
  - technical-standards-agent.md
  - content-patterns-agent.md
  - industry-terms-agent.md
  - quick-reference-agent.md

## Step 3: Launch 8 Specialized Agents in Parallel

**CRITICAL: Use Task tool to launch ALL 8 agents simultaneously in a SINGLE message.**

Each agent should receive:
- The agent prompt from `.claude/prompts/[agent-name].md`
- The complete article content from $2
- The relevant section(s) from `brands/$1/style-guide.md`

**Launch these 8 agents in parallel:**

1. **Agent 1 - Voice & Tone**: Review against Section 1 of style guide
2. **Agent 2 - Grammar & Usage**: Review against Section 2 of style guide
3. **Agent 3 - Punctuation**: Review against Section 3 of style guide
4. **Agent 4 - Formatting**: Review against Section 4 of style guide
5. **Agent 5 - Technical Standards**: Review against Section 5 of style guide
6. **Agent 6 - Content Patterns**: Review against Section 6 of style guide
7. **Agent 7 - Industry Terms**: Review against Section 7 of style guide
8. **Agent 8 - Quick Reference**: Final comprehensive check against Section 8

**Each agent must return:**
- List of violations with line numbers
- Specific corrections for each issue
- Citation of relevant style guide rules

## Step 4: Aggregate Findings

Once all 8 agents complete:
- Collect all violation reports
- Remove duplicate findings (if multiple agents caught same issue)
- Sort violations by line number (top to bottom)
- Calculate total violations by category
- Determine severity (High/Medium/Low)

## Step 5: Generate Review Report

Create a structured report:

```markdown
# Style Check Report: $1

**Article:** $2
**Brand:** $1
**Review Date:** [current date]
**Total Violations:** [number]

---

## Summary by Section

- Voice & Tone: [X] violations
- Grammar & Usage: [X] violations
- Punctuation: [X] violations
- Formatting: [X] violations
- Technical Standards: [X] violations
- Content Patterns: [X] violations
- Industry Terms: [X] violations
- Additional (Quick Check): [X] violations

---

## Detailed Findings

### Agent 1 - Voice & Tone
[Paste agent findings]

### Agent 2 - Grammar & Usage
[Paste agent findings]

### Agent 3 - Punctuation
[Paste agent findings]

### Agent 4 - Formatting
[Paste agent findings]

### Agent 5 - Technical Standards
[Paste agent findings]

### Agent 6 - Content Patterns
[Paste agent findings]

### Agent 7 - Industry Terms
[Paste agent findings]

### Agent 8 - Quick Reference Check
[Paste agent findings]

---

## Priority Recommendations

**High Priority** (Brand voice/structural issues):
[List critical violations]

**Medium Priority** (Consistency/formatting):
[List standard violations]

**Low Priority** (Minor polish):
[List minor violations]

---

## Next Steps

- Review findings above
- To apply corrections automatically: `/article-edit $1 $2`
- To apply manually: Edit the article at $2 using the corrections provided
```

## Step 6: Conditional Auto-Apply or Dry Run

**If `--dry-run` flag is present:**
- Generate full report showing what WOULD be changed
- For each violation, show before/after preview:
  ```
  Line [X]: [current text]
       →  [corrected text]
  ```
- Do NOT modify any files
- Display at end: "DRY RUN COMPLETE: No files were modified"
- Show summary: "[X] corrections would be applied"

**If `--auto-apply` flag is present (and NOT --dry-run):**
- Proceed to apply all corrections automatically
- Work through violations from top to bottom by line number
- Use the Edit tool to apply each correction
- Save result to same path with `_edited` suffix (unless already in `edited/` folder)
- Generate before/after summary

**If neither flag is present:**
- Display the report
- Prompt user: "Review complete. Run `/article-edit $1 $2` to apply corrections."

## Step 7: Save Report

Save the review report to:
- `docs/logs/[YYYY-MM-DD]_style-check_$1_[article-name].md`

## Usage Examples

```bash
# Review only (no auto-apply)
/style-check animalz brands/animalz/articles/original/my-article.md

# Preview what would be changed without modifying files
/style-check animalz brands/animalz/articles/original/my-article.md --dry-run

# Review and automatically apply corrections
/style-check animalz brands/animalz/articles/original/my-article.md --auto-apply

# Review article from different location
/style-check hubspot /Users/name/Documents/draft-article.md
```

## Agent Failure Recovery

If an agent fails during parallel execution:

1. **Retry once** with the same inputs after a brief delay
2. **If retry fails**: Continue with remaining agents (don't fail entire review)
3. **Mark failed section** as "INCOMPLETE" in the report:
   ```
   ### Agent [X] - [Section Name]
   ⚠️ INCOMPLETE: Agent failed after retry. Manual review recommended for this section.
   ```
4. **Add warning** at top of report: "Note: [X] agent(s) failed. Some sections may be incomplete."
5. **Report success/failure** of each agent at end of review:
   ```
   Agent Status:
   - Agent 1 (Voice & Tone): ✅ Success
   - Agent 2 (Grammar & Usage): ❌ Failed (manual review needed)
   - Agent 3 (Punctuation): ✅ Success
   ...
   ```

Never fail the entire review due to a single agent failure.

## Error Handling

- **Style guide missing**: Provide helpful error with suggestion to generate one
- **Article not found**: Check path and provide clear error
- **Agent failures**: See "Agent Failure Recovery" section above
- **No violations found**: Celebrate! Report that article is fully compliant

## Performance Notes

- 8 agents running in parallel: ~5-10 minutes
- Sequential would take: ~40+ minutes
- Speedup factor: 4-5x
