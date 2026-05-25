---
paths:
  - "paper/**/*.tex"
  - "presentation/**/*.tex"
  - "internal_reports/**/*.md"
---

# Fact Audit Log

**Purpose.** Track substantive verification of **non-citation factual
claims** — numbers, institutional facts, dates, sample sizes,
percentages, regulatory descriptions, jurisdictional facts, point
estimates from the analysis pipeline. These claims often have no
`\citep{}` attached but are equally load-bearing for the document's
credibility.

Whereas `.citation-audit.md` tracks (cited paper, claim) pairs,
`.fact-audit.md` tracks (factual claim, primary source) pairs. The
two logs are complementary.

> **Status note (this project):** the fact-audit log is likely **the most
> immediately useful** piece of the citation toolkit in this repo,
> even before a full paper draft exists. Anytime a number or
> institutional fact is asserted in an internal report, a slide
> caption, or a `.tex` table — that number's primary source should be
> traceable. For this project, the primary source is almost always one of
> the pipeline outputs.

## When to use

Any time the prose asserts:

- A **number from the analysis pipeline** — point estimate, standard
  error, sample size, F-statistic, percentage change, observation
  count.
- A **number from the scraping/cleaning pipeline** — event count, unit
  count, panel coverage period, share of neighborhoods with ≥1 event.
- An **institutional fact** — what partner agency does what, which
  jurisdiction covers which treated unit, what a decree provides, what a
  FOIA-type return contained.
- A **descriptive characterization** about a setting or population
  that is not common knowledge (treated-vs-control definitional
  criteria, intervention-event operational definitions, etc.).
