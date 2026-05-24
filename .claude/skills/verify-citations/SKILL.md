---
name: verify-citations
description: User-invoked substantive verification of a specific citation. Trigger only when the user explicitly asks to verify, vet, or check a citation — e.g., "verify this cite", "does this paper actually say that?", "check the cites in this paragraph", "is `\citep{X}` right here?" — or when the user has asked Claude to add a citation and to verify it before finalizing. Do NOT auto-trigger from `.tex` edits, from `\citep{}` / `\citet{}` presence, or from paper-draft writing in general; citation verification is opt-in. Performs substantive verification (does the cited paper support the specific claim?), not bibliographic checks (author/year/DOI).
argument-hint: "[bibkey or sentence containing the cite]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "WebSearch", "WebFetch", "Agent"]
---

# Verify Citations

**Purpose.** Every time a citation appears in prose, the cited paper must *substantively* support the *specific* claim it accompanies — not merely be topic-adjacent. This skill enforces that.

This skill is **mandatory and non-negotiable** once a paper draft exists in this repo. There is no "I'm pretty sure this paper says that" path. If a citation is added, it gets verified. If verification is not possible, that fact is recorded and surfaced to the user.

> **Status note (this project):** the citation toolkit ships dormant in this repo. Today this project is a Stata/Python analysis repo with no narrative draft. When the paper draft begins (likely in `paper/`), invoke this skill manually per cite. The orchestrator does not auto-trigger it.

---

## Layer 1 / Layer 2 — what this skill checks

The audit log uses a 10-column schema with two explicit verdicts per cite (see [`.claude/rules/citation-audit-log.md`](../../rules/citation-audit-log.md)):

- **Layer 1 — bibliographic correctness (`bib_check`).** Does the `.bib` entry's author list, year, title, and journal match the API record at the cited DOI? Captured in Step 3 of this skill (the BIB-DRIFT check). Verdicts: `BIB_OK` / `BIB_FAIL` / `BIB_NO_DOI`.
- **Layer 2 — substantive adequacy (`substantive_check`).** Does the cited paper's findings, evidence, or argument actually support the specific assertion in the sentence? Captured in Step 5. Verdicts: `VALID` / `MISMATCH` / `AMBIGUOUS` / `INACCESSIBLE`.

A cite is shippable only when Layer 1 = `BIB_OK` (or explicitly-overridden `BIB_NO_DOI`) **and** Layer 2 = `VALID`.

---

## What "substantive verification" means

> *Bibliographic verification* asks: is "Chalfin & McCrary (2017)" the correct author/year/title for bibkey `ChalfinMcCrary2017`?
>
> *Substantive verification* asks: does Chalfin & McCrary (2017) actually report findings that support the specific claim in this sentence?

This skill is about **both** questions, but the second is the load-bearing one and gets the harder check.

A citation is **VALID** only if the cited paper's *findings, evidence, or argument* directly support the *specific* assertion in the sentence — including its population, outcome, direction, magnitude, time period, and causal vs. correlational framing.

A citation is **MISMATCH** if the paper is on the broad topic but does not support the specific claim. Common failure modes:

| Failure mode | Example |
|---|---|
| **Topic-adjacent only** | Sentence: "Police raids reduce homicides in informal settlements." Cite: a paper on response-time elasticities in US cities. The paper is "about policing and crime" but does not study raids, informal settlements, or supply-disruption effects. |
| **Direction mismatch** | Prose claims an increase in violence after a crackdown; paper finds a decrease (or null). |
| **Magnitude mismatch** | Prose says "large reduction"; paper estimates a 2pp effect that the authors themselves frame as modest. |
| **Causal vs. correlational mismatch** | Prose says "raids reduce homicides"; paper reports a city-year correlation without identification. |
| **Population / setting mismatch** | Claim is about Buenos Aires informal settlements; paper studies Rio de Janeiro favelas with a different state-presence regime. Claim is about urban; paper is rural. |
| **Time-period mismatch** | Claim references the post-2018 crackdown era; paper's data ends in 2010. |
| **Out-of-scope inference** | Paper studies displacement of drug markets in setting S; prose extrapolates to a homicide-deterrence mechanism the paper does not test. |
| **Mis-attribution within the literature** | The finding *exists* in the literature, but is from a *different* paper than the one cited. |
| **Review / meta-analysis used for a specific finding** | A literature review is cited for a specific quantitative finding the review itself does not establish (it only summarizes others). Cite the primary source instead. |

---

## Pre-write fingerprint (Step 0 — before writing the cite)

The strictest prevention is to refuse to write a `\citep{}` that you cannot defend. Before any `\cite*{}` is written for the first time in prose, articulate internally — in plain text, ≤20 words each:

