---
name: research-ideation
description: Generate structured research questions, testable hypotheses, and empirical strategies from a topic or dataset
argument-hint: "[topic, phenomenon, or dataset description]"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# Research Ideation

Generate structured research questions, testable hypotheses, and empirical strategies.

**Input:** `$ARGUMENTS` — a topic, phenomenon, or dataset description.

---

## Steps

1. **Understand the input.** Read `$ARGUMENTS` and any referenced files. Check `literature_*/` for related papers.

2. **Generate 3-5 research questions** ordered from descriptive to causal:
   - **Descriptive:** What are the patterns?
   - **Correlational:** What factors are associated?
   - **Causal:** What is the effect?
   - **Mechanism:** Why does the effect exist?
   - **Policy:** What are the implications?

3. **For each research question, develop:**
   - **Hypothesis:** A testable prediction with expected sign/magnitude
   - **Identification strategy:** How to establish causality (DiD, IV, RDD, etc.)
   - **Data requirements:** What data is needed? Available?
   - **Key assumptions:** What must hold?
   - **Potential pitfalls:** Common threats to identification
   - **Related literature:** 2-3 papers using similar approaches

4. **Rank** by feasibility and contribution.

5. **Save** to `quality_reports/research_ideation_[sanitized_topic].md`

---

## Principles

- **Be creative but grounded.** Every suggestion must be empirically feasible.
- **Think like a referee.** For each causal question, immediately identify the challenge.
- **Consider data availability.** Brilliant question + no data = not actionable.
