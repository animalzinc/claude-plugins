---
type: llm
focus: { source: file, path: drafts/the-dashboard-nobody-opens.style-check/findings/final.json }
---

The file is a JSON array of style-check findings on an article written in the brand's own conventions. The brand's guide requires closed em dashes (no spaces around the dash), sentence-case headings, no serial comma before "and" or "or", "percent" spelled out, curly quotation marks, and bold list labels that end in a period.

A finding objects to a convention only when its rule_id, replacement, or comment asks to change that convention: spaces around an em dash or fewer em dashes, title-case headings, a serial comma, a percent sign, straight quotes, or a colon after a bold label. A finding about something else, such as a statistic's source or the article's structure, does not object to a convention even when its quote contains an em dash or the word "percent".

PASS if no finding objects to a convention. An empty array passes.
FAIL if any finding objects to a convention.
