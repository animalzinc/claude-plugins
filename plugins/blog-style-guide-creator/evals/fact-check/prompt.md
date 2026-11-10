---
model: sonnet
runs: 1
max_turns: 100
timeout_seconds: 2400
allowed_tools: [Read, Write, Glob, Grep, Skill, Agent, Bash, WebSearch]
---

Run a style check of drafts/example-domains.md against the demo-brand style guide, with the fact-check of its claims and links. It is an essay written by a person. Report the findings; don't apply any fixes.
