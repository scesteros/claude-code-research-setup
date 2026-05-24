---
paths:
  - "paper/**/*.tex"
  - "presentation/**/*.tex"
  - "internal_reports/**/*.md"
---

# Claim Discipline

**Repo context:** an empirical-economics analysis repository. On-demand rule set that
codifies the standards for making and defending substantive claims in
prose. Load this when drafting any section of the paper, slide, or
report that asserts a finding, a gap, a novelty claim, or a fact about
literature or institutions. Complements — does not replace — the
writing conventions in `CLAUDE.md` and the paragraph-level discipline
in [`prose-clarity.md`](prose-clarity.md).

> **Status note:** the citation toolkit ships dormant in this project.
> This rule applies once narrative prose (paper or reports) starts to
> assert substantive claims.

---

## The five claim-discipline rules

### 1. No fabrication

Never invent:
- Citations (author, year, title, outlet, page references).
- Empirical findings or magnitudes attributed to a cited paper.
- Gaps in the literature ("no study has examined X").
- Institutional facts (CABA agency jurisdictions, formal villa
  designation criteria, statute provisions, regulatory frameworks,
  partnership terms for any FOIA-type information request).
- Sample sizes, dates, or numerical claims about the pipeline output.
- Coefficient values, standard errors, or N for any regression spec
  in this repo — these come from the Stata `.log` or `output/tables/`
  CSVs, never from memory.

If a claim cannot be traced to a primary source, do not write it.
Find the source, soften the claim, or ask the user.

### 2. Hedge novelty claims

Statements that assert absence or first-status — "no published study",
"this is the first", "X has not been examined" — must be either:

- **Verified exhaustively** (an explicit, defensible literature search)
  and stated plainly; or
- **Softened** with hedging language: "to the best of our knowledge",
  "as far as we know", "while existing evidence remains limited",
  "we are not aware of", "we have not identified".

Default to the softened form unless a thorough search confirms the
stronger claim. See the two-pass novelty protocol below.

### 3. Verify before propagating

Before re-using any number, statistic, sample size, date, institutional
characteristic, or attribution **across documents** (paper → slides →
table caption → meeting note):

- Grep or check the primary source first. For a regression number, the
  primary source is the Stata `.log` or `output/tables/*.csv` of the
  most recent run.
- Do not trust a number simply because it appears in an earlier version
  of the user's own writing — earlier drafts may carry derived figures,
  working-stage estimates, or typos that the primary source contradicts.
- If the primary source contains a different figure or framing, flag
  the discrepancy before resolving it.
- For numbers with multiple plausible referents (e.g., main DiD vs.
  stacked DiD vs. event-study coefficient at horizon 0; full sample vs.
  restricted to villas with ≥1 raid), be explicit about which one is
  being used and where it comes from.

### 4. Follow stated conventions over existing prose

When `CLAUDE.md` or another file in `.claude/rules/` declares a
stylistic or technical convention (English for `.tex`, AER citation
style, table format, etc.), follow it consistently in any new prose.
If the existing prose in the document violates the stated convention,
**flag the inconsistency to the user** — do not silently mimic the
wrong style. The stated convention is the authority; existing prose
may be a drafting error.

### 5. Ask when uncertain

If a substantive claim cannot be sustained from the evidence at hand:

- Flag the uncertainty to the user.
- Propose alternative formulations (softer hedge, drop the claim,
  replace the cite).
- Do not rationalize past the gap.

The cost of pausing to ask is low; the cost of an unsupported claim
that ships is high.

---

## Hedging vocabulary — quick reference

When a novelty or absence claim is appropriate but not exhaustively
verified, prefer the right column:

| Strong (avoid unless verified) | Hedged (default) |
|---|---|
| "No study has examined raid effects on homicide in CABA villas." | "To the best of our knowledge, raid effects on homicide in CABA villas have not been examined." |
| "This is the first causal study of police raids in informal settlements." | "While existing causal evidence on police raids in informal settlements remains limited, this paper provides…" |
| "The literature on narco crackdowns in Argentina is non-existent." | "We are not aware of recent causal evidence on narco crackdowns in Argentina." |
| "The supply-disruption channel is undocumented in our setting." | "We have not identified prior work documenting the supply-disruption channel in our setting." |
| "Buenos Aires is the sharpest case of urban informal-settlement crime in the region." | "Buenos Aires exhibits a pronounced concentration of crime in informal settlements" (drop the comparative unless ranked). |

---

## What this rule is *not*

- Not a substitute for the `verify-citations` skill or `/audit-citations`
  — those operate on specific (citation, claim) pairs. This rule
  operates on writing posture more broadly.
- Not a substitute for `prose-clarity.md`, which handles paragraph-level
  discipline and topic-sentence structure.
- Not a blanket instruction to be cautious about everything. Strong
  claims, when defensible, should be made plainly. The rule is about
  matching the strength of a claim to the strength of the evidence
  behind it. In this project terms: a DiD coefficient that is significant
  at the 1% level and robust to all six specs justifies a strong claim;
  a single specification that is marginally significant requires
  hedging.

---

## Novelty-claim verification protocol (two-pass)

Novelty/absence claims — "no published study", "first causal evidence",
"to our knowledge X has not been examined", "the literature remains
thin" — carry asymmetric risk: a careless strong-form claim that ships
is referee-bait. They require a **two-pass** verification, not the
single pass that suffices for ordinary cites.

### Pass 1 — independent search

Run a structured search scoped to the specific claim, in this order:

1. **OpenAlex MCP** — broad subject + geography filter (e.g.,
   "policing crime informal settlements Latin America 2010–2024").
2. **paper-search-mcp** — multi-source (arXiv, Semantic Scholar,
   Crossref, RePEc, PubMed, others).
3. **Serper MCP** (`google_search_scholar`) for policy reports,
   dissertations, citation-count signals — especially for grey
   literature on Argentine policing.
4. **Manual targeted search by candidate keyword combinations**
   (population × outcome × identification strategy × geography).

The search must be **broad enough to disconfirm the claim** — i.e.,
the search would surface the paper that contradicts the absence, if
one exists. Document the search terms used.

### Pass 2 — independent re-search by a different agent or session

Re-run the same search with **different keyword combinations**,
ideally in a fresh agent context, to reduce the single-point-of-failure
risk that the first search missed a known paper. The agent should be
instructed to "find a paper that would falsify this novelty claim".

### Decision rule

- **Both passes find no falsifying paper** → the strong-form novelty
  claim is defensible. State it plainly.
