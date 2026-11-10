---
type: llm
focus: { source: file, path: drafts/seeded-draft.style-check/findings/final.json }
---

The file is a JSON array of style-check findings, each with a "rule_id" and a "line". These 31 errors were planted in the draft, written as rule_id@line:

TERM-AI@8, TERM-BANNED@8 (twice: "leverage" and "seamless"), PUNC-EMDASH@8, STRUCT-LEDE@8, VOICE-CONCRETE@10, USAGE-STATS@10, NUM-THOUSANDS@12, NUM-PCT@12, PROOF-WORD@12, HEAD-CASE@14, PUNC-LABEL@16, NUM-SMALL@16, TERM-NAMES@17, HEAD-FORMAT@20, PUNC-SERIAL@22, NUM-SMALL@23, TERM-PREFER@24, STRUCT-STEPS@25, NUM-TIME@26, NUM-ORD@27, USAGE-ACRONYM@27, PUNC-QUOTES@36, PROOF-DOUBLE@36, PROOF-NAME@40, NUM-START@42, NUM-MONEY@42, NUM-DATE@42, PROOF-TYPO@46, LINK-HERE@46, LINK-CLEAN@46.

PASS if at least 28 of the 31 planted errors appear as a finding with that rule_id on that line, and at most 3 findings in the file match no planted error.
FAIL if fewer than 28 planted errors are found, or if more than 3 findings match no planted error.
