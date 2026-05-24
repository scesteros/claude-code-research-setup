---
name: source-audit
description: User-invoked audit of prose claims against a designated source document (working-paper PDF, Stata `.log`, pipeline CSV, `.do` header, internal note, research plan, etc.). Trigger only when the user runs `/source-audit` or explicitly asks to verify prose against a specific source — e.g., "check this paragraph against the .log", "audit the data section against the codebook", "make sure the abstract matches the research plan". Do NOT auto-trigger from `.tex` edits or from passive heuristics about derived content. Different from /audit-citations (which targets formal `\citep{}` entries): /source-audit targets prose paraphrased or derived from a source even when no formal cite exists.
argument-hint: "[target file or section] [source PDF / .log / .csv / .do / .tex / .md]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Agent"]
---

# /source-audit

Audit prose for factual fidelity to a designated source document.

## When to use

- A section of the paper draft is paraphrased from a working paper, internal note, or other input document.
- **A number, point estimate, sample size, or descriptive statistic in the prose comes from this repo's analysis pipeline.** This is the most common use in this project: the paper draft asserts a coefficient or N, and the source is a Stata `.log` or a CSV under `output/tables/`.
- Before propagating a section across documents (paper → slides; paper → presentation; meeting notes → paper).
- When the user invokes `/source-audit` explicitly, or asks to "check the prose against the source", "verify what we wrote against the WP", "audit this section against the log", "check the numbers match the pipeline".
- Complements `/audit-citations`: the latter checks (citation, claim) pairs; this checks (prose claim, source location) pairs even when no formal cite exists.

### Source documents in this project — what counts

The "source" passed to this skill can be any of:

- **A Stata `.log` file** under `output/logs/` (the authoritative record of a regression run).
- **A CSV produced by the pipeline** under `output/tables/` (e.g., `main_did_daily.csv`, `event_study_stacked.csv`).
- **A `.do` file header or inline comment** that documents a sample restriction, treatment definition, or variable construction (use this when the prose asserts how a variable is built).
- **A working paper PDF** under `literature/methods/` or `literature/topic/`.
- **An information-request response** under `solicitudes_información/`.
- **A CABA government source document** (statute, decree, official codebook) for institutional facts about villas, comunas, or police jurisdictions.
- **A figure file** under `output/figures/` — for prose that describes what the figure shows (e.g., "the event-study plot shows no pre-trend").

If the source is a `.log` or `.csv`, treat it as a primary source. The Stata pipeline output is the authoritative value for any number the paper draft asserts about the analysis.

## Inputs

- **Target**: a path to a `.tex` file, a section of it, or a paragraph; alternatively a paragraph pasted by the user.
- **Source(s)**: a path to a PDF, `.tex`, `.md`, `.log`, `.csv`, or `.do` file the target is derived from. If the user does not specify, ask.
- Optional: specific dimensions the user wants checked (e.g., "just verify the point estimate", "just check the sample sizes").

If the source is not provided, ask before proceeding.

## Procedure

### 1. Enumerate substantive claims in the target

Read the target and list each substantive claim that should be source-grounded. A substantive claim is one of:

- A specific number, sample size, magnitude, date, percentage, point estimate, standard error, or F-statistic.
- An institutional fact (CABA agency jurisdictions, formal villa designation criteria, FARC/PRO trafficking-route boundaries, regulatory frameworks).
- An attribution ("the WP shows that…", "the regression in `4_Analysis_Standard_DiD_Daily.do` finds…").
- A characterization of a study's design, sample, outcome, or specification.
- A direct paraphrase of a passage from the source.

Skip:
- Pure rhetorical claims with no source-grounded content ("the question is interesting", "the literature is small").
- Claims already governed by formal `\citep{}` to other papers — those are for `/audit-citations`.

### 2. Locate each claim in the source

For each enumerated claim, search the source document for the corresponding passage. Use Grep/Read with section, page, table, footnote, log line, or CSV row references where possible. For PDFs, use the Read tool with the `pages` parameter.

For Stata `.log` files, search for: the model header (`reghdfe`, `xtreg`, `csdid`, etc.), the coefficient row of interest, the `N`, and any `vce(cluster ...)` annotation. For CSVs, identify the model column, the row for the relevant coefficient, and the units (percent vs. log points vs. levels).

### 3. Verify match dimension-by-dimension

Compare each prose claim against its source passage on:

