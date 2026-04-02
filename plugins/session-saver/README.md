# Session Saver

Save structured session logs so the next Claude Code session can pick up where you left off.

## The problem

Multi-day projects in Claude Code lose all conversation context between sessions. You start fresh every time, re-explaining what you were doing and where you left off.

## What it does

Session Saver captures the current session state to `docs/SESSION_LOG.md` in your project, including:

- **Objectives and summary:** What you set out to do and what got done
- **Files changed:** Every modified/created file with a 1-line description
- **Referenced materials:** Paths, links, and resources consulted during the session
- **Technical notes:** Key discoveries, decisions, and patterns
- **Future plans:** Detailed capture of unimplemented phases with specific steps
- **Next actions:** Open items as checkboxes
- **Continuation prompt:** A ready-to-paste prompt for your next session

The log file auto-splits when it exceeds 2,000 lines, archiving older entries to `docs/logs/`.

## Usage

Say "save session", "save progress", or "session summary" at the end of a session. Copy the continuation prompt it generates into your next session to resume with full context.

## Install

```bash
/plugin install session-saver
```

## Author

Tim Metz @ [Animalz](https://animalz.co)

## License

MIT
