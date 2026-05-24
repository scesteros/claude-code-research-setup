---
name: seminar
description: User-invoked constructive feedback on a research artefact about to be presented at an econ seminar / workshop / brown-bag / supervisor meeting. Dispatches 5 (or 6 with --audience) fresh-context discussant personas in parallel — Friendly Supervisor, Methodology Helper, Mechanism Skeptic, Lit Connector, Extension Architect, (+ Audience Coach). Posture is constructive (econ-seminar discussant, not hostile referee). Returns themed feedback: strengths to lead with, suggestions by theme, anticipated audience questions, pre-seminar punchlist. Trigger only when the user runs /seminar or explicitly asks for "seminar feedback" / "what would my colleagues say" / "prep for the brown bag" / "constructive review for the workshop". Do NOT auto-trigger from slide / paper edits. Different from /council (hostile pre-submission stress-test) and from /review-paper (prose+substance review).
argument-hint: "<target-file-or-section> [audience] [persona:p1,p2,...] [depth:light|standard|deep] [help]"
allowed-tools: ["Read", "Grep", "Glob", "Task", "Write", "Bash"]
---

# /seminar

*v1.0 — 2026-05-24 — constructive companion to `/council`. Where `/council` dispatches hostile-referee personas for pre-submission stress-testing, `/seminar` dispatches helpful-discussant personas for in-progress feedback. Same orchestrator architecture (Task-based parallel dispatch of a single agent file with persona-via-prompt). Different agent (`seminar-discussant` vs `council-critic`), different output (themed synthesis vs ranked items), different posture (constructive vs adversarial).*

Get 5 helpful colleagues to give you constructive feedback on what you are about to present — strengths to lead with, suggestions ordered by impact and tagged with effort, anticipated Q&A questions, and a pre-seminar punchlist. The value is in surfacing what discipline-specific colleagues with different lenses would say — feedback the user cannot easily generate alone because it comes from a Rolodex of background they don't have.

## When to use

- Slides ready (or nearly ready) for a brown-bag, workshop, internal seminar, supervisor meeting.
- Preliminary results just finished — what should the talk emphasize?
- Paper section drafted — what will the audience push on when this slide goes up?
- Choosing what to present at all — "given these 3 results, which one leads?".
- Dress rehearsal — final pass before walking into the room.

## When NOT to use

- Pre-submission referee-style stress test → use [`/council`](../council/SKILL.md) for hostile-referee personas.
- Prose / voice critique of a draft → use [`/review-paper`](../review-paper/SKILL.md) (orchestrates `paper-reviewer` for prose, optionally `domain-reviewer` for substance).
- Single-perspective plan review → use [`/review-plan`](../review-plan/SKILL.md).
- Citation verification → use [`/verify-citations`](../verify-citations/SKILL.md) or [`/audit-citations`](../audit-citations/SKILL.md).
- Quick 5-7 critical questions in one perspective → use [`/devils-advocate`](../devils-advocate/SKILL.md).

## Inputs

The `$ARGUMENTS` parser accepts:

| Argument | Default | Meaning |
|---|---|---|
| `<target>` (positional) | — | Path to a file (`.tex`, `.md`, `.pdf`, `.do`) OR a section reference (`<file>:§<section>`) OR `--inline` to read from the next conversation message |
| `audience` | off | Dispatch the 6th persona (Audience Coach). Useful when target is slides; usually unnecessary for paper drafts |
| `persona:p1,p2,...` | all 5 (or 6 with `audience`) | Subset of personas to dispatch. Valid: `Friendly Supervisor`, `Methodology Helper`, `Mechanism Skeptic`, `Lit Connector`, `Extension Architect`, `Audience Coach` (with `audience`) |
| `depth:light\|standard\|deep` | `standard` | `light` = top-3 strengths + top-3 suggestions only; `deep` = each persona reads source context paths in full and verifies any lit pointer |
| `dryrun` | off | Show the dispatch plan and budget estimate without running |
| `help` | off | Print this argument list and stop |

