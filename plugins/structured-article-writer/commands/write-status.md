<!-- SYNC: Personal version in writing-assistant/.claude/commands/write-status.md -->

# /write-status

Quick status check for articles in the writing process.

## Arguments

$ARGUMENTS — Optional: article slug. If not provided, show all in-progress articles.

## Process

### If a slug is provided
1. Read `articles/{slug}/state.md`
2. Report:
   - **Title:** {title}
   - **Current phase:** Phase {X}/8: {name}
   - **Phases completed:** list with dates
   - **Quality gates passed:** list
   - **Thesis:** {thesis}
   - **Target:** {word_count_target} words for {target_publication}
   - **Last updated:** {date}
   - **Last log entry:** {summary}

### If no slug provided
1. Scan all `articles/*/state.md` files
2. For each, report: title, current phase, last updated
3. Sort by last_updated (most recent first)
4. Separate into: In Progress / Completed

Keep the output concise — this is a quick status check, not a deep review.
