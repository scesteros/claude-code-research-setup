---
paths:
  - "paper/**/*.tex"
  - "paper/**/*.bib"
  - "presentation/**/*.tex"
---

# Citation Audit Log

Each paper subdirectory in this repo maintains a sidecar Markdown file
`.citation-audit.md` (e.g., `paper/.citation-audit.md`) that records
the bibliographic + substantive verification status of every citation
in the paper's prose. The file is maintained by the
[`verify-citations`](../skills/verify-citations/SKILL.md) skill, the
[`citation-verifier`](../agents/citation-verifier.md) agent, and the
[`/audit-citations`](../skills/audit-citations/SKILL.md) command. It
is the authoritative record of what has been checked and what is
still pending.

> **Status note (this project):** the citation toolkit ships dormant.
> This file documents the schema and lifecycle that will apply once a
> paper draft begins. No `.citation-audit.md` exists yet because no
> paper `.tex` exists yet.

## Why a sidecar log

- Avoids polluting `.tex` files with verification comments.
- Persists verification state across sessions, so a citation already
  verified is not re-checked unnecessarily.
- Lets the user audit at a glance: how many citations are still
  pending PDFs, how many are MISMATCHES not yet resolved, etc.
- Survives `git` history alongside the document.
- Is the single source of truth that the QA loop reads (not BibTeX
  header comments or agent self-attestations).

## File location

One log per paper subdirectory. Examples:

```
paper/.citation-audit.md
presentation/.citation-audit.md   # if the slide deck cites different papers
```

The leading dot makes it a hidden file, but it **is committed to the
repo** (do not add it to `.gitignore`).

## Schema (10 columns)

Markdown with a single table. Header must match exactly so parsers
and diffs remain stable:

```markdown
# Citation Audit Log — <document name>

Last updated: <YYYY-MM-DD>

| bibkey | location | claim_fingerprint | bib_check | substantive_check | failure_mode | version_read | evidence | last_checked | overridden_by_user |
|---|---|---|---|---|---|---|---|---|---|
```

### Column definitions

| Column | Meaning |
|---|---|
| `bibkey` | The BibTeX key as it appears in `references.bib` and in `\cite*{}` calls. |
| `location` | `file:line` where the citation appears, e.g. `paper/sections/02_motivation.tex:43`. One row per `(bibkey, location)` pair — the same bibkey cited in three sentences is three rows. |
| `claim_fingerprint` | Short paraphrase (≤ 20 words) of the specific assertion the citation supports. Used to detect whether the claim has materially changed since last verification. |
| `bib_check` | Layer 1 verdict on bibliographic correctness: `BIB_OK`, `BIB_FAIL`, or `BIB_NO_DOI`. `BIB_OK` means the author list, year, title, and journal in `references.bib` all match the API record at the cited DOI. `BIB_FAIL` means at least one of these fields disagrees. `BIB_NO_DOI` means the bib has no DOI, so the API match cannot be confirmed. |
| `substantive_check` | Layer 2 verdict: `VALID` / `MISMATCH` / `AMBIGUOUS` / `INACCESSIBLE`. |
| `failure_mode` | For `MISMATCH` / `AMBIGUOUS`, one of the substantive codes (`topic_adjacent_only`, `direction_mismatch`, `magnitude_mismatch`, `causal_vs_correlational`, `population_or_setting_mismatch`, `time_period_mismatch`, `out_of_scope_inference`, `mis_attribution`, `review_used_for_specific_finding`). For `BIB_FAIL`, one of `wrong_authors`, `wrong_year`, `wrong_title`, `wrong_journal`. Empty for `BIB_OK + VALID` and for `INACCESSIBLE`. |
| `version_read` | `published`, `working_paper:<series>:<year>` (e.g. `working_paper:NBER:2014`), `openalex_metadata_only`, or `none`. `openalex_metadata_only` means the API record was checked for the bibliographic match but the paper body was not read (acceptable for purely-methodological cites in passing — but the substantive check then defaults to `INACCESSIBLE`). |
| `evidence` | For `VALID`: section / table / page reference inside the paper. For `MISMATCH` / `AMBIGUOUS`: one-sentence factual summary of what the paper actually shows on the relevant point. For `INACCESSIBLE`: where it was searched and why it could not be obtained. For `BIB_FAIL`: which fields disagreed and what the API record said. Keep to one line; longer notes go in the chat or agent transcript. |
| `last_checked` | ISO date `YYYY-MM-DD`. |
| `overridden_by_user` | If the user explicitly overrode a `MISMATCH` / `AMBIGUOUS` / `BIB_FAIL` verdict (kept the citation as-is), record their one-line rationale. Empty otherwise. |

### Example rows (crime-econometrics flavor)

