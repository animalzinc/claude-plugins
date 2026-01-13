---
description: Validate style guide for internal consistency and completeness
argument-hint: [brand-name]
---

# Validate Style Guide

Check the **$1** style guide for internal contradictions, completeness, and quality issues.

## Step 1: Load Style Guide

- Read style guide from `brands/$1/style-guide.md`
- If not found: Error and suggest running `/generate-style-guide $1 [source]`
- Parse the document into 8 sections
- Extract all rules, examples, and exceptions

## Step 2: Run Completeness Checks

### Required Sections
- [ ] Section 1: Voice & Tone
- [ ] Section 2: Grammar & Usage
- [ ] Section 3: Punctuation
- [ ] Section 4: Formatting
- [ ] Section 5: Technical Standards
- [ ] Section 6: Content Patterns
- [ ] Section 7: Industry-Specific Terms
- [ ] Section 8: Quick Reference Checklist

**For each section, verify:**
- Section header exists
- At least 3 subsections present
- At least 5 rules per section
- Each rule has at least one example

### Rule Count
- Count total rules across all sections
- Target: 50+ rules
- Warning if <50 rules: "Style guide may be incomplete"
- Critical if <30 rules: "Style guide needs expansion"

### Example Coverage
- Count rules with examples
- Target: 90%+ rules should have examples
- Flag rules missing examples

## Step 3: Run Consistency Checks

### Cross-Section Contradictions
Check for rules that contradict each other across sections:

**Common contradiction patterns to detect:**
- Section 1 (Voice) says "use contractions" but Section 2 (Grammar) says "avoid contractions"
- Section 3 (Punctuation) says "em dash with spaces" but examples show without spaces
- Section 4 (Formatting) heading case rule conflicts with Section 2 capitalization rule
- Section 5 (Technical) date format conflicts with examples in other sections

### Example Consistency
- Check that DO examples don't appear in DON'T sections
- Verify examples follow the rules they illustrate
- Flag contradictory examples

### Terminology Consistency
- Extract all defined terms from Section 7
- Check if same terms are used consistently throughout document
- Flag inconsistent capitalization of product/brand names

### Quick Reference Alignment
- Verify Section 8 checklist covers rules from all other sections
- Flag critical rules missing from quick reference
- Check that checklist items match actual rules (not outdated)

## Step 4: Run Quality Checks

### Example Specificity
- Flag generic placeholder examples (e.g., "[insert example here]")
- Warn about overly similar examples (may not show rule breadth)
- Verify examples are realistic and relevant

### Rule Actionability
- Flag vague rules that can't be objectively applied:
  - "Write in a friendly tone" (how is "friendly" measured?)
  - "Use appropriate formatting" (what's appropriate?)
- Suggest making vague rules more specific

### Exception Documentation
- Identify rules that likely need exceptions but don't have them
- Check that exceptions have clear trigger conditions
- Verify exceptions don't undermine the main rule

### Formatting Consistency
- Check heading hierarchy is consistent
- Verify bullet point and numbering style is consistent
- Check DO/DON'T format is used consistently

## Step 5: Generate Validation Report

```markdown
# Style Guide Validation Report: $1

**Validation Date:** [current date]
**Style Guide Version:** [version from document]
**Style Guide Location:** brands/$1/style-guide.md

---

## Overall Assessment

| Category | Status | Score |
|----------|--------|-------|
| Completeness | [Pass/Warn/Fail] | [X]/100 |
| Consistency | [Pass/Warn/Fail] | [X]/100 |
| Quality | [Pass/Warn/Fail] | [X]/100 |
| **Overall** | **[Pass/Warn/Fail]** | **[X]/100** |

---

## Completeness Results

**Sections Present:** [X]/8

| Section | Status | Rules | Examples |
|---------|--------|-------|----------|
| 1. Voice & Tone | [Present/Missing] | [X] | [X] |
| 2. Grammar & Usage | [Present/Missing] | [X] | [X] |
| 3. Punctuation | [Present/Missing] | [X] | [X] |
| 4. Formatting | [Present/Missing] | [X] | [X] |
| 5. Technical Standards | [Present/Missing] | [X] | [X] |
| 6. Content Patterns | [Present/Missing] | [X] | [X] |
| 7. Industry Terms | [Present/Missing] | [X] | [X] |
| 8. Quick Reference | [Present/Missing] | [X] | N/A |

**Total Rules:** [X]
**Rules with Examples:** [X] ([X]%)

### Completeness Issues Found

[List any missing sections, insufficient rules, or missing examples]

---

## Consistency Results

### Contradictions Found

**Critical (Must Fix):**
1. [Description of contradiction]
   - Section [X] says: "[rule text]"
   - Section [Y] says: "[conflicting rule text]"
   - **Recommendation:** [how to resolve]

**Warnings:**
1. [Description of potential inconsistency]

### Example Issues

[List examples that contradict rules or each other]

### Terminology Issues

[List terms used inconsistently]

---

## Quality Results

### Vague Rules (Need Clarification)

1. **Section [X]:** "[vague rule text]"
   - **Issue:** [why it's vague]
   - **Suggestion:** [how to make it specific]

### Missing Exceptions

1. **Rule:** "[rule that likely needs exceptions]"
   - **Potential Exception:** [suggested exception]

### Formatting Issues

[List any formatting inconsistencies]

---

## Recommended Actions

### Critical (Fix Immediately)
1. [Action item]
2. [Action item]

### Important (Fix Soon)
1. [Action item]
2. [Action item]

### Suggested (Nice to Have)
1. [Action item]
2. [Action item]

---

## Validation Summary

- **Contradictions found:** [X]
- **Missing elements:** [X]
- **Quality issues:** [X]
- **Total issues:** [X]

**Recommendation:** [Overall recommendation - e.g., "Style guide is ready for use" or "Address critical issues before using"]
```

## Step 6: Save Report

Save the validation report to:
- `docs/logs/[YYYY-MM-DD]_validate_$1.md`

Display summary to user with path to full report.

## Usage Examples

```bash
# Validate a style guide
/validate-style-guide animalz

# Validate after updates
/validate-style-guide hubspot

# Validate before using for reviews
/validate-style-guide acme
```

## Scoring Criteria

### Completeness Score (out of 100)
- All 8 sections present: +40 points
- 50+ rules total: +20 points
- 90%+ rules have examples: +20 points
- All sections have 3+ subsections: +10 points
- Quick reference covers all sections: +10 points

### Consistency Score (out of 100)
- No critical contradictions: +50 points
- No example conflicts: +20 points
- Terminology used consistently: +15 points
- Quick reference aligned with rules: +15 points

### Quality Score (out of 100)
- No vague/unactionable rules: +30 points
- All examples are specific: +25 points
- Exceptions documented where needed: +25 points
- Consistent formatting: +20 points

### Overall Pass/Warn/Fail
- **Pass**: Overall score 80+ and no critical issues
- **Warn**: Overall score 60-79 or has important issues
- **Fail**: Overall score <60 or has critical contradictions

## Error Handling

- **Style guide not found**: Suggest creating one
- **Style guide empty or corrupt**: Report parsing error
- **Partial parse failure**: Report which sections couldn't be parsed
