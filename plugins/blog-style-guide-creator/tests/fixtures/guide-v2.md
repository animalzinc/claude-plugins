---
schema_version: 2
brand: Demo Co
content_types: [essay, how-to]
generated: false
---

# Demo Co style guide

Rules for the Demo Co blog. A fictional brand used for tests.

## Punctuation

### PUNC-EMDASH: Close up em dashes
```rule
severity: must
scope: all
kind: mechanical
check: dash-spacing
style: closed
ranges: en-dash
source: manual
evidence: invented for tests
```
Write "tools—and", not "tools — and".

✅ The draft was late—again.
❌ The draft was late — again.

### PUNC-SERIAL: Use the serial comma
```rule
severity: should
scope: all
kind: mechanical
check: serial-comma
required: true
source: manual
evidence: invented for tests
```
✅ We tested kites, boats, and bikes.
❌ We tested kites, boats and bikes.

### PUNC-QUOTES: Curly quotes, punctuation inside
```rule
severity: must
scope: all
kind: mechanical
check: quote-style
marks: curly
punctuation_inside: true
source: manual
evidence: invented for tests
```
✅ She called it “the plan.”
❌ She called it "the plan".

### PUNC-LABEL: Bold labels end in a colon
```rule
severity: should
scope: all
kind: mechanical
check: bold-label
separator: colon
source: manual
evidence: invented for tests
```
✅ **Setup:** install the kit
❌ **Setup.** install the kit

## Headings

### HEAD-CASE: Sentence-case headings
```rule
severity: must
scope: all
kind: mechanical
check: heading-case
case: sentence
levels: [2, 3]
style: cmos
source: manual
evidence: invented for tests
```
✅ How the kite flies
❌ How The Kite Flies

### HEAD-FORMAT: No bold, no end period in headings
```rule
severity: should
scope: all
kind: mechanical
check: heading-format
no_bold: true
no_end_period: true
source: manual
evidence: invented for tests
```
✅ Getting started
❌ Getting started.

## Words

### WORD-BANNED: Banned words
```rule
severity: must
scope: all
kind: usage
check: banned
terms: [synergy, "game changer"]
source: manual
evidence: invented for tests
audience: ai-drafting
```
✅ The new kite helps.
❌ The new kite is a game changer.

### WORD-PREFER: Preferred forms
```rule
severity: should
scope: all
kind: usage
check: preferred
pairs: ["e-mail => email", "utilize => use"]
source: manual
evidence: invented for tests
```
✅ Send an email.
❌ Send an e-mail.

### WORD-NAMES: Product names
```rule
severity: must
scope: all
kind: usage
check: term-case
terms: [KiteKit, Demo Co]
source: manual
evidence: invented for tests
```
✅ Open KiteKit first.
❌ Open Kitekit first.

### WORD-TONE: Plain verbs
```rule
severity: prefer
scope: [essay]
kind: voice
source: manual
evidence: invented for tests
```
Prefer a plain verb to a phrase built on a noun.

### WORD-INTRO: Open with the point
```rule
severity: should
scope: [how-to]
kind: structure
source: manual
evidence: invented for tests
```
The first paragraph of a how-to says what the reader will be able to do.

## Numbers

### NUM-SMALL: Spell out numbers under ten
```rule
severity: should
scope: all
kind: mechanical
check: numerals
spell_out_below: 10
source: manual
evidence: invented for tests
```
✅ We built three kites.
❌ We built 3 kites.

### NUM-ORD: Spell out small ordinals
```rule
severity: should
scope: all
kind: mechanical
check: ordinals
spell_out_below: 10
source: manual
evidence: invented for tests
```
✅ The second kite flew.
❌ The 2nd kite flew.

### NUM-START: No numeral at a sentence start
```rule
severity: must
scope: all
kind: mechanical
check: sentence-start-numeral
source: manual
evidence: invented for tests
```
✅ Twelve kites flew.
❌ 12 kites flew.

### NUM-PCT: Percent sign
```rule
severity: should
scope: all
kind: mechanical
check: percent
style: symbol
source: manual
evidence: invented for tests
```
✅ Sales rose 40%.
❌ Sales rose 40 percent.

### NUM-MONEY: Abbreviated money
```rule
severity: should
scope: all
kind: mechanical
check: money
style: abbreviated
source: manual
evidence: invented for tests
```
✅ The round raised $2.5M.
❌ The round raised $2.5 million.

### NUM-THOUSANDS: Thousands with commas
```rule
severity: should
scope: all
kind: mechanical
check: thousands
style: comma
source: manual
evidence: invented for tests
```
✅ We sold 4,000 kites.
❌ We sold 4k kites.

### NUM-DATE: Dates without ordinals
```rule
severity: should
scope: all
kind: mechanical
check: date-format
ordinals: false
source: manual
evidence: invented for tests
```
✅ The launch is on March 12.
❌ The launch is on March 12th.

### NUM-TIME: Times as 9am
```rule
severity: should
scope: all
kind: mechanical
check: time-format
style: 9am
source: manual
evidence: invented for tests
```
✅ The call starts at 10am.
❌ The call starts at 10 a.m. sharp.

## Links

### LINK-CLEAN: Clean links
```rule
severity: must
scope: all
kind: mechanical
check: link-hygiene
tracking: true
https: true
max_anchor_words: 6
source: manual
evidence: invented for tests
```
✅ Read the [kite manual](https://example.com/manual).
❌ Read the [kite manual](https://example.com/manual?utm_source=news).

### LINK-PATTERN: No "click here"
```rule
severity: should
scope: all
kind: usage
check: regex
pattern: "\\b[Cc]lick here\\b"
message: Name the destination instead of saying click here.
source: manual
evidence: invented for tests
```
✅ Read the guide.
❌ Click here to read the guide.

## Quick reference checklist

<!-- checklist:start -->
<!-- checklist:end -->

## Retired

- PUNC-OLD: replaced by PUNC-EMDASH
