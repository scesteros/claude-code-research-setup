# Tool Limitations

**Applies to:** every session.

**Established:** 2026-05-24. Adapted from [chrisblattman/claudeblattman / docs/downloads/tool-limitations.md](https://github.com/chrisblattman/claudeblattman/blob/main/docs/downloads/tool-limitations.md) (MIT), with this project-specific additions (Stata, xelatex, web scrapers).

**Spirit:** when the task at hand is better served by a different tool, Claude should say so once and offer to proceed or hand off — instead of struggling silently. Honesty about limitations is more useful than pretending to do everything.

---

## 1. When to hand off

The table flags categories where Claude is reliably the wrong tool, with the suggested handoff.

| Task category | Why Claude is weak here | Suggested handoff |
|---|---|---|
| **Stata execution** | Edit-only by repo convention; Claude does not run Stata. | User runs the `.do` manually after Claude emits it. |
| **xelatex / pdflatex execution** | Edit-only by repo convention; Claude does not compile LaTeX in this repo. | User compiles manually with the command Claude prints. |
| **Python scrapers (`<pipeline-source-path>/`)** | Edit-only by convention; the user runs the scraper inside the project's venv. | User runs `python scraper_*.py` after activating `.venv/Scripts/activate`. |
| **Heavy `.dta` introspection (large Stata binary)** | Claude cannot reliably parse Stata binary; results may be wrong. | Open in Stata; or export to CSV first and have Claude read that. |
| **Spreadsheet manipulation (XLSX with formulas, pivots, complex formatting)** | Claude can read CSV; cannot reliably edit XLSX formulas or formats. | Stay in Excel / Sheets; or use Gemini for spreadsheet-native work. |
| **Video / audio files** | Claude cannot process video or audio directly. | Use Gemini for media analysis; or work from transcripts (which Claude can analyse). |
| **Real-time collaborative editing of Google Docs** | MCP can read/write but there is no live co-edit mode. | Work in the document; periodically ask Claude to re-read the current state. |
| **Quantitative arithmetic in conversational responses (regression coefficients, budget calculations, sample-size math, post-hoc significance recomputation)** | In-line arithmetic is unreliable. | Write Python to compute (or recommend Stata/Wolfram for the user); never trust uncomputed in-line numbers. |
| **Live web data after the model knowledge cutoff** | Claude's knowledge cutoff is January 2026; events after that may be missing or wrong. | Use WebSearch / WebFetch (per skill conventions) or recommend Perplexity. |
| **Multi-source literature surveys / "find everything about X"** | `/lit-review` is good; deeper sweeps benefit from a different shape. | Recommend ChatGPT Deep Research or Perplexity for breadth; bring results back into `/lit-review` for verification. |
| **Citation-backed factual lookups with required source URLs** | Claude can fabricate plausible citations; lacks source-link discipline by default. | Recommend Perplexity for sourced answers; or use `/verify-citations` to vet anything Claude proposes. |
| **Image generation (figures, diagrams, illustrations)** | Claude generates none. | DALL-E / Midjourney / Stable Diffusion. For research diagrams: tikz/asymptote in LaTeX, ggplot/matplotlib in R/Python. |
| **PDF tables with merged cells / OCR / multi-column** | Extraction is often garbled. | Copy-paste the specific section; or re-export the PDF; or use Adobe Acrobat's extraction. |
| **Scheduled / background automation** | Claude runs only when invoked; no cron, no background jobs. | OS-level scheduler (Task Scheduler on Windows, cron on Unix), or `/schedule` skill (remote agents) for routines that should fire on a cron. |
| **Legal / tax / medical advice** | Claude can summarise; should not be the only source for consequential decisions. | Consult a professional; Claude can prepare the question and the source materials. |

## 2. How Claude should flag a limitation

When the user asks for something on this list, say so once and offer to proceed or hand off. One sentence. No prolonged apology.

**Template:**

> "I can attempt this, but for [task category] my output will be limited because [reason]. For better coverage, [handoff suggestion]. Want me to proceed with what I can do, or would you prefer to hand off?"

**Worked example (PDF extraction):**

> "I can try to extract the table from this PDF, but if cells are merged or the columns are scrambled in OCR, the result will be wrong without me catching it. Faster path: copy-paste the relevant rows or re-export the PDF as text. Want me to try first, or want to paste the rows?"

**Worked example (live data):**

> "I do not have reliable post-January-2026 data. I can pull what's accessible via WebSearch, but Perplexity will give you fuller coverage with source links. Proceed with WebSearch, or hand off?"

## 3. What this rule is *not*

- **Not an excuse to refuse work.** When the user explicitly says "do it anyway", do it — with the flagged caveat noted in the output.
- **Not a substitute for `verify` / `verification-protocol`.** Code that Claude writes still needs the standard verification gate before commit, regardless of whether tool-limitations was flagged upstream.
- **Not the only place limitations should appear.** Skill-level limitations belong in the skill's `## Error Handling` section (see `skill-design-patterns.md` §1.7); repo-wide limitations belong here.

## 4. What Claude *does* do well (stay here)

For balance: tasks for which Claude is the right tool and no handoff is needed.

- Editing `.do`, `.py`, `.tex` files (the repo's edit-only convention).
- Drafting and revising academic prose (papers, slides, internal reports).
- Reading and summarising local files (PDFs of cited papers, Stata `.log` files, pipeline CSVs).
- Multi-file consistency audits via `/cross-doc-audit`, `/deep-audit`, `/audit-citations`.
- Literature-review synthesis via `/lit-review` (paired with full-PDF reads by `citation-verifier`).
- Spawning parallel subagents for fresh-context evaluation (`/review-paper`, `/audit-citations`, `/council`).
- Spec-design conversations via `/data-analysis` and `/interview-me`.
- Git-flow operations via `/commit`.

When in doubt: try Claude first, flag the limitation if it shows up, hand off rather than struggle.

---

## 5. Related rules

- [`.claude/rules/skill-design-patterns.md`](skill-design-patterns.md) — §1.7 Graceful Degradation (skill-level analogue of this rule).
- [`.claude/rules/verification-protocol.md`](verification-protocol.md) — code-side verification (independent of tool-limitations flagging).
- [`.claude/rules/quality-gates.md`](quality-gates.md) — shipping bars; flagged limitations should be acknowledged in the output, not silently downgraded.
