---
type: regex
pattern: '"line": (29|30|31|32|38),'
match: not_contains
target: { source: file, path: drafts/seeded-draft.style-check/findings/final.json }
---