```markdown
| Martin2022force | paper/sections/02_lit_review.tex:48 | mechanism for police force size effects partly via response time | BIB_OK | AMBIGUOUS | out_of_scope_inference | published | Paper estimates force-size effects on race-specific arrests; response-time mediation is not directly identified. | 2026-05-13 |  |
| Smith2020intervention | paper/sections/02_lit_review.tex:64 | enforcement crackdowns raised local outcomes | BIB_OK | VALID |  | published | Table 3 col (2): +27% outcome increase in treated municipalities over the sample window (close-elections RDD). | 2026-05-13 |  |
| Brown2010framework | paper/sections/03_mechanism.tex:88 | the intervention reduces systemic effects by disrupting actor hierarchies | BIB_OK | MISMATCH | review_used_for_specific_finding | published | Paper defines the three-channel framework. Does not establish that the intervention reduces the systemic effect; that is downstream policy inference. | 2026-05-13 |  |
| Williams2017response | paper/sections/02_lit_review.tex:51 | response-time elasticity of clearance, regional police force | BIB_FAIL | INACCESSIBLE | wrong_authors |  | OpenAlex record at the cited DOI lists Williams & Davis, not Williams alone. Author list in references.bib missing co-author. Rewrote as WilliamsDavis2018response. | 2026-05-13 |  |
| MartinRoberts2018 | paper/sections/02_lit_review.tex:120 | police-on-crime elasticity ≈ -0.3 | BIB_OK | AMBIGUOUS | review_used_for_specific_finding | published | Paper is a survey; the -0.3 figure summarizes prior primary studies. Cite the primary papers for the specific magnitude. | 2026-05-13 | User: keep as additional cite alongside primary papers; clarify it is a survey. |
```

## Lifecycle

### Pre-draft phase (today in this project)

The citation toolkit ships dormant. No `.citation-audit.md` exists.
The schema documented above will activate when a paper draft begins.

### When a paper draft starts (writing the first cite)

For every `\cite*{key}` the writer adds to prose, they (or the
session's agent) must:

1. **Verify Layer 1** (bibliographic) via OpenAlex DOI lookup. Append
   a row with `bib_check = BIB_OK`, `BIB_FAIL`, or `BIB_NO_DOI`.
2. **Run the `verify-citations` skill** on the cite, which delegates
   to the `citation-verifier` agent for substantive checking. Append
   (or update in place) the row with `substantive_check = VALID /
   MISMATCH / AMBIGUOUS / INACCESSIBLE`.

If `BIB_FAIL` or `MISMATCH` is produced, fix the issue before
writing the next sentence — drop the cite, replace with the correct
paper, or soften the claim.

### Re-encountering a cite later in the session

If the same `(bibkey, location)` pair is encountered again, compare
the current sentence's claim to `claim_fingerprint`. If the
population, outcome, direction, magnitude, evidence type, or scope
have changed, the claim has changed and the citation must be
**re-verified** — do not reuse the prior verdict. The new verdict
replaces the old row.

### Batch audit via `/audit-citations`

When the user runs `/audit-citations <paper-subdir>`, the skill scans
every `.tex` for `\cite*{}` calls, verifies them against the audit
log, queues any unlogged or stale rows for the `citation-verifier`
agent, runs the parallel agents, and writes the consolidated rows
back in a single Write call (orchestrator-writes pattern). The
agents themselves do NOT write to the log.

The consolidated report breakdown:

```
Citation audit — paper/

Total citations: N
  BIB_OK + VALID:        a
  BIB_FAIL:              b
  Substantive MISMATCH:  c
  Substantive AMBIGUOUS: d
  Substantive INACCESSIBLE: e
  BIB_NO_DOI:            f
  Overridden:            g
```

If `b + c > 0`, the user is asked to fix before the draft is
considered ship-ready. No mandatory orchestrator gate enforces this
in this project — it's a user-invoked check.

### Inside `paper-reviewer` or `proofreader`

When the paper draft is reviewed by `paper-reviewer` (or any of the
existing review agents in `.claude/agents/`), the reviewer reads the
audit log alongside the prose. Any `BIB_FAIL` or `MISMATCH` in the
log becomes a CRITICAL issue in the review report, regardless of
whether the `.tex` itself compiles cleanly.

## Workflow rules

1. **One row per `(bibkey, location)` pair.** Same bibkey in three
   sentences → three rows.
2. **Update, do not duplicate.** When re-verifying a row, replace it
   rather than appending a second row for the same pair.
3. **Update `Last updated` at the top** whenever rows are added or
   changed.
4. **Never delete rows for unresolved BIB_FAIL / MISMATCH / AMBIGUOUS
   / INACCESSIBLE** without resolving the underlying issue. A removed
   citation means deleting the row is fine; a still-present cite with
   an unresolved verdict must remain in the log until resolved.
5. **The log is not a substitute for chat reporting.** Critical
   verdicts must still be surfaced in the agent's transcript at the
   moment they are detected.
6. **The log is the source of truth.** Self-attestations in bib
   headers or transcripts are ignored; only the audit log counts.
7. **The orchestrator (skill) is the sole writer.** Verifier agents
   return `AUDIT_LOG_ROW` blocks; the `verify-citations` /
   `audit-citations` skill serializes the writes.

## Detecting "claim has changed"

When re-encountering a `(bibkey, location)` already in the log,
compare the current sentence's claim to `claim_fingerprint`. If the
population, outcome, direction, magnitude, evidence type, or scope
have changed, the citation must be re-verified — do not reuse the
prior verdict. The new verdict replaces the old row.

## Reading order for citation-aware agents

When `verify-citations` or `audit-citations` starts work on a paper
subdirectory, it should:

1. Open `.citation-audit.md` first (if it exists).
2. Identify which `(bibkey, location)` pairs in the current `.tex`
   files are already logged and whether their claims have changed.
3. Verify only the new or changed pairs (delegate each to
   `citation-verifier`).
4. Update the log atomically at the end of the run.

## Severity in QA

See [`citation-integrity.md`](citation-integrity.md) and
[`quality-gates.md`](quality-gates.md) §"Citation integrity gate"
for the exact mapping from this log's verdicts to QA severity
(BIB_FAIL / MISMATCH → CRITICAL; AMBIGUOUS / INACCESSIBLE / BIB_NO_DOI
→ MAJOR; VALID → none).
