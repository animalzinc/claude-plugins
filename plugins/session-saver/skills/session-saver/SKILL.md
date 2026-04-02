<!-- SYNC: Personal version at ~/.claude/commands/save-session.md -->
---
name: Session Saver
description: Save a structured session log so the next session can pick up where you left off
triggers:
  - save session
  - session summary
  - pick up where I left off
  - save progress
  - end of session
  - session log
---

# Session Saver

You are going to produce a concise session log and SAVE IT TO A FILE in the project repository.

**Remember**: This session log and the codebase are the ONLY things that persist between sessions. The current conversation will be LOST. Capture any planned but unimplemented work in detail.

## Task

1. **Session summary**: Summarize today's objectives, notable prompts, key decisions, and achievements.
2. **Files changed**: List all modified/created files with 1-line descriptions of changes.
3. **Referenced materials**: List paths, directories, files, or links that were shared or referenced during the session but not modified. Includes workflow paths, reference documents, external URLs, and resources that provide important context.
4. **Technical notes**: Brief notes on important discoveries, patterns used, issues resolved, or unresolved issues.
5. **Future plans**: DETAILED capture of any unimplemented work, including:
   - Exact steps planned for each future phase
   - Specific implementation details discussed
   - Any design decisions or approaches agreed upon
6. **Open items**: List open questions/next actions as checkboxes.
7. **Metrics** (if available): Number of files changed, tests added/modified, lines added/removed.

## Format requirements

- Use ISO date format (YYYY-MM-DD) in the heading
- Include project path/name at the top
- Add session duration if available
- Tag the session type: [feature] [bugfix] [refactor] [docs] [config] [testing]

## Output structure

```markdown
## Session Log: [YYYY-MM-DD]

**Project**: [project-name or path]
**Duration**: [if available]
**Type**: [feature/bugfix/refactor/docs/config/testing]

### Objectives
- [Primary goal]
- [Secondary goals if any]

### Summary
[2-3 sentences describing what was accomplished]

### Files Changed
- `path/to/file1.ext` - Brief description of change
- `path/to/file2.ext` - Brief description of change

### Referenced Materials
*(Paths, directories, links, or resources shared/referenced this session — not modified, but important for context)*
- `path/to/workflow/directory/` - Description of what this is
- `path/to/reference/file.md` - Why it was referenced
- https://example.com/resource - External resource consulted

### Technical Notes
- [Key learning or pattern discovered]
- [Important decision made and why]

### Future Plans & Unimplemented Phases
*(Include this section only if there ARE unimplemented phases)*

#### Phase [X]: [Name]
**Status**: Not started / Partially complete
**Planned Steps**:
1. [Specific step with implementation details]
2. [Specific step with implementation details]

### Next Actions
- [ ] Todo item 1
- [ ] Todo item 2
- [ ] Question or investigation needed

### Metrics
- Files modified: X
- Files created: Y
- Tests added: Z

### Continuation Prompt
Project: [project-name]
Session log: docs/SESSION_LOG.md
Section: "## Session Log: [YYYY-MM-DD]" ([project/type] entry)

Context: [1-2 sentence summary of what we were working on]

Key points:
- [Key point 1]
- [Key point 2]
- [Key point 3 if applicable]

Referenced paths:
- [Only paths relevant to continuing this work]

Read the session log section above, familiarize yourself with the context, and let me know when ready to continue.

*(Leave sections empty if nothing to report. Delete empty sections before saving.)*
```

## Execution steps

Steps are ordered for **low-context resilience** — the session log is written to disk as early as possible. If context compaction happens during later steps, the core log is already saved.

1. **Check for existing session logs** (quick):
   - Use `ls docs/` to check if directory exists
   - Use `ls docs/SESSION_LOG.md` to check if file exists

2. **Check file size and auto-split if needed** (quick):
   - If `docs/SESSION_LOG.md` exists, count its lines: `wc -l docs/SESSION_LOG.md`
   - If >= 2,000 lines: Run this Bash command to split:
     ```bash
     total=$(wc -l < docs/SESSION_LOG.md) && \
     keep=1760 && \
     archive_lines=$((total - keep)) && \
     archive_date=$(head -n $archive_lines docs/SESSION_LOG.md | grep "## Session Log:" | tail -1 | sed 's/.*Session Log: //') && \
     mkdir -p docs/logs && \
     head -n $archive_lines docs/SESSION_LOG.md > "docs/logs/SESSION_LOG_ARCHIVE_${archive_date}.md" && \
     tail -n $keep docs/SESSION_LOG.md > docs/SESSION_LOG.md.tmp && \
     mv docs/SESSION_LOG.md.tmp docs/SESSION_LOG.md && \
     echo "Archived $archive_lines lines to docs/logs/SESSION_LOG_ARCHIVE_${archive_date}.md"
     ```
   - If < 2,000 lines: proceed normally

3. **Generate the session log content** following the output structure above

4. **Write to disk immediately**:
   - If `docs/SESSION_LOG.md` exists: Use the Edit tool to APPEND the new session log to the existing file
   - If it doesn't exist: Use the Write tool to CREATE the file with the session log
   - The session log should be added at the END of the existing file with a separator line (`---`)
   - **Include the Continuation Prompt section** as the last section of the entry

5. **Verify the save**:
   - Use the Read tool to confirm the session log was actually written to `docs/SESSION_LOG.md`
   - Confirm that any future phases/plans are clearly documented in the file

6. **Output confirmation** to the user:
   - Show what was saved

7. **Display the continuation prompt** to the user as a copyable block:
   - Extract the Continuation Prompt from the saved log entry and display it
   - Output format:
     ```
     ---
     **Next Session Prompt** (copy this to start your next session):

     [Contents of the Continuation Prompt section]
     ---
     ```

## Continuation prompt — referenced paths curation

- For "Referenced paths" in the Continuation Prompt: Review the full Referenced Materials list and include ONLY paths relevant for continuing the work
- Omit files that were just processed or consulted for one-off questions
- Focus on: active workflow paths, documents being iterated on, directories the user will likely need to navigate to again

## Save requirements

- Use Write or Edit tool to save the file (not just console output)
- Include any planned but incomplete phases in the saved file

## Tips

- Focus on what changed, not how (no diffs)
- Be concise but informative
- Verify the file was saved by reading it back
