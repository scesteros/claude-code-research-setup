---
name: council
description: User-invoked structured critique of a research target (design, draft, decision, plan, or proposal) by 5 fresh-context critic personas dispatched in parallel — Identification, Pre-Mortem, Catalog Conflict, Practitioner Cost, Hostile Referee. Returns ranked items with composite scores and surfaces blocking concerns. Trigger only when the user runs /council or explicitly asks to "stress-test" / "get a council on" / "five-perspective review" / "multi-critic review" of a specific target. Do NOT auto-trigger from draft edits or from passive matching on plan files. Different from /review-plan (single 6-dimension critique by plan-reviewer); /council uses 5 independent personas for higher disagreement bandwidth.
argument-hint: "<target-file-or-section> [persona:p1,p2,...] [depth:standard|deep] [items:auto|listed]"
allowed-tools: ["Read", "Grep", "Glob", "Task", "Write", "Bash"]
---

# /council

*v1.0 — 2026-05-24 — adapted from `chrisblattman/claudeblattman / skills/council.md` (MIT). Personas re-tuned for academic-economics research targets via `.claude/agents/council-critic.md`.*

Get five independent critics to argue about your design, draft, or decision in parallel. The value is not in any single critic — it is in where they disagree. Use when you suspect your current framing is convergent praise (the self-bias problem) or when the stakes are high enough to want structural disagreement.

## When to use

- A research design that is about to be committed to (paper plan, identification strategy, DiD spec).
- A draft section / abstract / positioning that the user wants stress-tested before sharing.
- A decision among 2–4 alternatives (which sample, which spec, which extension, which submission journal).
- A research-plan revision before sending to supervisors.
- A grant or IRB application before submission.

## When NOT to use

- Prose / voice critique — use `/review-paper` (which calls `paper-reviewer`).
- Methodology-only review — use `/review-paper` with the substance flag (which calls `domain-reviewer`).
- Single-perspective plan review — use `/review-plan` (which calls `plan-reviewer` for the 6-dimension critique). `/council` is the *parallel-disagreement* layer above that.
- Quick yes/no on a one-line decision — overkill for items the user can decide in 60 seconds.

## Inputs

The `$ARGUMENTS` parser accepts:

| Argument | Default | Meaning |
|---|---|---|
| `<target>` (positional) | — | Path to a file (`.md`, `.tex`, `.do`, plain text) OR a section reference (`<file>:§<section>`) OR `--inline` to read from the next conversation message |
| `persona:p1,p2,...` | all 5 | Subset of personas to dispatch. Valid: `Identification`, `Pre-Mortem`, `Catalog Conflict`, `Practitioner Cost`, `Hostile Referee` |
| `depth:standard\|deep` | `standard` | `deep` lets each persona run for longer / read more source context |
| `items:auto\|listed` | `auto` | `auto` = the skill extracts items from the target itself; `listed` = the user provides an explicit numbered list |
| `dryrun` | off | Show the dispatch plan and budget estimate without running |
| `help` | off | Print this argument list and stop |

## Pre-checks

1. **Existence of the agent file.** `.claude/agents/council-critic.md` must exist. If missing, abort with: *"Council agent file not found at `.claude/agents/council-critic.md`. Re-install per `chrisblattman/claudeblattman` adaptation; see PROVENANCE for the council/critic pair."*
2. **Target reachable.** If `<target>` is a path, verify the file exists. If `<target>` is a section reference, verify the file exists and the section is locatable. If `--inline`, prompt the user to paste the target after the argument parse confirmation.
3. **Budget pre-commit.** Print: *"Council will dispatch ${N} critic personas × ~30K tokens each = ~${N×30}K Sonnet tokens. Proceed? [y/N/dryrun]"*. The user types `y` to proceed; `dryrun` switches to show-plan-only mode.

## Phase 1 — Parse the target into items

