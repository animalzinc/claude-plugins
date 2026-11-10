---
schema_version: 2
brand: Acme Analytics
content_types: [essay, how-to, customer-story]
generated: false
---

# Acme Analytics style guide

Acme Analytics makes AcmeBoard, a dashboard tool for small data teams. Acme, AcmeBoard, and every customer named in these files are fictional: the brand ships with blog-style-guide-creator as a worked example, and its conventions differ from common defaults on purpose (closed em dashes, sentence-case headings, no serial comma, percent spelled out), so a check that leaks one brand's habits into another shows up.

## Voice

### VOICE-PERSONA: Write as the AcmeBoard team, to a data lead
```rule
severity: should
scope: all
kind: voice
source: manual
evidence: all three source articles
```
We write as the people who build AcmeBoard ("we") to the person who runs a small data team ("you"). The reader knows SQL and has opinions about dashboards, so skip the basics and show the work.

✅ You don’t need to audit 140 dashboards at once.
❌ Dashboards are a powerful way for organizations to visualize data.

### VOICE-CONCRETE: Name what changed in someone’s week
```rule
severity: should
scope: all
kind: voice
source: manual
evidence: every claim of value in the source articles names a time or a task
```
A claim about value names what changed for a person: a report that went from a day to an hour, a meeting that ended early. "Unlock insights" and "drive value" give the reader nothing to check.

✅ The finance team stopped rebuilding the same pivot table every Monday.
❌ AcmeBoard unlocks powerful insights for every team.

## Structure

### STRUCT-LEDE: How-tos open with what the reader will have
```rule
severity: should
scope: [how-to]
kind: structure
source: articles
evidence: retire-a-dashboard opens with the routine the reader ends up with
```
The first paragraph of a how-to says what the reader will have when they finish, in one or two sentences. Context and motivation come after.

### STRUCT-STEPS: Numbered steps start with a verb
```rule
severity: should
scope: [how-to]
kind: structure
source: articles
evidence: 5 of 5 steps in retire-a-dashboard open with an imperative verb
```
Each numbered step opens with the verb the reader performs. A step that opens with a noun or a condition is rewritten so the action comes first.

✅ 1. Filter the list to dashboards nobody has opened in 90 days.
❌ 1. The list, filtered to dashboards nobody has opened in 90 days.

### STRUCT-RESULT: Customer stories lead with the result
```rule
severity: must
scope: [customer-story]
kind: structure
source: articles
evidence: pinecrest-weekly-report states the result in its headline and first paragraph
```
The customer’s result, with its number, appears in the headline or the first two paragraphs. The story of how they got there follows.

### STRUCT-ESSAY-END: Essays end on the reader’s next move
```rule
severity: prefer
scope: [essay]
kind: structure
source: articles
evidence: the-dashboard-nobody-opens ends on a first step
```
The last section of an essay gives the reader something to do on Monday morning. A summary of the essay’s points is cut.

## Usage

### USAGE-STATS: Every statistic has a source
```rule
severity: must
scope: all
kind: usage
source: manual
evidence: house rule
```
A number about the world names its source in the same sentence or links to it. A number from a customer’s own data names the customer, and a number from AcmeBoard usage says so.

✅ Of the dashboards created in a given quarter, 61 percent were opened fewer than five times (AcmeBoard usage, 2025).
❌ Most data leads lose a day a week to reporting.

### USAGE-ACRONYM: Spell out acronyms at first use
```rule
severity: should
scope: all
kind: usage
source: manual
evidence: house rule
```
Spell out an acronym the first time it appears and put the short form in parentheses. SQL, API and CSV need no expansion.

✅ The extract, transform and load (ETL) job runs at night.
❌ The ETL job runs at night.

### TERM-BANNED: Words Acme does not use
```rule
severity: must
scope: all
kind: usage
check: banned
terms: [leverage, seamless, seamlessly, best-in-class, synergy]
source: manual
evidence: house rule
```
These words promise more than they say. Write the plain verb or the specific benefit.

✅ Teams use their data to decide what to restock.
❌ Teams leverage their data to decide what to restock.

### TERM-AI: Phrases common in AI drafts
```rule
severity: should
scope: all
kind: usage
check: banned
terms: [delve, "fast-paced world", game-changer, "unlock the power"]
source: manual
evidence: house rule for AI-assisted drafts
audience: ai-drafting
```
These phrases appear far more often in AI-generated drafts than in Acme’s own writing. In a human draft they are suggestions.