- **Either pass finds a candidate falsifier** → downgrade to the
  hedged form ("to the best of our knowledge", "we have not
  identified", "while existing evidence remains limited") and cite
  the candidate paper(s) in a sentence that acknowledges them and
  explains how the present work differs.
- **Both passes are inconclusive (broad search but ambiguous
  coverage)** → use the hedged form. Default to caution.

### What counts as a novelty claim (in this project)

Examples of statements that trigger the two-pass protocol:

- "No published causal study estimates the effect of police raids on
  homicides in Buenos Aires villas."
- "This is the first paper to use staggered DiD on narco-raid events
  in Latin American informal settlements."
- "The literature on Argentine drug enforcement is non-existent /
  thin / virtually absent."
- "We are not aware of recent quasi-experimental evaluations of CABA
  police operations."
- "Buenos Aires is the sharpest case of [phenomenon]."

Hedging vocabulary (already in §2 above) is necessary but not
sufficient: hedging plus exhaustive search is the bullet-proof
posture.

### Logging

When a novelty claim is verified, record the search trace in
`<paper-subdir>/.novelty-audit.md` (one row per claim) with: claim
text, location in `.tex`, search resources used, search terms,
candidate falsifiers identified (or "none"), final wording chosen
(strong vs. hedged), and date.

If no `.novelty-audit.md` exists yet, create it with a single-table
schema mirroring `.citation-audit.md`'s structure.

---

## Cluster-citation discipline

When a single claim is supported by `\citep{A, B, C, ...}` (multiple
cites in one parenthesis), apply three additional rules:

### 1. Each cite must independently support the claim

Every bibkey in a cluster cite must, **on its own**, substantiate the
specific claim of the sentence. A cluster is not a place to pad with
"broadly relevant" or "topic-adjacent" papers. If A is direct evidence
and B is conceptual background, they belong in two different sentences
with two different claims.

Failure mode caught by this rule: a 5-cite cluster after a sentence
asserting that police crackdowns *reduce* homicide, where only one
paper actually establishes that (in a specific context) and the other
four are general policing-and-crime references. The four belong in a
separate sentence where the broader association is being stated, with
clear hedging that they are not all on the specific mechanism.

### 2. Cap clusters at three cites

Default maximum: three cites per claim. If the cluster grows to four
or more, the claim is probably compound and should be split into two
sentences. Exceptions exist (a methodological cluster establishing
the DiD literature, a meta-survey reference) but they should be
deliberate, not accidental.

### 3. Label role explicitly when mixing evidence types

When a cluster genuinely mixes types — one empirical anchor + two
conceptual/foundational references — say so in prose:

> Empirically, crackdown-induced violence has been documented in
> Mexican municipalities \citep{dell2015trafficking}. The broader
> theoretical framework for systemic drug-market violence is
> articulated in \citet{goldstein1985tripartite} and
> \citet{lessing2021conceptualizing}.

This is cleaner than `\citep{dell2015trafficking, goldstein1985tripartite,
lessing2021conceptualizing}` because the reader can see which paper
carries the empirical weight and which carries the conceptual
scaffolding. The `.citation-audit.md` log mirrors this distinction in
its `claim_fingerprint` column.

### Practical check before writing a cluster cite

Before writing `\citep{A, B, C}`, fill this internally:

```
claim_fingerprint:   <one sentence ≤20 words>
A_supports_this:     ✓ / ✗  + reason
B_supports_this:     ✓ / ✗  + reason
C_supports_this:     ✓ / ✗  + reason
```

If any cite is `✗`, drop it from the cluster (or move it to its own
sentence with its own claim). This is the cluster-level analogue of
the per-cite pre-write fingerprint in the
[`verify-citations`](../skills/verify-citations/SKILL.md) skill.

---

## Related skills and rules

- [`verify-citations`](../skills/verify-citations/SKILL.md) skill —
  user-invoked substantive verification of a specific citation. Run
  on request when a cite is added, moved, or contested.
- [`/audit-citations`](../skills/audit-citations/SKILL.md) command —
  user-invoked batch verification of every citation in a target file
  or paper subdirectory.
- [`/source-audit`](../skills/source-audit/SKILL.md) skill — audit
  prose claims against a single source document (working paper, Stata
  `.log`, pipeline CSV, `.do` header, government source document).
- [`/cross-doc-audit`](../skills/cross-doc-audit/SKILL.md) skill —
  audit substantive consistency across two or more peer documents
  (paper + slides + table captions + Stata-output CSV).
- [`/claim-evidence-map`](../skills/claim-evidence-map/SKILL.md) skill
  — pre-submission claim×evidence table for a paper section.
- [`.claude/rules/citation-integrity.md`](citation-integrity.md) —
  flagship zero-tolerance policy.
- [`.claude/rules/paraphrase-discipline.md`](paraphrase-discipline.md)
  — paraphrase-specific standards.
- [`.claude/rules/prose-clarity.md`](prose-clarity.md) — paragraph-level
  clarity discipline.
- [`.claude/rules/verification-protocol.md`](verification-protocol.md)
  — code-side verification (Stata/Python). Parallel discipline.
- `CLAUDE.md` — repo-wide writing conventions.