Read the target. Extract a list of `items` — the things the critics will score, each one a discrete unit a critic can rate 1–5.

**Item-extraction rules by target type:**

| Target type | Items =  |
|---|---|
| Research-plan section / project plan | Each numbered hypothesis (H1, H2, ...), or each numbered section if no hypotheses |
| Paper draft section | Each numbered paragraph or each labelled claim |
| Decision (`option-A` vs `option-B` vs ...) | Each option |
| Empirical spec | Each specification variant (baseline / robustness 1 / robustness 2 / ...) |
| Inline text (free-form) | Each numbered claim or each paragraph |

If the target has no natural items (one continuous prose block), treat the whole target as one item with `id: target-1`. Surface this to the user: *"Target has no natural items; scoring as one block. Want me to break it into paragraphs first? [Y/n]"*

**Output of Phase 1:** an inventory like:

```
TARGET ITEMS

1. H1 — Primary mechanism (the intervention directly disrupts the system)
2. H2 — Externality mechanism (the intervention generates spillovers reducing the outcome)
3. H3 — Counter-effect mechanism (the intervention creates conditions that raise the outcome)
4. Design — Stacked event-study DiD on unit-date panel
5. Spec — Three contamination-handling specifications side by side

Dispatching council across these 5 items.
```

## Phase 2 — Dispatch the council in parallel

For each persona in the active set (default: all 5), spawn one `council-critic` agent via the `Task` tool. All persona dispatches happen **in a single message** so they run concurrently.

**Each dispatch carries:**

1. The persona name (one of `Identification` / `Pre-Mortem` / `Catalog Conflict` / `Practitioner Cost` / `Hostile Referee`).
2. The target type label (`design` / `draft` / `decision` / `plan` / `proposal` / `other`).
3. The full list of items from Phase 1.
4. Source context paths the critic may read.

**Per-persona dispatch prompt skeleton:**

> You are the `council-critic` agent, running the `<persona>` persona only.
>
> Target type: `<type>`.
>
> Items to score (score EVERY item; one block per item):
>
> ```
> 1. <id> — <description>
> 2. <id> — <description>
> ...
> ```
>
> Source context you may read: `<paths>`.
>
> Return the structured blocks per the council-critic output format. No commentary outside the blocks.

## Phase 3 — Collect, validate, composite

Wait for all persona returns. Each return is a stack of blocks (one per item).

**Validate** each return:
- Every item scored? If a persona returned fewer than N blocks, flag and re-prompt that persona once with: *"Persona <X> returned <K> of <N> blocks. Re-score the missing items: <id-list>."*. If the second pass also fails, mark the missing items `score:n/a` and continue.
- Every block has all four fields (TARGET / PERSONA / SCORE / RATIONALE / BLOCKING)? If a block is malformed, parse what you can and mark missing fields `unknown`.

**Composite scoring** per item:

```
composite = mean(non-n/a scores) − 0.1 × blocker_count
```

Where `blocker_count` = number of personas that returned `BLOCKING: <something>` (i.e., NOT `none`) for that item.

Additive penalty, not multiplicative — an item with 5 blockers still keeps most of its mean. The composite ranks; the user gates.

## Phase 4 — Present the ranked report

Output one structured block. Use this template verbatim:

