---
name: audit-citations
description: User-invoked batch audit of every citation in a `.tex` file or paper subdirectory for substantive validity. Trigger only when the user runs `/audit-citations` or explicitly asks to audit/review/check citations across a draft — e.g., "audit the citations in paper/", "review references in the abstract", "check that the cites are right". Do NOT auto-trigger from `.tex` edits or from passive matching on `\citep{}` / `\citet{}`. Batch counterpart of verify-citations: scans the target, runs substantive verification on every `\citet{}` / `\citep{}` found, and produces a consolidated report plus an updated audit log.
argument-hint: "[target .tex file or document subdirectory; optional --adversarial]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "WebSearch", "WebFetch", "Agent"]
---

# /audit-citations

Audits every citation in a paper subdirectory for **substantive** validity (does the paper support the specific claim?) **and** bibliographic correctness (does the bib entry match the API record at the cited DOI?). Uses the 10-column audit-log schema in [`.claude/rules/citation-audit-log.md`](../../rules/citation-audit-log.md).

> **Status note (this project):** the citation toolkit ships dormant. There is no mandatory orchestrator gate. Invoke this skill manually with `/audit-citations <paper-subdir>` once a paper draft begins.

## When to use

- The user runs `/audit-citations <target>`.
- The user asks to audit, review, check, or verify citations across an existing draft, section, or full paper subdirectory (typically `paper/`).
- A draft was written before the `verify-citations` skill was introduced and needs to be back-filled.
- The user wants a one-shot report of all MISMATCHES across a document.
- Pre-submission hygiene pass.

For new prose being written one sentence at a time, use the `verify-citations` skill directly — this command is for batch mode.

## Inputs

- **Target**: a path to a `.tex` file, a `sections/` directory, or a whole paper subdirectory (e.g., `paper/`, `paper/sections/`). Ask the user if not specified.
- **Scope**: by default, audit every `\citet{}`, `\citep{}`, `\citeauthor{}`, `\citeyear{}` in the target. If the user wants a narrower scope (e.g., "only section 2"), respect it.
- **Mode flag (optional)**: `--adversarial` runs the `citation-adversary` agent as a second-opinion pass on every cite the first verifier marks VALID. Use for pre-submission audits, contested claims, or whenever the user wants higher-confidence verification at roughly 2× cost. Default is single-pass.

## Procedure

### 1. Inventory

Enumerate every citation in the target. Build a working table with:

| location (file:line) | bibkey | sentence (verbatim) |
|---|---|---|

Resolve multi-key cites: `\citep{A, B}` becomes two rows (one per bibkey).

### 2. Cross-check with the audit log

Read `<paper-subdir>/.citation-audit.md` (the 10-column schema). For each row in the working table, check whether `(bibkey, location)` already has a `BIB_OK + VALID` entry and the claim has not changed.

- If yes → mark as "already verified" and skip to step 4.
- If no → queue for verification.

### 3. Verify each queued citation

For each citation in the queue, follow the protocol of the `verify-citations` skill: Step 1 (isolate the claim), Step 3 (resolve bibkey + BIB-DRIFT check = Layer 1), Step 4 (obtain and read the paper), Step 5 (substantive check = Layer 2). Delegate the actual paper-reading and verdict to the `citation-verifier` agent. One agent invocation per citation. Verifier invocations may run in parallel.

**Important — concurrent writes:** the `citation-verifier` agent does NOT write to `<paper-subdir>/.citation-audit.md` itself (concurrent writes race). Instead, each agent returns its verdict block, which contains a pre-formatted `AUDIT_LOG_ROW`. This skill is the **single writer** to the log (orchestrator-writes pattern).

Search tooling for the verifier agents (this project does not have a Python search client):

1. **OpenAlex MCP** — DOI → authors/title/year/journal verification (Layer 1).
2. **paper-search-mcp** — multi-source (Semantic Scholar, Crossref, arXiv, RePEc, etc.).
3. **Serper MCP** (`google_search_scholar`, `google_search`) — escalation for hard-to-find papers.
4. **WebFetch** — direct GET on a known URL.

If the document has many citations, batch sensibly but do **not** sacrifice depth — each paper still needs to be read substantively for its specific claim. If the queue is very long, ask the user whether to proceed all-at-once or section-by-section.

### 3b. Adversarial pass (only if `--adversarial` flag set)

For every cite the first verifier returns as VALID, invoke the `citation-adversary` agent (see `.claude/agents/citation-adversary.md`) with the same (bibkey, claim, sentence) inputs plus the first verifier's evidence. The adversary reads the paper independently in fresh context with the explicit posture "disagree if you can".

Reconcile the two verdicts:
- **CONFIRM** → VALID stands. Note `adversary_confirmed: yes` in the log row's evidence cell or in a sidecar note.
- **DISSENT** → demote VALID to the adversary's proposed verdict (MISMATCH or AMBIGUOUS). Use the adversary's evidence in the log row and surface the dissent to the user in the report.
- **INACCESSIBLE** → VALID stands but note `adversary_confirmed: no — inaccessible`. Surface to the user.