## Pre-checks

1. **Existence of the agent file.** `.claude/agents/seminar-discussant.md` must exist. If missing, abort with: *"Discussant agent file not found at `.claude/agents/seminar-discussant.md`. Cannot run."*
2. **Target reachable.** If `<target>` is a path, verify the file exists. If `<target>` is a section reference, verify the file exists and the section is locatable. If `--inline`, prompt the user to paste the target after the argument parse confirmation.
3. **Auto-detect target type** (informational; passed to discussants):
   - `.tex` with `\frametitle` / `\begin{frame}` → `slides`
   - `.tex` without frames (paper-style) or `.md` in `quality_reports/lit_reviews/` → `paper-section`
   - `.md` in `quality_reports/` or `internal_reports/` not matching above → `results-doc`
   - Anything else → `other`
4. **Budget pre-commit.** Print: *"Seminar feedback will dispatch ${N} discussant personas × ~${30 if standard, 15 if light, 50 if deep}K tokens each = ~${N×budget}K Sonnet tokens. Proceed? [y/N/dryrun]"*

## Phase 1 — Identify the target and gather minimal context

Read the target. Decide whether the discussants need additional context paths:

| Target type | Context to also pass to discussants |
|---|---|
| `slides` | The companion paper draft if one exists (search `internal_reports/`, `quality_reports/lit_reviews/`); the research plan |
| `paper-section` | The other sections of the same paper (siblings); related lit reviews under `quality_reports/lit_reviews/` |
| `results-doc` | The most recent Stata `.log` if one is referenced; the research plan |
| `talking-points` / `other` | Research plan + any document the talking-points reference |

Limit context paths to ≤3 paths. The discussants do not need the whole repo — they need enough to evaluate the target.

**Output of Phase 1** (shown to user before dispatch):

```
SEMINAR FEEDBACK — <target>
Target type: <slides / paper-section / results-doc / talking-points / other>
Context paths to pass: <path1>, <path2>
Personas to dispatch: <list of 5 or 6>
Depth: <light / standard / deep>
Estimated cost: ~<N>K Sonnet tokens, ~<M> minutes wall-clock

Dispatch? [y / N / dryrun / change-personas]
```

## Phase 2 — Dispatch the discussants in parallel

For each persona in the active set (default: all 5; +1 if `audience` flag), spawn one `seminar-discussant` agent via the `Task` tool. All persona dispatches happen **in a single message** so they run concurrently.

**Each dispatch carries:**

1. The persona name (one of the 6 valid names).
2. The target type label.
3. The target content (read by the orchestrator; passed inline in the prompt) — OR the target path if it is short enough to be read by the agent itself, plus context paths.
4. The depth flag.

**Per-persona dispatch prompt skeleton:**

> You are the `seminar-discussant` agent, running the `<persona>` persona only.
>
> Target type: `<type>`.
> Depth: `<depth>`.
>
> Target content (or path to read):
>
> ```
> <inline content or file path>
> ```
>
> Context paths you may read for additional grounding:
> - `<path1>`
> - `<path2>`
>
> Return the structured output per the seminar-discussant output format. No commentary outside the structured block.

## Phase 3 — Collect, validate, and synthesise by theme