✅ This guide covers the basics.
❌ This guide will delve into the basics.

### TERM-PREFER: Preferred forms
```rule
severity: should
scope: all
kind: usage
check: preferred
pairs: ["utilize => use", "utilise => use", "e-mail => email", "end-user => end user"]
source: manual
evidence: house rule
```
✅ Use the layout grid.
❌ Utilize the layout grid.

### TERM-NAMES: Product and company names
```rule
severity: must
scope: all
kind: usage
check: term-case
terms: [AcmeBoard, Acme Analytics, PostgreSQL]
source: articles
evidence: AcmeBoard appears 5 times across 3 articles, always in this form
```
✅ Open AcmeBoard and choose Usage.
❌ Open Acmeboard and choose Usage.

## Punctuation

### PUNC-EMDASH: Close up em dashes
```rule
severity: must
scope: all
kind: mechanical
check: dash-spacing
style: closed
ranges: en-dash
source: articles
evidence: 4 of 4 em dashes closed across 3 articles
```
An em dash touches the words on either side. Ranges take an en dash.

✅ Nobody deletes it—deleting feels like admitting the week was wasted.
❌ Nobody deletes it — deleting feels like admitting the week was wasted.

### PUNC-SERIAL: No serial comma
```rule
severity: should
scope: all
kind: mechanical
check: serial-comma
required: false
source: articles
evidence: 2 lists of three or more across 3 articles, both without the serial comma
```
Leave out the comma before "and" or "or" at the end of a list, unless the last two items would read as one.

✅ The exports came from the point-of-sale system, the warehouse and the web store.
❌ The exports came from the point-of-sale system, the warehouse, and the web store.

### PUNC-QUOTES: Curly quotes, punctuation inside
```rule
severity: must
scope: all
kind: mechanical
check: quote-style
marks: curly
punctuation_inside: true
source: articles
evidence: 8 curly double quotes and 11 curly apostrophes across 3 articles, no straight marks; 3 of 3 closing quotes with the punctuation inside
```
✅ She called it “the Monday report.”
❌ She called it "the Monday report".

