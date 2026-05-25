---
paths:
  - "paper/**/*.tex"
  - "presentation/**/*.tex"
  - "internal_reports/**/*.md"
---

# Paraphrase Discipline

**Repo context:** an empirical-economics analysis repository. On-demand rule set for
prose that paraphrases or derives content from a source document
(working paper, paper being summarized, internal note, Stata `.log`,
pipeline CSV, FOIA return). Complements
[`claim-discipline.md`](claim-discipline.md) with paraphrase-specific
guidance.

> **Status note:** the citation toolkit ships dormant in this project.
> This rule applies once narrative prose starts paraphrasing literature
> or pipeline output.

---

## The three paraphrase rules

### 1. Match precision; do not amplify it

The paraphrase must not add precision (numbers, comparators, time
periods, specificity) that is not in the source.

| Source says | Paraphrase should NOT say (unless independently verified) |
|---|---|
| "Enforcement crackdowns can raise local violence." | "Enforcement crackdowns cause large increases in violence." (The source allows ambiguity; the paraphrase removes it.) |
| "The scraper identified ~50 intervention events." | "The scraper identified exactly 50 / over 50 / fewer than 50 intervention events." (Use what the source says.) |
| "Among four countries in the region including country A." | "Country A ranks first / second / among the highest." (The source does not rank.) |
| "We are not aware of recent quasi-experimental evaluations of policing in the study city." | "There are no studies of policing in the study city." (The hedge in the source is informative; preserve it.) |
| "Table 3, col 2: coefficient = -0.118 (SE 0.031), p < 0.01." | "The intervention dramatically reduces the outcome." (Source gives a magnitude and SE; paraphrase loses both and adds an adjective.) |

When the source uses a hedge ("approximately", "around", "may", "we
are not aware of"), the paraphrase must preserve the same level of
hedging or stronger.

### 2. Preserve attribution

When paraphrasing a substantive claim from a source, attribute it to
the source via:

- A formal `\citep{}` or `\citet{}` to the source, or
- A direct verbal attribution ("Smith (2020) finds that…",
  "Martin & Roberts (2018) survey…", "the regression in
  `4_Analysis_Standard_DiD_Daily.do` shows…").

Do not present the source's claim as the writer's own observation
unless the writer is independently demonstrating it. In this project:

- **From the literature:** "Brown (2010) introduces the framework"
  — attribute, do not assert as if it were a stylized fact.
- **From the pipeline:** "Our main DiD specification (Table 1, col 2)
  finds an 11.8% reduction" — attribute to the table, not to memory.

### 3. Tag cross-section and cross-experiment carefully

When the source has multiple studies, experiments, sections, or
sub-samples, the paraphrase must specify which part of the source it
draws from.

**Example failure mode** (from policing-and-crime literature with
parallel specifications):

- Suppose the source paper has two specs: a daily DiD and a monthly
  DiD.
- The daily DiD clusters at the neighborhood-day level.
- The monthly DiD clusters at the neighborhood-month level and uses a
  different control set.
- A paraphrase that says "the paper clusters at the neighborhood level and
  uses control set X" without specifying which spec conflates the
  two — a cross-experiment confusion.

**Example failure mode in this project itself:**

- The repo has `4_Analysis_Standard_DiD_Daily.do`,
  `4_Analysis_Standard_DiD_Weekly.do`, `4_Analysis_Standard_DiD_Monthly.do`.
- A paraphrase in the paper that says "we find an 11.8% reduction"
  must specify *which* spec (daily? weekly? monthly?). Do not let the
  reader assume.

**Mitigation:**

- When citing the source for a specific fact, mention the section,
  table, footnote, log file, or `.do` script in the source.
- When the source has parallel studies or sub-samples (or the repo
  has parallel `.do` files), tag which one a fact comes from at
  first mention.
- If unsure which sub-part of the source a fact belongs to, ask the
  user before paraphrasing.

---

## Practical guidance

- **First-mention specificity.** When paraphrasing a specific number
  or sample size, attribute the source on first mention: *"The
  scraped event panel covers 51 events across 7 treated units over 2016–2024
  (`<pipeline-output-path>/final_event_panel.csv`)."*
- **Multi-spec disambiguation.** When the analysis pipeline has
  multiple specifications: *"Our preferred specification (daily DiD,
  `4_Analysis_Standard_DiD_Daily.do`) finds…"* — script + spec
  reference makes the paraphrase verifiable.
- **Multi-study disambiguation in the literature.** *"Smith (2020,
  Section IV.B, panel close-elections RDD) finds…"* — section
  reference makes the source–paraphrase mapping verifiable.
- **Preserve hedges.** If a Stata `.log` records the coefficient as
  "significant at the 10% level only", do not paraphrase as
  "significantly reduces" — preserve the hedge.
- **Re-read derived prose against the source at least once.** Drift
  accumulates across edits; a final pass against the source catches
  it. The [`/source-audit`](../skills/source-audit/SKILL.md) skill
  automates this.

---

## What this rule is *not*

- Not a substitute for [`claim-discipline.md`](claim-discipline.md) —
  that rule covers writing posture broadly. This rule covers
  paraphrase specifically.
- Not a substitute for the
  [`/source-audit`](../skills/source-audit/SKILL.md) skill — that
  skill performs the audit; this rule articulates the standard the
  audit checks against.

---

## Related skills and rules

- [`/source-audit`](../skills/source-audit/SKILL.md) — skill that
  audits a draft section against a source document (paper PDF, Stata
  `.log`, pipeline CSV, `.do` header).
- [`source-fact-checker`](../agents/source-fact-checker.md) agent —
  per-claim fresh-context verifier.
- [`/cross-doc-audit`](../skills/cross-doc-audit/SKILL.md) — audit
  substantive consistency across two or more peer documents.
- [`.claude/rules/claim-discipline.md`](claim-discipline.md) — broader
  claim discipline.
- [`verify-citations`](../skills/verify-citations/SKILL.md) skill and
  [`/audit-citations`](../skills/audit-citations/SKILL.md) command —
  for formal `\citep{}` entries.
- [`.claude/rules/fact-audit-log.md`](fact-audit-log.md) — schema for
  the `.fact-audit.md` sidecar where non-cite factual claims are
  logged.