The first verifier's MISMATCH/AMBIGUOUS verdicts are not re-checked adversarially (those are already negative — a second negative adds little).

### 4. Update the audit log (orchestrator-writes pattern)

Collect every returned `AUDIT_LOG_ROW` from the verifier agents. Then:

1. Read the current `<paper-subdir>/.citation-audit.md` (if it exists).
2. For each returned row:
   - If a row with the same `(bibkey, location)` exists → replace it (update in place).
   - Otherwise → append it.
3. Refresh the `Last updated:` header line at the top.
4. Write the file back in a **single** Write call. Never let multiple agents write concurrently.

If the file does not exist yet, create it with the 10-column schema header from `.claude/rules/citation-audit-log.md`.

### 5. Reconcile .tex against the log (orphan-row reconciliation)

Before producing the report, run a diff between the cites in the `.tex` and the rows in the log:

- **In `.tex` but not in log** → these were never verified. Add to the verification queue (re-run Step 3 for these only).
- **In log but not in `.tex`** → orphaned rows (a cite that was removed from the prose, e.g., during a previous revision). Flag these in the report under an "Orphaned log rows" section and ask the user whether to delete them.

This step closes a known drift mode: when prose is edited (cite dropped, moved, or renamed) without synchronizing the log.

### 6. Produce a consolidated report

Present to the user, in the chat, a structured summary:

```
Citation audit — <target>

Total citations audited: N
  BIB_OK + VALID:        n_valid
  BIB_FAIL:              n_bib_fail
  Substantive MISMATCH:  n_mismatch
  AMBIGUOUS:             n_ambiguous
  INACCESSIBLE:          n_inaccessible
  BIB_NO_DOI:            n_no_doi
  Already verified (skipped): n_skipped
  Overridden by user:    n_overridden

── BIB_FAIL ──────────────────────────────────────
1. <bibkey> at <file:line>
   .bib says: <field = value>
   API record says: <field = value>
   Failure mode: <wrong_authors | wrong_year | wrong_title | wrong_journal>
   Suggested fix: rewrite the bib entry from the API record

── Substantive MISMATCH ──────────────────────────
1. <bibkey> at <file:line>
   Sentence: "..."
   Specific claim: ...
   What the paper shows: ... (section/table reference)
   Failure mode: <mode>
   Suggested fix: drop | replace | soften

2. ...

── AMBIGUOUS ────────────────────────────────────
...

── INACCESSIBLE — PDF NEEDED ────────────────────
- <bibkey> — <author, year>, "<title>" — reason
- ...

── VALID (summary only) ─────────────────────────
<n_valid> citations confirmed. Details in .citation-audit.md.

── ORPHANED LOG ROWS (no longer in .tex) ─────────
- <bibkey> @ <stale location> — proposed action: delete row

[--adversarial mode only]
── ADVERSARIAL DISSENTS ─────────────────────────
- <bibkey> @ <location>: first verifier said VALID; adversary DISSENTS — <failure mode> — <one-line evidence>
```

### 7. Wait for user direction on critical verdicts

Do not modify the `.tex` automatically. The user decides for each BIB_FAIL / MISMATCH / AMBIGUOUS:

- Drop the citation
- Replace with a better-fitting paper (propose candidates only if you can identify them confidently; otherwise leave to the user)
- Soften the claim to match the paper's actual support
- Rewrite the bib entry to match the API record (for BIB_FAIL)
- Override the verdict (record the override and rationale in the audit log's `overridden_by_user` cell)

For INACCESSIBLE citations, present the consolidated PDF-needed list at the end and pause — the user attaches the PDFs and you re-run verification on those entries only.

## Posture

- **Strict**, same as the `verify-citations` skill. A MISMATCH that ships is worse than a MISMATCH that is flagged.
- **No silent rewriting** of the `.tex`. All edits to prose or citations require user direction.
- **No fabrication** of replacement citations. Fabricating a citation is prohibited.
- **Reuse the audit log** to avoid redundant work — but only when the claim is unchanged.
- **Orchestrator is the sole writer to the audit log** — even when verifier agents run in parallel, log writes are serialized through this skill.

## Related

- `verify-citations` skill — per-citation substantive verification during writing.
- `citation-verifier` agent — fresh-context per-citation worker.
- `citation-adversary` agent — adversarial second-opinion worker (only when `--adversarial`).
- `.claude/rules/citation-integrity.md` — flagship zero-tolerance policy.
- `.claude/rules/citation-audit-log.md` — 10-column schema and lifecycle.
- `.claude/rules/claim-discipline.md` — overarching claim posture.
- `.claude/rules/quality-gates.md` — citation severity → CRITICAL / MAJOR mapping.
