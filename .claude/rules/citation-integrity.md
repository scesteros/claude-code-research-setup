---
paths:
  - "paper/**/*.tex"
  - "paper/**/*.bib"
  - "presentation/**/*.tex"
---

# Citation Integrity — Zero-Tolerance Policy

**Status:** policy doc. Applies to every agent and skill in this repo
that produces citations or BibTeX entries — currently none, because
this project is a Stata/Python analysis repo with no narrative draft. The
toolkit ships **dormant**: skills (`verify-citations`, `audit-citations`,
`source-audit`, `cross-doc-audit`, `claim-evidence-map`) and agents
(`citation-verifier`, `citation-adversary`, `source-fact-checker`,
`cross-doc-checker`) are installed and ready to be invoked manually
once a paper draft begins.

**Forward-looking:** enforced once the paper draft begins (likely under
`paper/`); today the toolkit ships dormant. There is no mandatory
orchestrator gate triggering citation audits, because this project has no
citation pipeline. The user invokes `/audit-citations <paper-subdir>`
manually when needed.

**Code-side analog:** [`verification-protocol.md`](verification-protocol.md)
covers Stata/Python output verification (the code-execution-side
discipline). This document covers citation/prose-side discipline. The
two are parallel and complementary — `verification-protocol.md`
ensures the pipeline numbers are real; `citation-integrity.md` ensures
the prose around them is honest.

---

## The three layers of citation integrity

Every citation that appears in any `.tex` file inside the paper
subdirectory (e.g., `paper/paper.tex`, `paper/sections/*.tex`) or the
slide deck (`presentation/`) must pass **all three** of the following
checks before being considered shippable:

### Layer 1 — Bibliographic correctness

The BibTeX entry's author list, year, title, journal, and DOI must
match an authoritative record returned by **OpenAlex**, **Crossref**,
**Semantic Scholar**, or **arXiv** for the cited DOI.

- **Author list** is the single most-fabricated field. It must be
  copied verbatim from the API response, not typed from memory.
- A cite key like `Martin2022force` does **not** imply the
  authors are Martin et al.; the cite key is just a label. Always
  re-derive authors from the API.
- A real title attached to invented authors is **worse** than a fully
  invented paper, because it is more plausible to a casual reader.

### Layer 2 — Substantive adequacy

The cited paper's findings, evidence, or argument must directly
support the specific assertion the citation accompanies. Topic
adjacency is not enough. Failure modes include:

| Failure mode | Example |
|---|---|
| `topic_adjacent_only` | Cite a paper on response-time elasticities in one setting for a claim about a different intervention's effects on a different outcome in a different setting. Both "policing + crime" but different intervention, sample, country, and mechanism. |
| `direction_mismatch` | Prose says enforcement crackdowns reduce violence; paper finds the opposite (e.g., a well-known crackdown study showing violence rising in treated municipalities). |
| `magnitude_mismatch` | Prose says "large reduction"; paper estimates a 1pp effect that the authors themselves frame as modest. |
| `causal_vs_correlational` | Prose says the intervention reduces the outcome; paper reports a city-year correlation without identification. |
| `population_or_setting_mismatch` | Claim is about urban treated neighborhoods; paper studies rural agricultural producers. |
| `time_period_mismatch` | Claim is about post-2018 in the study city; paper's data ends in 2005. |
| `out_of_scope_inference` | Claim extrapolates beyond what the paper warrants (e.g., using a foundational theoretical framework as evidence for a specific outcome reduction). |
| `mis_attribution` | The finding exists in the literature but is from a different paper than the one cited. |
| `review_used_for_specific_finding` | A well-known survey cited for a specific elasticity it summarizes but does not itself establish. Cite the primary paper. |

### Layer 3 — Internal consistency

Across `paper/`, `presentation/`, and any other `.tex` files that
share citations, the same `(cite key, authors, year, DOI)` tuple must
be used consistently. The same paper must not appear under two
different keys; the same key must not point to two different papers.

---

## Rules for any agent (or human) that produces a citation

### 1. No fabrication, ever

Never invent any of:
- An author name.
- A year, journal, volume, issue, page range, or DOI.
- A paper's findings, magnitudes, or design (sample, identification, time period).
- A "gap in the literature" — claims of absence ("no study has examined") must be hedged unless an exhaustive search confirms them.

If a fact cannot be traced to a primary source, **do not write it**.
Drop the citation, soften the prose, or surface the gap to the user.

### 2. Write the bib first, prose second

Before adding `\citep{key}` or `\citet{key}` to prose:

1. Resolve the DOI in OpenAlex (preferred) or Crossref via the
   OpenAlex MCP / paper-search-mcp / Serper MCP tools.
2. Transcribe the author list, year, title, journal, volume, pages
   **verbatim from the API response** into `references.bib`.
3. Cross-check the cite key against the first author's surname + year
   in the API response. If the cite key uses a different surname,
   either change the key or remove the entry.
4. Only **after** the bib entry is in place and matches the API, add
   the `\cite*{}` call to the prose.

### 3. Self-attestation is not a substitute for verification

A bib header that says "All entries verified through OpenAlex" carries
zero weight unless the verification actually happened. The trustworthy
attestation is the audit log (`paper/.citation-audit.md`), not the
comment line.

### 4. Substantive adequacy is checked separately

