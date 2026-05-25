---
name: cross-doc-audit
description: User-invoked audit of substantive consistency across two or more related documents (e.g., paper + slides, paper + table captions, paper + Stata-output CSV). Trigger only when the user runs `/cross-doc-audit` or explicitly asks to compare/cross-check two or more documents — e.g., "check that the slides match the paper", "compare the abstract with the research plan", "audit consistency between paper and presentation". Do NOT auto-trigger from edits to either document or from passive matching. Detects numerical mismatches, terminology drift, framing divergence, structural conflicts, and asymmetric inclusion. Different from /deep-audit (which checks structural infrastructure — paths, refs, conventions) and from /source-audit (single source).
argument-hint: "[doc1] [doc2] ([doc3] ...) or 'paper+slides' shorthand"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Agent"]
---

# /cross-doc-audit

Audit substantive consistency across two or more related documents.

## When to use

- Several documents in the repo share substantive content (paper draft + slide deck; paper + table captions; meeting notes + paper draft; paper + Stata-output CSV).
- After a sequence of edits that touched only one of those documents, when changes should propagate.
- Before submission or sharing, to confirm cross-document alignment.
- When the user invokes `/cross-doc-audit` explicitly or asks to "check that paper and slides agree", "verify the captions match the paper", "see if the numbers in the slides match the pipeline".

This skill is distinct from:

- `/deep-audit` — checks **structural** consistency (file paths, figure refs, citation keys, convention violations). `/cross-doc-audit` checks **factual / terminological / framing** consistency between documents.
- `/source-audit` — checks prose in a target document against a single **source** document (one-direction, derivation-focused). `/cross-doc-audit` checks consistency between **peers** that share content (bidirectional).
- `/audit-citations` — checks formal `\citep{}` pairs. `/cross-doc-audit` checks substantive content claims regardless of citation status.

## Inputs

- **Target documents**: a list of file paths to compare. Two or more. Common pairings in this project:
  - `paper/paper.tex` + `presentation/main.tex` (paper draft ↔ slide deck)
  - `paper/paper.tex` + `paper/tables/*.tex` (paper body ↔ table captions / `\caption{}` text)
  - `paper/paper.tex` + `output/tables/main_did_daily.csv` (paper body ↔ Stata-output CSV)
  - `paper/paper.tex` + `meetings/<date>_summary.md` (paper draft ↔ meeting notes)
  - `presentation/main.tex` + `output/tables/*.csv` (slides ↔ pipeline output)
- Optional shorthand: `paper+slides` resolves to `paper/paper.tex` + `presentation/main.tex` if those exist.
- Optional **focus**: a specific dimension to check (e.g., "just numerical facts", "just terminology", "just authorship", "just the main coefficient").

If only one document is provided, ask the user to specify the other(s).

## What to check

Group substantive claims into these dimensions:

1. **Numerical facts** — point estimates, standard errors, sample sizes, percentages, dates, magnitudes, counts.
2. **Named entities** — paper citations, organizations (the federal police, the city police, the partner agency), locations (neighborhoods, districts, treated areas), co-authors, dataset names.
3. **Terminology** — technical terms and framings ("intervention event" vs. "operation"; "treated unit" vs. "intervention site"; "stacked DiD" vs. "Cengiz et al. estimator").
4. **Structural claims** — descriptions of study design, identification, outcomes, event window, clustering, treatment definition.
5. **Authorship and attribution** — who authored what, who is co-author on which project, who is supervisor.
6. **Asymmetric inclusion** — a substantive fact mentioned in one document but conspicuously absent from the corresponding section in another.

## Procedure

### 1. Read each target document

Use Read on each `.tex` / `.md` / `.csv` / `.pdf` file. For long documents, scan once for structure and then return for specific section reads. For CSVs, read the header row and any unit / specification notes.

### 2. Extract substantive claims with location pointers

For each document, enumerate substantive claims along the six dimensions above. Record:
- The claim text (verbatim or near-verbatim).
- The document and approximate line / row number.
- The dimension category.

This is most efficient when the user has named a focus dimension; otherwise enumerate all six.

### 3. Cluster equivalent claims across documents

Claims that refer to the same underlying fact are clustered together, regardless of phrasing. E.g.:

- "Outcome falls by 11.8% post-intervention" (paper) and "$-0.118$ log points" (CSV cell `main_did_daily.csv` row `treated`) and "−12% effect on outcome" (slide) → same cluster. Three rounding precisions and two unit framings — flag for alignment.
- "Treatment defined as any intervention event in neighborhood in 30-day window" (paper §3.1) and "30-day post-event treatment indicator" (slide §Methodology) → same cluster.
- "Clustered at neighborhood level" (paper) and "Clustered at district level" (slide) → same cluster, STRUCTURAL_CONFLICT.

