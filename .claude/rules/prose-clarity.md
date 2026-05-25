---
paths:
  - "paper/**/*.tex"
  - "presentation/**/*.tex"
  - "internal_reports/**/*.md"
---

# Prose Clarity Rules

**Repo context:** an empirical-economics analysis repository. On-demand
rule set that distills paragraph-level discipline. Load this when
drafting or revising prose-heavy sections (Abstract, Introduction,
Motivation, Data, Identification, Results, Discussion, Conclusion of
the eventual paper draft, or any internal report). Complements — does
not replace — the writing conventions in `CLAUDE.md` and the
[`claim-discipline.md`](claim-discipline.md) /
[`paraphrase-discipline.md`](paraphrase-discipline.md) rules.

> **Status note:** the citation toolkit ships dormant in this project.
> This rule applies once narrative prose starts being written
> (paper draft, internal reports, slide deck speaker notes).

---

## The four paragraph-clarity questions

Apply these to every prose paragraph. If any answer is "no", revise.

1. **Does the paragraph have one explicit message?**
   One claim per paragraph. Two distinct claims → two paragraphs. In
   empirical economics writing, the topic sentence is the
   load-bearing claim; the rest of the paragraph defends it.

2. **Does the first sentence state what follows?**
   The opening sentence asserts the paragraph's point. It is not
   background, not a transition, not a question. (Topic sentences
   claim, not describe.)

3. **Are the key nouns and terms understandable from this paragraph
   alone?**
   No undefined acronyms (project-specific agency names, DiD, RDD, IV, SCM
   require first-mention expansion or a clear earlier definition),
   no concepts introduced in earlier sections without a one-clause
   reminder, no antecedents like "this approach" without an explicit
   referent.

4. **Does each sentence connect logically to the previous one?**
   The connection should be one of: cause, contrast, consequence,
   refinement, evidence, example. If a sentence does not connect, it
   does not belong in this paragraph.

---

## Discipline at the sentence level

- **Subject before verb, verb before object.** Avoid front-loading
  long subordinate clauses before the main verb.
- **One idea per sentence.** Two-clause sentences are fine;
  three-clause sentences usually hide a buried claim.
- **Numbers beat adjectives.** Prefer "an 11.8% reduction (SE 3.1pp)"
  over "a sizable reduction". Always.
- **Active voice, first-person plural** in own work; passive only
  when the agent is genuinely irrelevant.
- **Hedge to match design strength.** Causal verbs require causal
  designs. The staggered-DiD spec justifies "the intervention reduces the outcome";
  a simple cross-unit correlation justifies only "is associated
  with".

---

## Empirical-economics paragraph patterns

The recurring paragraph types in an empirical-economics paper, with
their topic-sentence templates:

| Paragraph type | Topic sentence template |
|---|---|
| **Motivation** | "We study [phenomenon] because [policy stake + literature gap]." |
| **Setting** | "[Setting] is characterized by [feature 1], [feature 2], [feature 3 — the one that enables identification]." |
| **Identification** | "Our identification rests on [exogenous variation], which is plausibly orthogonal to [main confound] because [reason]." |
| **Result** | "Table N, column C shows that [treatment] [direction-verb] [outcome] by [magnitude] ([precision]); the effect is [robustness statement]." |
| **Mechanism** | "Three features of the setting/data point to [channel]: [feature 1], [feature 2], [feature 3]." |
| **Caveat** | "This estimate likely [under/over]states the true effect because [confounder pattern]." |

In every case the topic sentence carries the claim and the body
defends it with one piece of evidence per sentence. The most common
failure in econ paragraphs is a topic sentence that *describes* the
section instead of stating a claim — "We now turn to the results"
instead of "The intervention reduces the daily outcome by 11.8%". Avoid the
former.

---

## What to cut on a clarity pass

- Throat-clearing: "In this paper...", "It is worth noting that...",
  "It is important to mention that..."
- Filler intensifiers: "very", "quite", "rather", "indeed" (unless
  contrastive).
- Redundant doublets: "first and foremost", "each and every".
- Empty transitions: "Moreover," "Furthermore," that do not actually
  mark contrast or addition.
- Forward references the reader cannot yet resolve ("as we will see
  in Section 5").
- Sentence-level hedges stacked on paragraph-level hedges (one hedge
  per claim, not three).

---

## Reverse outlining (quick check)

After drafting a section, write down only the topic sentence of each
paragraph in order. Read them as a list. The list should:

- Tell a coherent story by itself, without the body sentences.
- Show one claim per line, not background.
- Reveal logical sequence (motivation → setting → design → result →
  interpretation → caveat).

If the list does not read as a coherent argument, the section does
not — even if every individual paragraph reads fine. The fix is
structural, not sentence-level.

---

## Claim–evidence discipline

Every substantive claim has one of: an own result (table/figure from
this repo's pipeline), a citation, or an institutional source. Claims
without one of these belong in a working notes file (under
`internal_reports/` or `quality_reports/`), not in the manuscript.

The [`/claim-evidence-map`](../skills/claim-evidence-map/SKILL.md)
skill builds an explicit map for an entire section.

---

## What this rule is *not*

- Not a style guide for tables, figures, or LaTeX formatting (see
  [`latex-table-conventions.md`](latex-table-conventions.md),
  [`beamer-slides-conventions.md`](beamer-slides-conventions.md)).
- Not a substitute for `paper-reviewer` or `domain-reviewer` agents —
  those are full reviews, this is a self-discipline checklist.
- Not specific to any one section type. Apply uniformly across
  Abstract, Intro, Motivation, Data, Design, Results, Discussion,
  Conclusion.

---

## Related

- [`.claude/rules/claim-discipline.md`](claim-discipline.md) — overarching
  claim posture.
- [`.claude/rules/paraphrase-discipline.md`](paraphrase-discipline.md)
  — paraphrase-specific standards.
- [`.claude/rules/citation-integrity.md`](citation-integrity.md) —
  flagship zero-tolerance policy on citations.
- [`/claim-evidence-map`](../skills/claim-evidence-map/SKILL.md) — pre-
  submission claim×evidence table.