- A **trend** or **comparison** ("the outcome peaked in 2018", "events
  intensified post-2019").

If the claim is **common knowledge** (the study country is in a given
region; the study city is a federal district) no logging is needed. If
a reader could ask "where does that number come from?", log it.

## File location

One log per paper / report subdirectory, as a hidden but committed
file:

```
paper/.fact-audit.md
internal_reports/.fact-audit.md
```

## Schema

```markdown
# Fact Audit Log — <document name>

Last updated: <YYYY-MM-DD>

| claim_fingerprint | location | primary_source | source_value | doc_value | verdict | last_checked | overridden_by_user |
|---|---|---|---|---|---|---|---|
```

### Column definitions

| Column | Meaning |
|---|---|
| `claim_fingerprint` | Short paraphrase (≤20 words) of the factual claim. |
| `location` | `file:line` where the claim appears in prose. |
| `primary_source` | The authoritative source: a path under `output/` for pipeline outputs (preferred — see examples), a URL to an official document, a government decree, or a dataset codebook reference. |
| `source_value` | The verbatim value the source reports (with units). |
| `doc_value` | The value the prose currently asserts (with units). |
| `verdict` | `VERIFIED` (doc_value matches source_value, modulo stated rounding), `DRIFT` (doc_value is materially different from source_value), `UNSOURCED` (no primary source located), or `STALE` (source has been updated; doc may need refresh — common after a pipeline re-run). |
| `last_checked` | ISO date `YYYY-MM-DD`. |
| `overridden_by_user` | Brief rationale if the user kept a `doc_value` that differs from `source_value`. |

### Primary-source categories (this project)

The most common primary-source categories — and the example rows
below — emphasize this project's pipeline outputs:

- **Stata pipeline output (CSV or `.log`).** A regression coefficient,
  standard error, N, or F-stat must trace to a `.csv` row in
  `output/tables/` or a regression block in `output/logs/`. This is
  the **single most common case** in this project.
- **Scraping pipeline output.** An event count or event-window summary
  must trace to a `.csv` under `<pipeline-output-path>/` or
  the cleaned panel.
- **Government source document.** Statute, decree, official
  treated-area boundary map, agency mission statement.
- **External administrative source.** Partner-agency reports, national
  statistics, ministry-of-security publications.
- **FOIA-type return.** A document under `information_requests/`
  with a clear date and agency name.

### Example rows (crime-econometrics flavor)

```markdown
| Main DiD coefficient: the intervention reduces the daily outcome by 11.8% | paper/sections/04_results.tex:42 | this project pipeline output (output/tables/main_did_daily.csv, treated row, col=2, v2026-04) | -0.1184 (log points) | 11.8% (rounded) | VERIFIED | 2026-05-13 | User: paper reports the percent transformation; CSV reports log points; both consistent. |
| Standard error on main DiD: 3.1pp | paper/sections/04_results.tex:43 | this project pipeline output (output/tables/main_did_daily.csv, treated row, SE col) | 0.0312 (log SE) | 3.1pp | VERIFIED | 2026-05-13 |  |
| Sample period 2016–2024 | paper/sections/03_data.tex:11 | this project pipeline output (output/logs/3_Data_Analysis_I.log, panel range line) | 2016-01-01 to 2024-12-31 | 2016–2024 | VERIFIED | 2026-05-13 |  |
| 10 officially designated treated areas in the study city | paper/sections/03_data.tex:25 | City Decree NN/YYYY (formal treated-area registry) | 10 areas + 1 transitional site | "10 areas" | DRIFT | 2026-05-13 | User notes: decree lists 10 areas + 1 transitional housing site; add hedge "ten areas plus one transitional housing site". |
| ~50 validated intervention events 2016–2024 | paper/sections/03_data.tex:62 | this project scraping pipeline (<pipeline-output-path>/final_event_panel.csv, row count) | 51 rows | "approximately fifty" | VERIFIED | 2026-05-13 |  |
| 7 of 10 treated areas experienced ≥1 event 2016–2024 | paper/sections/03_data.tex:64 | this project pipeline output (output/tables/unit_event_summary.csv, treated unit count) | 7 units | 7 units | VERIFIED | 2026-05-13 |  |
| Event window: 30 days pre, 60 days post | paper/sections/03_methodology.tex:18 | analysis/8_Event_Study_Stacked.do header (lines 12–18) | [-30, +60] | "30 days pre, 60 days post" | VERIFIED | 2026-05-13 |  |
| First stage F-stat: 18.4 | paper/sections/04_results.tex:88 | this project pipeline output (output/logs/4_Analysis_Standard_DiD_Daily.log, first-stage block) | 14.7 | 18.4 | STALE | 2026-05-13 | User: paper was written before the 2026-04 re-run with the new clustering; needs update. |
```

## Workflow rules

1. **One row per (fact, location) pair.** Same fact in two different
   sentences → two rows.
2. **Update, do not duplicate.** When the fact is re-verified, replace
   the row.
3. **Update `Last updated`** when rows are added or modified.
4. **Never delete DRIFT or STALE rows without resolution.** A DRIFT or
   STALE row stays until the prose is updated or the user records an
   override.
5. **Cross-document numbers must agree.** If `paper/.fact-audit.md`
   says "51 event episodes" and `presentation/.fact-audit.md` says
   "approximately fifty", that's fine (rounding); but "51" vs "47"
   is a DRIFT that must be reconciled across documents (use
   `/cross-doc-audit` to find them).
6. **Pipeline re-runs trigger STALE re-verification.** When a `.do`
   file is re-run and `output/tables/*.csv` updates, every row whose
   `primary_source` points to a re-run CSV must be re-checked. The
   prose may still match (if the value did not change), or may now be
   STALE.

## Detecting "fact has changed" across drafts

When prose is edited and a number changes, compare against the
existing row. If the source value still matches, update the doc value
and re-verify. If the source has changed (e.g., the analysis pipeline
regenerated the panel with a different filter, or a new specification
was added), re-verify against the new source value and update both.

## What this log is NOT

- Not a substitute for `.citation-audit.md`. The two logs run
  side-by-side.
- Not a place for opinions or interpretations. Only facts with a
  primary source.
- Not a place for raw analysis output. Source the prose-asserted
  value; the underlying CSV / log lives where the pipeline put it.
- Not for transient sanity-check numbers in agent transcripts. Only
  for numbers that appear in shippable prose (paper, slides, internal
  report).

## Related skills and rules

- [`.claude/rules/citation-audit-log.md`](citation-audit-log.md) —
  companion log for cited papers.
- [`.claude/rules/claim-discipline.md`](claim-discipline.md) — broader
  claim-discipline framework. Rule §3 ("Verify before propagating")
  covers cross-document number drift.
- [`/source-audit`](../skills/source-audit/SKILL.md) skill — when
  prose paraphrases a source document (including a Stata `.log` or
  pipeline CSV), this skill audits the prose against the source.
  Outputs feed `.fact-audit.md`.
- [`/cross-doc-audit`](../skills/cross-doc-audit/SKILL.md) skill —
  when peer documents share substantive content, cross-check
  `.fact-audit.md` rows across documents for agreement.
- [`.claude/rules/verification-protocol.md`](verification-protocol.md)
  — code-side verification (Stata/Python). Together with this rule,
  forms the dual discipline: code is verified separately from prose,
  and prose is verified against code.