```
claim_fingerprint:   what the sentence claims (specific population, outcome, direction, mechanism)
paper_shows:         what the cited paper actually shows, based on the verification you just did
match_dimensions:    direction ✓/✗ · magnitude ✓/✗ · population ✓/✗ · setting ✓/✗ · mechanism ✓/✗ · evidence-type ✓/✗
```

**Rule.** If **any** of the six dimensions is `✗`, the citation does not go in. Either: (a) drop the citation, (b) soften the claim until the match holds, or (c) flag the gap to the user and let them direct.

This step is non-negotiable for new cites. For audit/batch mode, this same fingerprint structure is what the `citation-verifier` agent returns in its evidence column.

### Red-flag canonical citations

A specific failure pattern: foundational/canonical papers get cited reflexively for **specific mechanism claims** they don't actually make. The paper is so general it *seems* to fit almost any sentence in its broad topic. Examples especially relevant to crime / policing / drug-market work:

- **Becker (1968)** — foundational individual-deterrence model. Routinely misused for network-disruption or supply-side-disruption claims it does not theorize.
- **Becker & Murphy (1988) rational addiction** — consumer-demand theory. Routinely misused for crime / supply-disruption claims it does not establish.
- **Becker, Murphy & Grossman (2006)** — illegal-goods market theory. Frequently miscited for "enforcement lowers violence" when the paper's implication runs the opposite direction (enforcement can raise violence through market disruption).
- **Goldstein (1985) tripartite framework** — concept-defining paper for drug/violence channels (psychopharmacological, economic-compulsive, systemic). Valid when cited *for the channel concept*; not valid when cited as evidence for a specific policy intervention (e.g., raids reducing crime).
- **Levitt (1997)** — police-on-crime causal effect via electoral cycles. Routinely overcited for "police reduce crime" claims; the specific IV and population matter (US cities, mayoral cycles), and McCrary 2002's critique of the IV should be acknowledged when invoking Levitt for a contested claim.
- **Chalfin & McCrary (2017)** — review of police-on-crime evidence. Routinely cited as if it provides a specific number for the elasticity; it is a survey, so cite the primary papers for specific magnitudes.
- **Dell (2015)** — trafficking-related violence in Mexico. Heavily-cited but specific to Mexican municipalities, PAN electoral cycles, and the 2007–2010 window — transportability to Argentina or to 2020s settings is not automatic.

**Rule for red-flag canonicals.** When proposing any of these for a mechanism-specific claim, the verification bar is higher: the cite must show that the *specific* mechanism is in the paper, not just that the paper is in the broad topic. Hedging language ("the broader Becker (1968) framework suggests...") is acceptable only when verified that the framework does in fact support the specific implication.

This list is not exhaustive. Any heavily-cited "foundational" paper deserves heightened scrutiny when paired with a narrow mechanism claim.

---

## When this skill runs

**User-invoked only.** Run when the user explicitly asks for verification — for example:

1. The user runs `/verify-citations` on a specific cite or paragraph.
2. The user asks "does this paper actually say that?", "verify this cite", "check the cites here", etc.
3. The user asks Claude to add a new citation **and** to verify it before finalizing the sentence.
4. The user is auditing a draft for citation soundness (for batch mode, delegate to `/audit-citations`).

Do **not** auto-trigger this skill from:
- `.tex` edits or the mere presence of `\citep{}` / `\citet{}` in a file being read or edited.
- New prose being drafted without an explicit user request to verify.
- Paper-draft writing in general.

Once invoked, run the protocol below in full — do not skip verification because the bibkey "looks reasonable", the paper is well-known, or the claim is "general background." If verification cannot be done (paper inaccessible), mark the citation `INACCESSIBLE` and add the paper to a pending list for the user. See "When the paper is inaccessible" below.

---

## The protocol

For **every** sentence with a citation, execute the following steps before considering the sentence final.

### Step 1 — Isolate the claim

Read the sentence and write down (internally) the **specific assertion** the citation is meant to support. Be precise on:

- **Population / setting**: who, where, when.
- **Outcome**: what is being measured.
- **Direction**: more / less / equal / no effect.
- **Magnitude**: implied by the words used ("substantial", "modest", "negligible") or stated numerically.
- **Type of evidence implied**: descriptive, correlational, or causal.
- **Scope of the claim**: a single finding, a stylized fact, a theoretical mechanism, a methodological choice.

If the sentence makes multiple claims, identify which claim the citation attaches to.

### Step 2 — Check the audit log first