### 4. Issue a verdict per cluster

- **CONSISTENT** — every mention of the same fact agrees across all documents on every dimension that matters. (Phrasing differences allowed; the substance must match.)
- **NUMERICAL_MISMATCH** — same fact, different numbers (or different precision, different units).
- **TERMINOLOGY_DRIFT** — same concept, different terms used inconsistently across documents (e.g., one doc updated, the other not).
- **FRAMING_DIVERGENCE** — same fact, framed at different scopes or precision. May be intentional or accidental.
- **STRUCTURAL_CONFLICT** — same design feature described differently in two documents (e.g., one says clustering at neighborhood level, another says district level).
- **MISSING_FROM_DOC** — a substantive fact present in one document is conspicuously absent from the parallel section of another, where the user might expect it to appear.

### 5. Delegate per-cluster verification to the agent when warranted

For complex or ambiguous clusters (e.g., a numerical fact mentioned across three documents with slight variations, or a coefficient cluster spanning paper + slides + multiple CSV columns), delegate to the `cross-doc-checker` agent in fresh context. One agent invocation per cluster keeps verification isolated and rigorous.

### 6. Produce the report

Present the audit inline:

```
Cross-doc audit — <doc1> vs <doc2> [vs <doc3> ...]

Claim clusters audited: N
  CONSISTENT:                 n
  NUMERICAL_MISMATCH:         n
  TERMINOLOGY_DRIFT:          n
  FRAMING_DIVERGENCE:         n
  STRUCTURAL_CONFLICT:        n
  MISSING_FROM_DOC:           n

── NUMERICAL_MISMATCH ──
1. Main DiD coefficient on the daily outcome:
   - paper/paper.tex:204: "outcome falls by 11.8% (SE 3.1)"
   - presentation/main.tex:88: "−12% effect (SE 3.1)"
   - output/tables/main_did_daily.csv:row=treated: "-0.1184, SE 0.0312"
   Issue: paper rounds to 11.8%; slide rounds to 12%; CSV is in log points (-0.118).
   Suggested fix: align rounding; clarify units (log points ≈ percent for small effects).

── TERMINOLOGY_DRIFT ──
2. ...

── FRAMING_DIVERGENCE ──
3. ...

── STRUCTURAL_CONFLICT ──
4. ...

── MISSING_FROM_DOC ──
5. ...

── CONSISTENT (summary only) ──
n_consistent clusters confirmed.
```

### 7. Wait for user direction

For each non-CONSISTENT cluster, the user decides: align to one version, accept the divergence as intentional, or further investigate. Do not modify any `.tex` automatically.

## Posture

- **Conservative.** Flag in doubt. Some divergences are intentional (different framings for different audiences); the user makes that call.
- **Specific.** Quote the exact text and location in each document.
- **No silent rewriting.** All alignments require user direction.
- **Tolerate stylistic divergence.** A paper and a slide describe the same fact at different verbosity; that is not a mismatch. Only flag when substance, precision, or framing genuinely differ.
- **Stata-output CSVs are authoritative for numbers.** If paper says "12%" and CSV says "-0.1184", the CSV wins. The prose must align to the pipeline, not the other way around.
- **Follow** `.claude/rules/claim-discipline.md` **and** `.claude/rules/paraphrase-discipline.md` as the substantive standards.

## Common pairings and what to watch for

| Pair | Watch for |
|---|---|
| Paper draft + slide deck | Numerical drift on main effects, terminology drift after one document is updated, missing first-stage results on slides, hedge consistency |
| Paper body + table captions | Caption text restating a coefficient differently from the body; "treated" vs. "intervention" inconsistency |
| Paper draft + Stata-output CSV | Sign / unit / magnitude drift; specification mismatch (daily vs. monthly); the prose must align to the CSV, not vice versa |
| Paper + meeting notes | Old framings carried over; coefficient quoted in a meeting before a later re-run was incorporated |
| Slide deck + table captions | Reformatted table that drops standard errors; abbreviated terminology on slide that disagrees with the caption |

## Related

- `/source-audit` — for prose derived from a single source document (one-direction).
- `/audit-citations` — for formal `\citep{}` entries against the cited papers.
- `/deep-audit` — for structural / infrastructure consistency.
- `cross-doc-checker` agent — per-cluster fresh-context verifier.
- `.claude/rules/claim-discipline.md` — overarching claim posture.
- `.claude/rules/paraphrase-discipline.md` — when one document paraphrases another.