```
COUNCIL REPORT — <target>
Dispatched: <persona list>
Items scored: <N>
Total blockers raised: <K>

────────────────────────────────────────
RANKED ITEMS (composite, high to low)
────────────────────────────────────────

1. <item id> — composite <score>  [<blocker count> blockers]
   <one-line summary of consensus>
   Per-persona:
   - Identification     <score> — <rationale>
   - Pre-Mortem         <score> — <rationale>
   - Catalog Conflict   <score> — <rationale>
   - Practitioner Cost  <score> — <rationale>
   - Hostile Referee    <score> — <rationale>
   Blocking concerns:
   - [<persona>] <blocking text>
   - [<persona>] <blocking text>

2. <item id> — composite <score>  [<blocker count> blockers]
   ...

────────────────────────────────────────
DISAGREEMENT MAP — where personas diverge most
────────────────────────────────────────

- <item id>: Identification scored 4 / Hostile Referee scored 2 — surface the gap
  to the user. Likely cause: <one line>.

────────────────────────────────────────
PROPOSED ACTIONS
────────────────────────────────────────

Top 3 items (composite ≥ 4.0):
  → ship as drafted, optionally address minor blockers

Items 4–7 (composite 3.0–3.9):
  → revise per the dominant blocker; re-run /council after revision

Items below 3.0 OR with ≥3 blockers:
  → defer / redesign / drop. Specific guidance per item above.

────────────────────────────────────────
ITERATION GATE
────────────────────────────────────────

Options:
- accept  — accept the ranking; persist this report to quality_reports/council/
- revise <item-id> <new-text>  — rewrite an item; re-dispatch ONLY that item
- redispatch <persona>  — re-run one persona with sharper inputs
- dismiss — end without persisting
```

Wait for the user's selection. Default action is `dismiss` if the user does not respond.

## Phase 5 — Persist the report (if accepted)

If the user selects `accept`, write the council report to:

```
quality_reports/council/<YYYY-MM-DD>_<short-target-slug>.md
```

Use today's date and a kebab-case slug derived from the target filename or topic. Append a row to the central research-archive INDEX:

```bash
python "~/research-archive/append_index.py" \
  --project this project --type council-report \
  --topic "<≤60-char description of what was councilled>" \
  --path "<absolute path to the council report just written>" \
  --notes "<N> items / <K> blockers / top composite <score>"
```

Per [`.claude/rules/research-archive-protocol.md`](../../rules/research-archive-protocol.md).

## Error handling

- **Agent file missing.** Abort with a clear install pointer (see Pre-checks 1).
- **Target file not found / section not locatable.** Re-prompt the user for a corrected path. If still missing, abort.
- **One persona dispatch fails** (timeout, error). Surface in the report: *"Persona `<X>` failed (`<error>`). Composite computed on remaining 4 personas. Re-run with `redispatch <X>` to fill the gap."* Continue with the others.
- **All persona dispatches fail.** Abort and report. Do not persist a partial report.
- **`Task` tool unavailable.** Abort with: *"This skill requires the `Task` tool to dispatch sub-agents. It is currently unavailable. Cannot run."*

## Cost reminder

Five `council-critic` dispatches × ~30K tokens each = ~150–200K Sonnet tokens per run. Substantial but not prohibitive. For very high-stakes targets (paper submission readiness, IRB), the cost is justified. For routine plan reviews, use `/review-plan` instead.

`depth:deep` raises per-persona token budget to ~50K and is appropriate for paper-submission-readiness or grant-application reviews.

## Related

- [`.claude/agents/council-critic.md`](../../agents/council-critic.md) — the per-persona agent. Required.
- [`/review-plan`](../review-plan/SKILL.md) — single-perspective plan review (6-dimension critique). Use as the cheaper / lighter alternative when stakes are lower.
- [`/devils-advocate`](../devils-advocate/SKILL.md) — 5–7 critical questions, one perspective. Use to spike a quick critique without the full council.
- [`/review-paper`](../review-paper/SKILL.md) — paper-level review orchestrating `paper-reviewer` (prose) + optionally `domain-reviewer` (substance). Orthogonal to `/council`; for prose review, prefer `/review-paper`.
- [`.claude/rules/skill-design-patterns.md`](../../rules/skill-design-patterns.md) — patterns this skill applies (Phased Execution §1.1, Critic Stance §1.3, Iteration Gate §1.5, Depth Calibration §1.6).
- [`.claude/rules/research-archive-protocol.md`](../../rules/research-archive-protocol.md) — INDEX append rule that Phase 5 applies.