### PUNC-LABEL: Bold labels end in a period
```rule
severity: should
scope: all
kind: mechanical
check: bold-label
separator: period
source: articles
evidence: 6 of 6 bold list labels end in a period inside the bold
```
✅ - **Owner.** The person who answers questions about it.
❌ - **Owner:** The person who answers questions about it.

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
source: articles
evidence: 8 of 10 level-2 headings in sentence case, none in title case
```
Capitalize the first word and proper nouns only.

✅ Keep the routine small
❌ Keep The Routine Small

### HEAD-FORMAT: No bold or end period in headings
```rule
severity: should
scope: all
kind: mechanical
check: heading-format
no_bold: true
no_end_period: true
source: manual
evidence: house rule
```
✅ Before you start
❌ Before you start.

## Numbers

### NUM-SMALL: Spell out numbers under ten
```rule
severity: should
scope: all
kind: mechanical
check: numerals
spell_out_below: 10
source: articles
evidence: 18 numbers under ten spelled out in prose across 3 articles, none as digits
```
Numbers from ten up are numerals. Percentages, money, times, and step numbers stay numerals at any size.

✅ It needs three things on each dashboard.
❌ It needs 3 things on each dashboard.

### NUM-ORD: Spell out small ordinals
```rule
severity: should
scope: all
kind: mechanical
check: ordinals
spell_out_below: 10
source: articles
evidence: 4 of 4 ordinals spelled out
```
✅ The second refresh catches late data.
❌ The 2nd refresh catches late data.

### NUM-START: No numeral at the start of a sentence
```rule
severity: must
scope: all
kind: mechanical
check: sentence-start-numeral
source: manual
evidence: house rule
```
Spell the number out or rewrite the sentence so it starts with another word.

✅ Twelve people opened the dashboard in its first week.
❌ 12 people opened the dashboard in its first week.

### NUM-PCT: Spell out percent
```rule
severity: should
scope: all
kind: mechanical
check: percent
style: word
source: articles
evidence: 61 percent and 40 percent; no percent signs across 3 articles
```
✅ Churn fell 12 percent.
❌ Churn fell 12%.

### NUM-MONEY: Write out million and billion
```rule
severity: should
scope: all
kind: mechanical
check: money
style: words
source: articles
evidence: $1.2 million; no abbreviated amounts across 3 articles
```
✅ The stores sell about $1.2 million on a busy weekend.
❌ The stores sell about $1.2M on a busy weekend.

### NUM-THOUSANDS: Thousands with a comma
```rule
severity: should
scope: all
kind: mechanical
check: thousands
style: comma
source: articles
evidence: 4,000 and $18,000; no k forms across 3 articles
```
✅ The report covers about 4,000 products.
❌ The report covers about 4k products.

### NUM-DATE: Dates without ordinals
```rule
severity: should
scope: all
kind: mechanical
check: date-format
ordinals: false
source: manual
evidence: house rule
```
✅ Refreshes are free on every plan since March 3.
❌ Refreshes are free on every plan since March 3rd.

### NUM-TIME: Times as 9 a.m.
```rule
severity: should
scope: all
kind: mechanical
check: time-format
style: 9 a.m.
source: articles
evidence: 3 of 3 times written as 9 a.m.
```
✅ Post the list at 9 a.m. on a Monday.
❌ Post the list at 9am on a Monday.

## Links and images

### LINK-CLEAN: Clean links with short anchors
```rule
severity: must
scope: all
kind: mechanical
check: link-hygiene
tracking: true
https: true
max_anchor_words: 8
source: manual
evidence: house rule
```
Links carry no tracking parameters, use https, and anchor on the few words that name the destination.

✅ Read the [retirement routine](https://acme.example/blog/retire-a-dashboard).
❌ Read the [retirement routine](https://acme.example/blog/retire-a-dashboard?utm_source=newsletter).

### LINK-HERE: Name the destination
```rule
severity: should
scope: all
kind: usage
check: regex
pattern: "\\b[Cc]lick here\\b"
message: Name the destination instead of saying click here.
source: manual
evidence: house rule
```
✅ Read the retirement routine.
❌ Click here to read the retirement routine.

### IMG-ALT: Every image has alt text
```rule
severity: must
scope: all
kind: mechanical
check: regex
pattern: "!\\[\\]\\("
message: Add alt text that says what the image shows.
source: manual
evidence: house rule
```
Alt text says what the image shows, in a phrase: "AcmeBoard usage tab sorted by last opened".

## Quick reference checklist

<!-- checklist:start -->
**Must:**

- [ ] STRUCT-RESULT: Customer stories lead with the result (customer-story)
- [ ] USAGE-STATS: Every statistic has a source
- [ ] TERM-BANNED: Words Acme does not use
- [ ] TERM-NAMES: Product and company names
- [ ] PUNC-EMDASH: Close up em dashes
- [ ] PUNC-QUOTES: Curly quotes, punctuation inside
- [ ] HEAD-CASE: Sentence-case headings
- [ ] NUM-START: No numeral at the start of a sentence
- [ ] LINK-CLEAN: Clean links with short anchors
- [ ] IMG-ALT: Every image has alt text

**Should:**

- [ ] VOICE-PERSONA: Write as the AcmeBoard team, to a data lead
- [ ] VOICE-CONCRETE: Name what changed in someone’s week
- [ ] STRUCT-LEDE: How-tos open with what the reader will have (how-to)
- [ ] STRUCT-STEPS: Numbered steps start with a verb (how-to)
- [ ] USAGE-ACRONYM: Spell out acronyms at first use
- [ ] TERM-AI: Phrases common in AI drafts
- [ ] TERM-PREFER: Preferred forms
- [ ] PUNC-SERIAL: No serial comma
- [ ] PUNC-LABEL: Bold labels end in a period
- [ ] HEAD-FORMAT: No bold or end period in headings
- [ ] NUM-SMALL: Spell out numbers under ten
- [ ] NUM-ORD: Spell out small ordinals
- [ ] NUM-PCT: Spell out percent
- [ ] NUM-MONEY: Write out million and billion
- [ ] NUM-THOUSANDS: Thousands with a comma
- [ ] NUM-DATE: Dates without ordinals
- [ ] NUM-TIME: Times as 9 a.m.
- [ ] LINK-HERE: Name the destination

**Prefer:**

- [ ] STRUCT-ESSAY-END: Essays end on the reader’s next move (essay)
<!-- checklist:end -->