Bibliographic correctness (Layer 1) is necessary but not sufficient.
Even after the bib matches OpenAlex, the cite must substantively
support the *specific* claim in the sentence. This is the job of the
[`verify-citations`](../skills/verify-citations/SKILL.md) skill, which
delegates to the [`citation-verifier`](../agents/citation-verifier.md)
agent for fresh-context paper reading. Any agent or human that adds a
citation to prose in this repo's paper draft should invoke
`verify-citations` before considering the sentence final.

### 5. Hedge novelty claims

Any assertion of absence ("first causal evidence", "no prior study",
"undocumented") must be either backed by an explicit, defensible
search and stated plainly, or softened with hedging language ("to the
best of our knowledge", "we are not aware of", "while existing
evidence remains limited"). Default to the hedged form. See
[`.claude/rules/claim-discipline.md`](claim-discipline.md) §2 and the
two-pass novelty protocol.

### 6. Honest cite-bib relationships

- One cite key → exactly one paper, consistently across all `.tex`
  files in the paper draft.
- If two papers have the same first author and year, distinguish keys
  (`Garcia2005a`, `Garcia2005b`) rather than collapsing.
- The same paper must not appear under different keys.

---

## The audit log

Once a paper draft exists, its subdirectory maintains a sidecar log
`.citation-audit.md` (e.g., `paper/.citation-audit.md`). Schema and
update rules in
[`.claude/rules/citation-audit-log.md`](citation-audit-log.md). The
log uses a **10-column schema** with `bib_check` and `substantive_check`
as separate verdict columns.

When `/audit-citations` is run manually, the consolidated report
reads this log as the single source of truth.

---

## Tooling

| Tool | Layer | Use |
|---|---|---|
| **OpenAlex MCP** | Layer 1 | DOI lookup → author list verification. Free. |
| **paper-search-mcp** | Layer 1 / 2 | Multi-source (arXiv, Semantic Scholar, Crossref, RePEc, PubMed, …). Free. |
| **Serper MCP** (`google_search_scholar`) | Layer 1 / 2 | Escalation for hard-to-find papers. |
| [`verify-citations`](../skills/verify-citations/SKILL.md) skill | Layers 1+2 | User-invoked per-cite verification. Run on request when a cite is added, moved, or contested. Does NOT auto-trigger on `.tex` edits. |
| [`audit-citations`](../skills/audit-citations/SKILL.md) skill | Layers 1+2+3 | User-invoked batch audit of a paper subdirectory. Run via `/audit-citations`. |
| [`citation-verifier`](../agents/citation-verifier.md) agent | Layers 1+2 | Fresh-context per-citation worker. |
| [`citation-adversary`](../agents/citation-adversary.md) agent | Layer 2 | Adversarial second-opinion (only when `--adversarial`). |

Use of these tools, once a paper draft exists, is **not optional** for
citations in that draft.

---

## Severity in QA

When a paper draft is being reviewed by `paper-reviewer` or
`proofreader`, citation verdicts from `audit-citations` map to QA
severity as follows (full table in
[`.claude/rules/quality-gates.md`](quality-gates.md), §"Citation
integrity gate"):

| Verdict | Severity |
|---|---|
| `BIB_FAIL` (Layer 1 — author/year/title does not match the API record at the cited DOI) | **CRITICAL**. Block commit until rewritten. |
| `MISMATCH` (Layer 2 — paper is real but does not support the claim) | **CRITICAL**. Block commit until prose or cite is changed. |
| `AMBIGUOUS` (Layer 2 — paper partially supports the claim) | **MAJOR**. Surfaced in QA report; user decides whether to refix or accept. |
| `INACCESSIBLE` (paper cannot be obtained for substantive check) | **MAJOR**. Logged; the entry may ship with the row marked `INACCESSIBLE` in the audit log, but flagged in the final summary. |
| `BIB_NO_DOI` (bib has no DOI, so API match cannot be confirmed) | **MAJOR**. Warning. User asked to add a DOI if possible. |
| `VALID` (`BIB_OK + VALID`) | None. |

The single source of truth is `paper/.citation-audit.md`.
Self-attestations in BibTeX header comments or agent transcripts are
ignored.

---

## Related rules and skills

- [`.claude/rules/claim-discipline.md`](claim-discipline.md) —
  posture for claim writing across the paper draft.
- [`.claude/rules/citation-audit-log.md`](citation-audit-log.md) —
  10-column audit log schema and lifecycle.
- [`.claude/rules/fact-audit-log.md`](fact-audit-log.md) —
  companion log for non-citation factual claims (numbers, dates,
  institutional facts) — the most immediately useful piece for
  this project while the citation toolkit is dormant.
- [`.claude/rules/paraphrase-discipline.md`](paraphrase-discipline.md)
  — paraphrase-specific standards.
- [`.claude/rules/prose-clarity.md`](prose-clarity.md) — paragraph-level
  clarity discipline.
- [`.claude/rules/quality-gates.md`](quality-gates.md) — full severity
  ladder including citation severity table.
- [`.claude/rules/verification-protocol.md`](verification-protocol.md)
  — code-side verification (Stata/Python). Parallel discipline; not
  a substitute.

---

## Why this rule exists

A paper draft that asserts causal effects in a specific empirical
setting only has value if the literature citations are trustworthy.
Most applied-econ subliteratures have well-known cite hazards: a few
canonical / foundational papers get reflexively cited for
mechanism-specific claims they do not actually make. The dormant
toolkit installed here is the structural defense; when the paper
draft begins, invoking `/audit-citations paper/` produces a
consolidated report that catches the failure modes above.
