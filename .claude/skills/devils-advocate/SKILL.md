---
name: devils-advocate
description: Challenge research design with 5-7 critical questions. Checks identification, data quality, alternative explanations, and potential referee objections.
argument-hint: "[analysis file, research design description, or 'full project']"
allowed-tools: ["Read", "Grep", "Glob"]
---

# Devil's Advocate Review

Critically examine the research design and challenge it with 5-7 specific questions.

**Philosophy:** "We arrive at the best possible research through active dialogue."

---

## Setup

1. **Read the target** (analysis file, specification, or full project)
2. **Read the rules** in `.claude/rules/did-event-study-checks.md` for domain-specific concerns
3. **Check existing analysis files** for context on what's already been done

---

## Challenge Categories

Generate 5-7 challenges from these categories:

### 1. Identification Challenges
> "What if the parallel trends assumption fails because of X?"

### 2. Treatment Variable Challenges
> "Could media reporting bias systematically affect which raids we observe?"

### 3. Alternative Explanation Challenges
> "Could this result be driven by Y rather than the raid itself?"

### 4. Data Quality Challenges
> "Is there a structural break in crime reporting during this period?"

### 5. External Validity Challenges
> "Do these results generalize beyond Buenos Aires informal settlements?"

### 6. Specification Challenges
> "What happens if we change the event window / geographic unit / crime category?"

### 7. Magnitude Challenges
> "Is the effect size plausible given what we know about criminal networks?"

---

## Output Format

```markdown
# Devil's Advocate: [Topic]

## Challenges

### Challenge 1: [Category] — [Short title]
**Question:** [The specific critical question]
**Why it matters:** [What could go wrong / what a referee would say]
**Suggested response:** [How to address it — additional test, robustness check, argument]
**Severity:** [High / Medium / Low]

## Summary Verdict
**Strengths:** [2-3 things the design does well]
**Critical to address:** [0-2 must-fix before submission]
**Worth investigating:** [2-3 additional robustness checks]
```

---

## Principles

- **Be specific:** Reference exact specifications and data choices
- **Be constructive:** Every challenge has a suggested response
- **Be honest:** If the design is strong, say so
- **Think like a hostile referee:** What would make them reject?
