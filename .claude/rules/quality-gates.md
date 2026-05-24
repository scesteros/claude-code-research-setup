---
paths:
  - "analysis/**/*.do"
  - "<pipeline-path>/**/*.py"
  - "output/**"
  - "presentation/**/*.tex"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** -- good enough to save
- **90/100 = PR** -- ready for review
- **95/100 = Excellence** -- publication-ready

## Stata .do Files

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax errors preventing execution | -100 |
| Critical | Hardcoded absolute paths (not using globals) | -20 |
| Critical | Wrong variable names / merge errors | -20 |
| Critical | Missing `drop _all` / `clear all` at start | -10 |
| Major | Missing comments on non-obvious sections | -5 |
| Major | Inconsistent naming conventions | -3 |
| Major | Missing `set more off` | -3 |
| Minor | Long lines (>120 chars) | -1 per line |
| Minor | Excessive blank lines | -1 |

## Python Scripts (.py)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax errors | -100 |
| Critical | Hardcoded paths outside config | -20 |
| Critical | Missing error handling for web requests | -15 |
| Major | No output validation | -10 |
| Major | Missing docstrings on functions | -5 |
| Minor | PEP8 violations | -1 per violation |

## Research Outputs (Tables & Figures)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Results don't match what code produces | -100 |
| Critical | Missing standard errors or significance | -20 |
| Major | Not publication-ready formatting | -10 |
| Major | Missing axis labels or legend | -5 |
| Major | Low resolution / wrong dimensions | -5 |
| Minor | Font inconsistency | -2 |

## Beamer Slides (.tex)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | LaTeX syntax errors preventing compilation | -100 |
| Critical | References to non-existent figures/tables | -20 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Overloaded frames (>1 key message per slide) | -10 |
| Major | Missing source attribution on figures | -5 |
| Major | Tables not reformatted for slides (>5 cols or >8 rows) | -5 |
| Major | Generic frame titles ("Results 1" instead of descriptive) | -3 |
| Minor | Inconsistent font sizes across frames | -2 |
| Minor | Missing non-breaking spaces before references | -1 |
| Minor | Unescaped special characters outside math mode | -1 |

## Enforcement

- **Score < 80:** Block commit. List blocking issues.
- **Score < 90:** Allow commit, warn. List recommendations.
- User can override with justification.

## Tolerance Thresholds (DiD / Event Studies)

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Point estimates | Display precision (3-4 decimals) | Stata rounding |
| Standard errors | Display precision | Clustering variation |
| Observation counts | Exact match | No reason for difference |
| Pre-trend coefficients | Same significance level | Parallel trends test |

## Citation integrity gate (`audit-citations` skill)

> **Status:** dormant until a paper draft begins. Once `paper/` (or
> any other `.tex` prose draft) contains formal `\cite*{}` calls,
> invoke `/audit-citations <paper-subdir>` manually. The skill
> produces two verdicts per cite (see
> [`citation-integrity.md`](citation-integrity.md) and
> [`citation-audit-log.md`](citation-audit-log.md)).

| Verdict | Severity | Effect on commit |
|---|---|---|
| Layer 1 `BIB_FAIL` — bib entry's authors / year / title / journal mismatches the OpenAlex/Crossref record at the cited DOI | CRITICAL | Block commit until rewritten. |
| Layer 2 `MISMATCH` — paper does not substantively support the specific claim (one of the failure modes in `citation-integrity.md`) | CRITICAL | Same. |
| Layer 2 `AMBIGUOUS` — paper partially supports the claim | MAJOR | Surfaced in the audit report; user decides whether to refix or accept. |
| Layer 2 `INACCESSIBLE` — paper cannot be obtained for substantive check | MAJOR | Logged; the entry may ship with the row marked `INACCESSIBLE` in the audit log, but flagged in the final summary. |
| Layer 1 `BIB_NO_DOI` — bib has no DOI, so the API match cannot be confirmed | MAJOR | Warning. User asked to add a DOI if possible; otherwise the entry ships with a `BIB_NO_DOI` annotation in the audit log. |
| Both layers pass (`BIB_OK + VALID`) | None | Commit. |

The single source of truth is the per-paper-subdir audit log
(`paper/.citation-audit.md`). Self-attestations in BibTeX header
comments or agent transcripts are ignored.

The non-citation factual claims (numbers from the analysis pipeline,
institutional facts about villas / agencies / CABA, dates) are tracked
in a complementary `.fact-audit.md` sidecar — see
[`fact-audit-log.md`](fact-audit-log.md). DRIFT / STALE verdicts on
those facts are treated as MAJOR by default and surfaced in the audit
report; the user decides whether they rise to CRITICAL on a case-by-case
basis (a number that propagates to the abstract is more load-bearing
than one in a footnote).