- **Number / magnitude:** do the digits match? Are units the same? Is the value at the same level of aggregation? (Coefficient in logs vs. percent change is a common drift.)
- **Population / setting:** same sample, same time period, same unit of observation? (Daily vs. monthly panel; barrios vs. comunas; pre-2018 vs. full window.)
- **Direction / sign:** prose says "decrease", source says "decrease"?
- **Precision:** does the prose add quantifiers, comparators, or specificity not in the source ("sharpest", "first", "only", "primary", "robust to all specifications")?
- **Attribution:** is the claim attributed to the source, or stated as the writer's own finding?
- **Cross-section / cross-experiment:** if the source has multiple studies, experiments, or sections (or the Stata pipeline has multiple specifications), does the claim correctly map to the right one?

### 4. Issue a verdict per claim

- **VERIFIED** — every dimension matches; the prose accurately reflects the source.
- **DRIFT** — source supports the claim, but the prose paraphrase has shifted (added precision, narrowed scope, changed unit). Flag the specific drift dimension.
- **OVERCLAIM** — prose makes a stronger claim than the source supports. Flag and suggest a hedge.
- **UNSOURCED** — claim cannot be located in the source. Either the source does not support it, or the source pointer is wrong. Ask the user.
- **CROSS-SECTION-CONFLATION** — the source has multiple studies, experiments, or specs, and the prose has merged facts from different ones inappropriately. Flag and disambiguate. (Common in this project: prose quotes a coefficient from the daily DiD but attributes the SE pattern from the monthly DiD.)

### 5. Delegate verification to the agent for thoroughness

For long sections or multiple source documents, delegate individual claim checks to the `source-fact-checker` agent in fresh context. One agent invocation per claim (or per closely related claim cluster) keeps the verification rigorous and isolated from the writing context.

### 6. Produce the report

Present the audit inline in chat using this format:

```
Source audit — <target> against <source>

Claims audited: N
  VERIFIED:                 n_verified
  DRIFT:                    n_drift
  OVERCLAIM:                n_overclaim
  UNSOURCED:                n_unsourced
  CROSS-SECTION-CONFLATION: n_conflation

── DRIFT / OVERCLAIM / UNSOURCED / CONFLATION ──

1. [verdict] Target sentence: "..."
   Source location: <section / page / table / log-line / csv-row>
   Source says: "..."
   Specific failure: <which dimension drifted / what the source actually shows>
   Suggested fix: <rephrase | hedge | drop | clarify which spec / log / csv row>

2. ...

── VERIFIED (summary only) ──
n_verified claims confirmed. Details available on request.
```

### 7. Wait for user direction on non-VERIFIED claims

For each DRIFT / OVERCLAIM / UNSOURCED / CROSS-SECTION-CONFLATION, the user decides: rephrase, hedge, drop, or override. Do not modify the `.tex` automatically.

Verdicts go into `<paper-subdir>/.fact-audit.md` (see `.claude/rules/fact-audit-log.md`) — not `.citation-audit.md`. The two logs are complementary.

## Posture

- **Conservative.** Default to flagging when in doubt. Better to flag a verified claim than miss a drift.
- **Specific.** Quote the source location and the source text directly. For Stata output, quote the coefficient line and the `N` row verbatim.
- **No silent rewriting.** All fixes require user direction.
- **Pipeline numbers are authoritative.** If the prose says "homicides fall by 11.8%" and the `main_did.csv` cell says "-0.118 log points", that's a DRIFT (units), not VERIFIED — even though the magnitudes are arithmetically close.
- **Reuse where possible.** If the `.fact-audit.md` log already covers a (claim, source) pair under the same fingerprint and the source value has not changed, note it and skip.
- **Follow** `.claude/rules/claim-discipline.md` **and** `.claude/rules/paraphrase-discipline.md` as the substantive standards.

## Related

- `/audit-citations` — batch verification of formal `\citep{}` entries against the cited papers.
- `verify-citations` skill — per-citation substantive verification.
- `/cross-doc-audit` — audit substantive consistency across two or more peer documents (different concern: peer alignment rather than derivation fidelity).
- `.claude/rules/fact-audit-log.md` — schema and lifecycle of the `.fact-audit.md` sidecar.
- `.claude/rules/claim-discipline.md` — overarching claim posture.
- `.claude/rules/paraphrase-discipline.md` — paraphrase-specific standards.
- `source-fact-checker` agent — per-claim fresh-context verifier.
