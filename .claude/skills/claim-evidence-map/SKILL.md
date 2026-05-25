---
name: claim-evidence-map
description: User-invoked construction of a Claim | Evidence | Status table for a manuscript or section. Trigger only when the user runs `/claim-evidence-map` or explicitly asks to map claims to evidence — e.g., "build a claim-evidence map for the abstract", "list each claim with its evidence", "show me what's supported and what's not". Do NOT auto-trigger from `.tex` edits or from passive matching. Extracts each substantive assertion, locates the supporting evidence (own results, cited literature, institutional fact, or none), and flags claims that are unsupported, weakly hedged, or over-hedged.
argument-hint: "[file path or section keyword; optional 'focus:abstract|intro|conclusion']"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# Claim–Evidence Map

**Repo context:** an empirical-economics analysis repository. The paper draft (when it begins) will live or die on whether the strength of each claim matches the strength of the evidence behind it. This skill makes that mapping explicit so the user can see at a glance where causal language is unsupported, where a result is over-hedged, or where a citation is missing.

> **Status note:** the citation toolkit ships dormant in this project. Invoke this skill manually with `/claim-evidence-map <paper-section>` once a paper draft exists.

---

## Setup

1. **Resolve the target** (file path or keyword glob; if multiple matches, ask).
2. **Parse `focus:` flag** if present. Default: scan the full document but emphasize Abstract, Introduction, and Conclusion (where claims are most concentrated).
3. **Identify the document's identification strategy.** For this project, the paper claims causal identification via staggered DiD / event-study designs on intervention events. Causal language is appropriate **only** for claims that map to one of those estimators; descriptive language is required for everything else.

---

## What counts as a "claim"

Any sentence that asserts:

- A causal effect ("the intervention reduces the outcome in treated neighborhoods by Z%").
- A correlation or association ("units with more events show higher police presence overall").
- A descriptive fact about the data, institution, or world ("the study city has 10 officially designated treated areas as of 2024").
- A statement about prior literature ("Smith (2020) finds ...").
- A mechanism or interpretation ("This is consistent with a supply-disruption channel à la Brown (2010)").

Skip: section headings, table/figure captions, equation definitions, transitional sentences ("In this section we...").

---

## Evidence categories

| Category | What it means | Example source for this project |
|---|---|---|
| **Own result (DiD)** | Supported by a number/figure/table in the manuscript that comes from this repo's analysis pipeline. | Coefficient row in `output/tables/main_did_daily.csv`; event-study figure in `output/figures/`. |
| **Cited literature** | Supported by a formal `\citep{}` to a paper in `references.bib`. | Martin & Roberts 2018 cited for the police-on-crime survey. |
| **Institutional fact** | Supported by official source, statute, or administrative documentation (cite). | City decree formalizing treated-area boundaries; partner-agency annual report. |
| **Pipeline-derived descriptive** | Number computed from the scraped/cleaned panel but not from a regression. | "Across 2016–2024, the scraper identified ~50 intervention events" (from `<pipeline-output-path>/`). |
| **Assumption** | Stated as a modeling / identifying assumption; explicit, not asserted as fact. | "We assume parallel trends conditional on neighborhood fixed effects." |
| **None** | No evidence located in the manuscript or its references. | — |

---

## Status rubric

| Status | When to assign |
|---|---|
| **OK** | Evidence matches claim strength: causal language with a DiD/event-study result; descriptive language with a tabulation; institutional claims with an official source citation. |
| **Over-claim** | Causal/strong language but evidence is associational, descriptive, or missing. **Flag for revision.** Especially common in this project: framing a robustness coefficient as the headline causal estimate, or making a generalization beyond the study setting without a transportability discussion. |
| **Under-claim** | Hedged language but evidence is strong (DiD with all robustness checks passing, multiple specifications agreeing). Hedge can be loosened. |
| **Unsupported** | No evidence located. Either add a citation, run a check, or remove the claim. |
| **Stale** | Cited source / pipeline output exists but reports a different number or finding than the manuscript states. (E.g., paper says "11.8%" but `main_did_daily.csv` now reports 9.6% after the most recent re-run.) |

---

## Output Format

Write to `quality_reports/claim_evidence_map_[name].md`:

```markdown
# Claim–Evidence Map: [document path]

**Identification regime claimed:** [causal (staggered DiD) / event-study / descriptive / mixed]
**Required hedge tier:** [strong / moderate / weak per section]

## Map

| # | Section | Claim (verbatim, short) | Evidence | Status | Note |
|---|---------|------------------------|----------|--------|------|
| 1 | Intro ¶2 | "The intervention reduces the daily outcome by 11.8%."   | output/tables/main_did_daily.csv (treated row, col 2) | OK | — |
| 2 | Abstract | "The intervention causes large reductions in the outcome." | None located in the manuscript | Over-claim | Hedge to "is associated with reductions" or cite the main DiD table directly. |
| 3 | Intro ¶4 | "The intervention may also displace the outcome to neighboring units." | None | Unsupported | Either run the spillover spec or drop. |
| 4 | §5 ¶1 | "Brown (2010) channel explains the heterogeneity." | Brown2010framework cite | Stale or Over-claim? | Verify via /audit-citations — Brown 2010 defines the channel concept; does not establish the heterogeneity. |

## Summary
- **Over-claims:** [count, list]
- **Unsupported:** [count, list]
- **Stale:** [count, list]
- **Under-claims:** [count, list — usually fewer, but worth surfacing]

## Priority fixes (top 5)
1. [Section / paragraph — what to change]
2. ...
```

---

## Principles

- **The Abstract and Introduction are the hottest zones.** Claims there cascade through the paper; check them first.
- **Hedge to match design strength.** "The intervention reduces X" requires the DiD result. "The intervention is associated with X" requires only a tabulation. Use the appropriate verb tier.
- **Causal claims about the intervention require the DiD output row, not just the existence of `4_Analysis_Standard_DiD_Daily.do`.** Cite the table / figure number explicitly.
- **Institutional-fact claims about treated areas, districts, or partner agencies require a government source document or an officially published map / decree.** Do not assert "the city has X treated areas" without an official source.
- **Verify numbers verbatim.** If the Abstract says "12%" and `output/tables/main_did_daily.csv` says "-0.118 log points", that is a Stale flag, not OK — the units don't match and the precision differs.
- **Do not rewrite the manuscript** in this skill. Output is a diagnostic table.
- **If `references.bib` is missing or cited keys are absent**, mark them and do not fabricate citations.

---

## When to use a different tool

- Need adversarial design critique → `/devils-advocate`.
- Need full prose-and-substance review → `/review-paper`.
- Need formal-cite verification → `/audit-citations`.
- Need prose-vs-pipeline-output check → `/source-audit <paper> <CSV or .log>`.
- Need paper-vs-slide consistency check → `/cross-doc-audit paper+slides`.

This skill is narrower: it builds one map of every claim and where its evidence lives.
