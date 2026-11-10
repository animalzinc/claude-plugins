---
type: regex
pattern: '"rule_id": "(PUNC|HEAD)-'
match: not_contains
target: { source: file, path: drafts/the-dashboard-nobody-opens.style-check/findings/final.json }
---