Before fetching anything, read `<paper-subdir>/.citation-audit.md` (sidecar log; see `.claude/rules/citation-audit-log.md`). For this project this will typically be `paper/.citation-audit.md` once the draft exists.

- If this `(bibkey, claim-fingerprint)` pair is already logged as `BIB_OK + VALID` and the claim has not materially changed → skip to Step 6 and reuse the prior verdict. Add a reference to the existing log row.
- If logged as `MISMATCH`, `AMBIGUOUS`, or `BIB_FAIL` → still re-attempt verification this session (the user may have since attached the PDF, or the claim may have been edited).

### Step 3 — Resolve the bibkey + .bib drift check (Layer 1)

Read the document's `.bib` file. Extract:

- Full author list.
- Title.
- Year.
- Journal / working paper series / outlet.
- DOI or URL if present.

If the bibkey is not in the `.bib` → stop and tell the user. Do not invent.

**.bib drift check (Layer 1).** Before fetching the paper online, also do a fast sanity check on the `.bib` entry itself. Compare the author / year / title in the `.bib` against the actual published metadata you find online in Step 4. Failure modes to catch:

- **Wrong year.** A bibkey labelled `Smith2020` whose `.bib` entry actually has `year = {2020}` but the paper was published in 2019 (preprint date confused with publication date).
- **Wrong outlet.** `.bib` says `journal = {Quarterly Journal of Economics}` but the paper appeared in `Journal of Public Economics`.
- **Wrong title.** `.bib` title is paraphrased or guessed; the actual title is different. Often a sign the bibkey was hand-typed instead of imported.
- **Wrong author.** The first author is correct but a co-author is wrong or missing — common when a bibkey was created from memory.

If you find drift, flag it to the user as **BIB-DRIFT** in addition to whatever substantive verdict you reach. Record `bib_check = BIB_FAIL` in the log row with the matching failure mode in the `failure_mode` column. Format the chat report as:

> ⚠️ **Bib-drift — `BibkeyYear`**
> .bib entry says: [field = value]
> Actual published metadata: [field = value]
> Recommendation: update the `.bib` entry; the substantive verdict for this audit is [VALID/MISMATCH/...] but the bibkey itself is mislabelled.

If the bib has no DOI at all, record `bib_check = BIB_NO_DOI` and recommend the user add one. The substantive check still proceeds.

This catches the case where the bibkey *looks* right (`Becker1968`) but the underlying entry is malformed (wrong title, wrong journal, etc.), which the substantive check alone would miss.

### Step 4 — Obtain and read the paper

This repo does not maintain a local PDF library for every cite. Locate the paper online:

1. **Search for the published version first** (journal site, publisher, DOI).
2. **If inaccessible (paywall, no access), search for an open-access working paper version** (NBER, IZA, SSRN, CEPR, RePEc, author's personal page, university repository). A working paper version counts as a valid substitute *if* it contains the finding being cited; note the version used in the audit log.
3. **Read the relevant sections, not just the abstract.** Abstracts and introductions overstate; the body is what counts. At minimum read: the section presenting the finding, the relevant table/figure caption, and any caveats in the conclusion. For methodological citations, read the method section.
4. **Do not rely on second-hand summaries** (other papers' lit reviews, blog posts, Wikipedia) for the substantive check. They can be used to *find* the paper, not to *verify* it.

**Search tooling.** this project does not have a Python search client. Use, in order:

1. **OpenAlex MCP** — DOI lookup, author/title resolution, free.
2. **paper-search-mcp** — multi-source (arXiv, Semantic Scholar, OpenAlex, Crossref, RePEc, PubMed, others), free.
3. **Serper MCP** (`google_search` or `google_search_scholar`) — for web-space coverage when academic APIs don't surface the paper.
4. **WebFetch** — direct GET on a known URL (publisher page, NBER working-paper PDF, author's personal page).

If no version of the paper can be accessed → go to "When the paper is inaccessible."

### Step 5 — Run the substantive check (Layer 2)

Compare what the paper actually shows against the assertion isolated in Step 1. Decide:

- **VALID** — the paper directly supports the specific assertion. Note the section/table/page that contains the support.
- **MISMATCH** — the paper is on the broad topic but does not support the specific assertion. Identify which failure mode (from the table above) applies and why.
- **AMBIGUOUS** — the paper *partially* supports the assertion (e.g., correct direction but the claim's magnitude is stronger than the paper's estimates; correct outcome but different population). In practice, treat AMBIGUOUS as a soft MISMATCH: do not let the sentence stand unchanged.

Be conservative. If the paper does not clearly support the claim, it is not VALID.

### Step 6 — Record the verdict and act

Update `<paper-subdir>/.citation-audit.md` with one row per `(bibkey, claim-location)` pair, using the 10-column schema in `.claude/rules/citation-audit-log.md`.

Then act on the verdict:

- **BIB_OK + VALID** → leave the sentence as is. Verification is complete.
- **BIB_FAIL** → fix the `.bib` entry before doing anything else. Re-run Step 3.
- **Substantive MISMATCH** or **AMBIGUOUS** → do NOT silently rewrite. Report the issue to the user in the chat, propose options:
  1. Drop the citation.
  2. Replace with a better-fitting paper (and propose candidates if any are known).
  3. Soften the claim to match what the paper actually shows.
  4. The user disagrees with the verdict and wants to keep the citation (record their override in the log with a brief rationale).

  Wait for user direction before changing the prose. Never override the user, but never silently let a MISMATCH ship either.

- **INACCESSIBLE** → keep the citation in the prose, log it, and add the paper to the session's pending list (see below). Continue writing.

---

## When the paper is inaccessible

The fallback is approved explicitly: **do not block on inaccessibility.** Procedure:

1. Mark the citation `INACCESSIBLE — PDF needed` in `.citation-audit.md` with the reason (paywall / no preprint found / search did not return the paper / etc.).
2. Continue with subsequent writing.
3. At the **end of the writing session or on user request**, present a consolidated list:

   > **Papers needing PDFs for substantive verification:**
   > - `Bibkey1` — Author (Year), "Title" — reason
   > - `Bibkey2` — Author (Year), "Title" — reason
   >
   > Please attach these so I can complete verification.

4. Once the user attaches PDFs, re-run Steps 4–6 for each.

Note: a **working paper version** found online is acceptable. Only fall back to "PDF needed" when *no* version (published or working) is accessible.

---

## Reporting MISMATCHES inline

When a MISMATCH or AMBIGUOUS verdict comes up while writing, surface it immediately in the chat with this structure:

> ⚠️ **Citation flag — `BibkeyYear`**
> **Sentence:** [the sentence as drafted]
> **Specific claim:** [what the cite is supposed to support]
> **What the paper actually shows:** [one-paragraph factual summary from the paper itself, with section/table reference]
> **Failure mode:** [from the table above]
> **Options:** [drop / replace / soften / override]

Keep the report compact. The user wants the verdict and the evidence, not a long preamble.

---

## What this skill does NOT do

- **Does not opine on whether the claim is true.** It only checks whether the *cited paper* supports the claim. If the claim is true but the cited paper does not establish it, the citation is still a MISMATCH.
- **Does not fabricate citations.** If a MISMATCH leaves a claim uncited, propose this to the user; never invent a replacement citation.
- **Does not modify `.bib` files** without explicit user request — except as required by a confirmed BIB_FAIL fix that the user has greenlit.

---

## Delegation: substantive verification of a single paper

The actual reading and judgment for one paper is delegated to the `citation-verifier` agent (see `.claude/agents/citation-verifier.md`). Invoke it with:

- The bibkey
- The full bib entry
- The sentence and the isolated claim (from Step 1)
- The document path (so the orchestrator can update the audit log)

The agent returns a verdict (`VALID` / `MISMATCH` / `AMBIGUOUS` / `INACCESSIBLE`) with evidence and a pre-formatted `AUDIT_LOG_ROW`. This skill is the orchestrator; the agent is the worker. Using the agent isolates the paper-reading context from the writing context. The skill — not the agent — is the single writer to `.citation-audit.md`.

For batch audit of an entire `.tex` file or a whole `paper/` subdirectory, use the `/audit-citations` slash command, which loops this skill over every citation in the target.

---

## Quick reference — decision tree

```
Adding/editing a cite in prose
        │
        ▼
  Isolate the specific claim (Step 1)
        │
        ▼
  Already in audit log as BIB_OK+VALID & claim unchanged? ──Yes──► reuse
        │ No
        ▼
  Resolve bibkey from .bib + BIB-DRIFT check (Step 3)  ← Layer 1
        │
        ▼
  Search published version → search working paper version (Step 4)
        │
        ├── Found → read the relevant sections
        │           │
        │           ▼
        │     Compare to claim (Step 5)  ← Layer 2
        │           │
        │           ├── VALID → log, keep sentence
        │           ├── MISMATCH → log, surface to user, do NOT silently rewrite
        │           └── AMBIGUOUS → treat as soft MISMATCH
        │
        └── Not found → log INACCESSIBLE, continue, add to pending list
```

---

**Default posture: be strict and conservative. A MISMATCH that ships is worse than a MISMATCH that is flagged and discussed.**