Wait for all persona returns. Each return is one structured block (per the agent's output format).

**Validate** each return:
- All four sections present (STRENGTHS / SUGGESTIONS / QUESTIONS / PRE-SEMINAR PUNCHLIST)? If a return is malformed, parse what you can and mark missing sections as "—".
- Effort tags on every suggestion? If a tag is missing, default to `medium` and flag in the synthesis ("effort not tagged by discussant").

**Synthesise by theme.** Unlike `/council` (which ranks by composite score), seminar feedback is qualitative and constructive. Group suggestions across discussants by theme:

| Theme | Typically populated by |
|---|---|
| Framing & narrative | Friendly Supervisor, Audience Coach |
| Methodology & robustness | Methodology Helper, Mechanism Skeptic |
| Mechanism & interpretation | Mechanism Skeptic, Methodology Helper |
| Connections to literature | Lit Connector, occasionally Friendly Supervisor |
| Extensions & next steps | Extension Architect |
| Presentation craft | Audience Coach (only if dispatched) |

If a suggestion does not fit a theme cleanly, put it in a final "Other" theme. Do not force a fit.

**De-duplicate questions.** Multiple discussants may anticipate similar Q&A questions. Cluster near-duplicates; preserve the persona attribution for each cluster.

**Identify disagreements.** Where do discussants pull in different directions? Common patterns:
- Friendly Supervisor says "lead with finding X"; Mechanism Skeptic says "X needs more hedging before you can lead with it"
- Extension Architect proposes a follow-up that Lit Connector points out is already done by Y et al.
- Methodology Helper suggests adding spec Z; Audience Coach says the existing table is already too dense

Surface these in a dedicated `DISAGREEMENT MAP` section.

## Phase 4 — Present the feedback report

Output the report in this exact structure. Use the template verbatim.

```
SEMINAR FEEDBACK — <target>
Dispatched: <persona list>  |  Depth: <depth>  |  <total suggestions> suggestions, <total questions> anticipated questions

════════════════════════════════════════════════════════════════
STRENGTHS TO LEAD WITH (across discussants)
════════════════════════════════════════════════════════════════

Convergent (cited by ≥2 discussants):
1. <strength> — [<persona-list>]
2. ...

Single-persona but worth noting:
- <strength> — [<persona>]
- ...

════════════════════════════════════════════════════════════════
SUGGESTIONS BY THEME
════════════════════════════════════════════════════════════════

▸ Framing & narrative (<N>)
  1. <suggestion> — [<persona>] — effort: <low/med/high>
  2. ...

▸ Methodology & robustness (<N>)
  1. ...

▸ Mechanism & interpretation (<N>)
  1. ...

▸ Connections to literature (<N>)
  1. <suggestion> — [<persona>] — effort: <low/med/high>
     (NOTE: cite unverified — discussant flagged "to check")
  2. ...

▸ Extensions & next steps (<N>)
  1. ...

▸ Presentation craft (<N>)   [only if Audience Coach was dispatched]
  1. ...

════════════════════════════════════════════════════════════════
LIKELY AUDIENCE QUESTIONS (de-duplicated)
════════════════════════════════════════════════════════════════

1. <question>
   Anticipated by: <persona-list>
   Suggested prep: <one-line cue>

2. ...

════════════════════════════════════════════════════════════════
DISAGREEMENT MAP — where discussants pull in different directions
════════════════════════════════════════════════════════════════

- <topic>: <persona A>'s view vs <persona B>'s view
  Likely cause: <one line>
  How to resolve: <one line — usually "decide based on your audience" or "test by running spec X">

(If no disagreements: "All discussants converge on the suggestions above. No internal tension to resolve.")

════════════════════════════════════════════════════════════════
PRE-SEMINAR PUNCHLIST (must-fix in the next 24h)
════════════════════════════════════════════════════════════════

(Only items that any discussant flagged as blocking.)

- [<persona>] <item>
- ...

(If empty: "No blockers flagged. The talk is shippable as-is.")

════════════════════════════════════════════════════════════════
ITERATION GATE
════════════════════════════════════════════════════════════════

Options:
- accept                          — persist this report to quality_reports/seminar-feedback/ and append to research-archive INDEX
- focus <theme>                   — drill into one theme; re-dispatch discussants with focus prompt
- redispatch <persona>            — re-run one persona with sharper inputs
- redispatch-with-audience        — add Audience Coach (if it was not in original dispatch)
- dismiss                         — end without persisting
```

Wait for the user's selection. Default action is `dismiss` if the user does not respond.

## Phase 5 — Persist the report (if accepted)

If the user selects `accept`, write the report to:

```
quality_reports/seminar-feedback/<YYYY-MM-DD>_<short-target-slug>.md
```

Use today's date and a kebab-case slug derived from the target filename or topic. Append a row to the central research-archive INDEX:

```bash
python "~/research-archive/append_index.py" \
  --project this project --type seminar-feedback \
  --topic "<≤60-char description of what was feedback'd>" \
  --path "<absolute path to the feedback report just written>" \
  --notes "<N> suggestions / <N> questions / <K> blockers / depth:<depth>"
```

Per [`.claude/rules/research-archive-protocol.md`](../../rules/research-archive-protocol.md).

## Error handling

- **Agent file missing.** Abort with a clear install pointer (see Pre-checks 1).
- **Target file not found / section not locatable.** Re-prompt for a corrected path. If still missing, abort.
- **One persona dispatch fails** (timeout, error). Surface in the report: *"Persona `<X>` failed (`<error>`). Synthesis computed on remaining N-1 discussants. Re-run with `redispatch <X>` to fill the gap."* Continue with the others.
- **All persona dispatches fail.** Abort and report. Do not persist a partial report.
- **`Task` tool unavailable.** Abort with: *"This skill requires the `Task` tool to dispatch sub-agents. It is currently unavailable. Cannot run."*

## Cost reminder

5 `seminar-discussant` dispatches × ~30K tokens each = ~150K Sonnet tokens at `standard` depth (~3 min wall-clock). Add ~30K for the 6th persona (`audience`). `depth:light` drops to ~80K (5 × ~15K); `depth:deep` rises to ~250K (5 × ~50K).

Use `depth:light` for "quick prep before a 30-min brown bag". Use `depth:deep` for "dress rehearsal before a job-talk or formal seminar".

## When to use `/seminar` vs `/council` vs `/review-plan`

| If you want... | Use |
|---|---|
| Constructive feedback before presenting in-progress work to colleagues | **`/seminar`** |
| Hostile pre-submission stress test (referee mindset) | [`/council`](../council/SKILL.md) |
| Single-perspective plan review with 6 dimensions | [`/review-plan`](../review-plan/SKILL.md) |
| 5-7 critical questions from one perspective | [`/devils-advocate`](../devils-advocate/SKILL.md) |
| Prose / voice / argument-structure review | [`/review-paper`](../review-paper/SKILL.md) |

`/seminar` and `/council` are complementary:
- During the project (preliminary results → seminar prep → revised analysis): `/seminar`.
- Before submission (paper draft → camera-ready): `/council`.

A typical flow for a paper: develop results → `/seminar` (brown-bag prep) → revise per feedback → `/seminar` (workshop prep) → revise → `/review-paper` (prose audit) → `/audit-citations` → `/council` (pre-submission stress test) → submit.

## Related

- [`.claude/agents/seminar-discussant.md`](../../agents/seminar-discussant.md) — the per-persona agent. Required.
- [`/council`](../council/SKILL.md) — adversarial counterpart for pre-submission.
- [`/review-paper`](../review-paper/SKILL.md), [`/review-plan`](../review-plan/SKILL.md), [`/devils-advocate`](../devils-advocate/SKILL.md) — single-perspective reviews; complementary, not substitute.
- [`.claude/rules/skill-design-patterns.md`](../../rules/skill-design-patterns.md) — patterns this skill applies (Phased Execution §1.1, Output Templates §1.4, Iteration Gate §1.5, Depth Calibration §1.6, Graceful Degradation §1.7).
- [`.claude/rules/research-archive-protocol.md`](../../rules/research-archive-protocol.md) — INDEX append rule that Phase 5 applies.
- [`.claude/rules/claim-discipline.md`](../../rules/claim-discipline.md) — the Lit Connector persona must follow no-fabrication discipline when proposing literature pointers.
