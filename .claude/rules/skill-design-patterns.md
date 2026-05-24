# Skill Design Patterns

**Applies to:** any new or modified file under `.claude/skills/**/SKILL.md` and `.claude/agents/*.md`.

**Established:** 2026-05-24. Adopted from [chrisblattman/claudeblattman](https://github.com/chrisblattman/claudeblattman) (MIT) — `docs/system/patterns.md` and `docs/downloads/skill-patterns.md` — with concrete examples drawn from this repo's existing skills.

**Spirit:** these are reusable design ideas. When authoring a new skill or revising an old one, the patterns below name what good skills already do, so we converge on a small set of well-understood shapes instead of reinventing structure every time.

> **Status note:** this is a *design* rule, not a *behavior* rule. It tells the author what shape to give a skill; it does not change how Claude executes an already-shipped skill at run-time. Pair with [`.claude/rules/quality-gates.md`](quality-gates.md) for the shippability bar.

---

## 1. The eight structural patterns

Each pattern names a recurring shape we want our skills to take. Apply them when they fit; do not force them.

### 1.1 Phased Execution

Break a workflow into numbered phases with explicit `STOP` checkpoints between phases that cannot easily be undone.

```markdown
### Phase 1: Discovery
[Assess current state — read files, inventory the target]

### Phase 2: Analysis
[Present findings; identify gaps]

**STOP: Discuss with user before proceeding.**

### Phase 3: Proposal
[Present a specific plan informed by the discussion]

**Ask for approval before Phase 4.**

### Phase 4: Implementation
[Execute the approved plan]
```

**Use when:** the workflow has 3+ steps and executing the wrong thing is hard to undo (file rewrites, batch edits, audit-log writes).

**Examples in this repo:**
- [`/lit-review`](../skills/lit-review/SKILL.md) — Parse topic → Search → Organize → Identify gaps → Save report.
- [`/audit-citations`](../skills/audit-citations/SKILL.md) — Inventory → Cross-check log → Verify each → Update log → Reconcile orphans → Produce report → Wait for user direction.
- [`/data-analysis`](../skills/data-analysis/SKILL.md) — Spec design (with gate) → Code → Verify → Output.

**Anti-pattern:** a single "do everything" block that does silent file writes without a stopping point.

### 1.2 Flags Parsing

Parse `$ARGUMENTS` for named flags using a `key:value` convention so one skill stays flexible instead of forking into siblings.

```markdown
## Arguments

`$ARGUMENTS` supports:
- `depth:light/standard/deep` — thoroughness level
- `file:path/to/file` — explicit input file
- `focus:dimension` — weight one aspect
- `since:YYYY-MM-DD` — date filter
- `dryrun` — show plan without executing
- `help` — print the option list and stop
```

**Use when:** the same skill should run at multiple thoroughness levels, or against multiple input shapes, without forking.

**Examples in this repo:**
- [`/audit-citations`](../skills/audit-citations/SKILL.md) accepts `--adversarial` to dispatch the `citation-adversary` agent as a second-opinion pass.

**Adopt where missing:** `/lit-review`, `/review-plan`, `/source-audit`, `/cross-doc-audit` could all benefit from `depth:` and `since:` flags. Add when next revising them.

### 1.3 Critic Stance

Explicitly shift Claude's role from collaborator to critic in the skill prose. Counteracts the tendency to be agreeable.

```markdown
**CRITIC STANCE:**
> You are the critic, not the planner. Do not rationalize. Do not
> hedge. Your job is to find what is missing, what will break, and
> what is wishful thinking. If you developed this plan earlier in the
> session, that makes you *more* responsible for finding its flaws,
> not less.
```

**Use when:** the skill asks Claude to critique its own or anyone else's work. The agreeableness default is otherwise hard to overcome.

**Examples in this repo:**
- [`/devils-advocate`](../skills/devils-advocate/SKILL.md) uses this pattern to generate 5–7 critical challenges instead of bland affirmation.
- [`plan-reviewer`](../agents/plan-reviewer.md) (agent invoked by `/review-plan`) bakes the critic stance into the agent definition.

**Stronger alternative:** when reviewing Claude's own work, prefer an *agent* over a critic-stance skill — fresh context avoids self-bias. See [`.claude/rules/skill-design-patterns.md`](skill-design-patterns.md) §2.

### 1.4 Output Templates

Define the exact format of the skill's output inline. Do not let Claude decide how to structure results.

```markdown
### Output

```
PLAN REVIEW — [title]
Reviewing as: [expert role]

STRENGTHS
1. [Label] — [explanation]

WEAKNESSES
[Red] [Label] — [issue] → Fix: [recommendation]
[Yellow] [Label] — [issue] → Fix: [recommendation]

VERDICT
APPROVE / REVISE — [rationale]
```
```

**Use when:** any skill that produces a report, table, or audit row. Format consistency makes results comparable across runs and across days.

**Examples in this repo:**
- [`/audit-citations`](../skills/audit-citations/SKILL.md) — defines the consolidated-report block (BIB_FAIL / Substantive MISMATCH / AMBIGUOUS / INACCESSIBLE / Orphaned log rows / Adversarial dissents) verbatim.
- [`citation-audit-log.md`](citation-audit-log.md) — defines the 10-column schema that `/verify-citations` and `/audit-citations` both write to.
- [`fact-audit-log.md`](fact-audit-log.md) — defines the 8-column schema for non-cite facts.

**Adopt where missing:** `/research-ideation` and `/interview-me` produce free-form output that is hard to compare across runs. Worth tightening when next revised.

### 1.5 Iteration Gate

After producing a draft / proposal / set of changes, explicitly ask whether to apply, refine, or dismiss.

```markdown
After presenting the review, ask:

> "Apply these revisions? Or provide feedback to refine further."

User can:
- **Accept** — apply changes
- **Give feedback** — loop back with adjustments
- **Dismiss** — end without changes
```

**Use when:** the skill proposes changes the user should review before they take effect.

**Examples in this repo:**
- [`/audit-citations`](../skills/audit-citations/SKILL.md) Step 7 ("Wait for user direction on critical verdicts") is an iteration gate.
- [`/deep-audit`](../skills/deep-audit/SKILL.md) presents findings before applying fixes (gate); auto-fix only with explicit override.

**Adopt where missing:** `/research-ideation` (after generating ideas, ask "deepen any of these?"), `/create-slides` (after drafting frames, ask "regenerate any?").

### 1.6 Depth Calibration

Let the user request more or less thoroughness without forking the skill.

| Level | Behavior | Default? |
|---|---|---|
| `depth:light` | format only, no extras | Yes |
| `depth:standard` | format + assumptions + rationale | No |
| `depth:deep` | full research + compare + verify | No |

**Use when:** the skill can do a fast pass or a slow careful pass and the right choice depends on stakes.

**Adopt where missing:** `/lit-review` (light = abstract-only sweep; deep = full-paper reads), `/review-plan` (light = 6-dimension scorecard; deep = web-research best-practices comparison), `/audit-citations` (light = bib-only; deep = full-paper substantive verification).

### 1.7 Graceful Degradation

When a tool, MCP, or input file is missing, explain what is unavailable and proceed with what is possible. Never block on a missing optional source.

```markdown
## Error Handling

- **WebSearch unavailable:** note in the report; fall back to local
  literature folders only.
- **Specified PDF not found at the given path:** prompt the user
  once for the correct path; if still missing, mark the row
  INACCESSIBLE and continue with the rest.
- **Stata not installed:** edit-only mode; emit the `.do` file and
  the run instruction, do not attempt execution.
```

**Use when:** the skill depends on optional tools or files. The user should never hit a dead end because one component is missing.

**Examples in this repo:**
- [`/audit-citations`](../skills/audit-citations/SKILL.md) marks INACCESSIBLE rows for papers the verifier could not retrieve, instead of blocking the whole audit.
- [`citation-verifier`](../agents/citation-verifier.md) returns INACCESSIBLE rather than failing when a PDF is paywalled.

**Adopt where missing:** any skill that lists "required" inputs — convert most of them to "expected, with graceful degradation" wherever the worst-case is "weaker output", not "incorrect output".

### 1.8 Domain Auto-Detection

Infer the right behavior from content rather than requiring an explicit flag.

```markdown
Infer the domain from the content of the target file:

| Signals in content | Persona / behavior |
|---|---|
| "regression", "RCT", "DiD", "event study" | Use econometrics-methodology persona |
| "narrative", "topic sentence", "voice" | Use prose-review persona |
| "skill", "agent", "MCP" | Use skill-engineering persona |
```

**Use when:** the skill works across multiple distinct domains and explicit flags would be redundant with content cues.

**Examples in this repo:**
- [`/review-paper`](../skills/review-paper/SKILL.md) implicitly routes to `paper-reviewer` (prose) and optionally to `domain-reviewer` (substance). The auto-detection could be made more explicit.

---

## 2. Agents vs skills — when each one fits

This is a separate but related design decision. The full rule lives in [chrisblattman/claudeblattman / docs/system/agents-vs-skills.md](https://github.com/chrisblattman/claudeblattman/blob/main/docs/system/agents-vs-skills.md); the short version:

| Dimension | Skill | Agent |
|---|---|---|
| Context | Main conversation; full history | Fresh context; no prior conversation |
| User interaction | Can ask, show drafts, get feedback | Returns one result when done |
| Memory | Sees everything discussed | Sees only what you explicitly pass |
| Bias | Influenced by prior conversation (self-bias) | Fresh perspective |
| Speed | Instant | Slower (new process) |

**Rule of thumb:** if you are asking Claude to *critique* something it helped *create*, use an agent. Skills are for workflows; agents are for fresh-eyes evaluation, parallelism, or context isolation.

This repo already does this well: `/verify-citations` and `/audit-citations` are skills (workflows with user direction), but the per-cite reading is delegated to the `citation-verifier` agent (fresh-context evaluation). Maintain that split.

---

## 3. Quality checklist — apply before shipping

A new or revised skill is shippable when every box below is checked.

### 3.1 Frontmatter and structure

- [ ] `name` is kebab-case
- [ ] `description` includes WHAT it does, WHEN it triggers, and key capabilities — under 1024 chars (Claude pre-loads only this; it is the trigger mechanism)
- [ ] `argument-hint` describes the expected argument shape
- [ ] `allowed-tools` is the minimum set the skill actually needs (broader = larger blast radius)
- [ ] No XML angle brackets in the frontmatter values
- [ ] Skill body under ~5,000 words (move overflow to `references/` and link)
- [ ] Critical instructions appear in the first 500 words (Claude may not read the bottom of long skills carefully)

### 3.2 Behavior

- [ ] Zero-argument case is sensible (or fails with a one-line `Usage:` hint)
- [ ] Output format is specified in the skill body (not left to Claude)
- [ ] Errors are handled (missing files, missing MCP, empty input) — see §1.7
- [ ] The skill does one thing well, not three poorly
- [ ] Pre-approved tools declared at the top (avoids permission prompts mid-flow)
- [ ] State files (if any) live in `.claude/state/` with a `schema_version` field and a prune rule

### 3.3 Author hygiene

- [ ] Version header on the first or second line: `*v1.0 — 2026-05-24 — initial release*` — overwrite, do not append
- [ ] Arguments documented in a single block users can scan
- [ ] Reference files (long content moved out of the skill body) linked relatively
- [ ] Cross-references to related skills and rules at the bottom
- [ ] Tested against a real task — not just the happy path

---

## 4. Prefix-stability rules (caching-aware skill design)

Claude Code's harness is built on prefix-matching cache. Five rules protect that cache.

1. **Static content first, dynamic content last** — in the skill body, put fixed instructions before any content that varies between invocations.
2. **Never add/remove tools mid-session** — declare `allowed-tools` at the top; spawn subagents instead of mutating the tool set.
3. **Never switch models mid-session** — for cheaper handoffs, spawn a subagent on the cheaper model (e.g., Haiku for triage) rather than switching the main model.
4. **Use system-reminder messages for updates** — not changes to the system prompt.
5. **Treat cache breaks as incidents** — when a skill suddenly gets slower or more expensive without behavior change, the first suspect is a cache-break introduced by an author change.

Most of our current skills are short enough that the cache impact is small, but the rules apply at any size.

---

## 5. The development lifecycle

When the temptation is to write a skill, walk through this first.

1. **Notice the pattern** — what do you do repeatedly? Prompts you type more than twice; multi-step flows you walk Claude through manually; tasks where you always provide the same constraints.
2. **Do it manually first** — for at least three real instances. The friction points you hit in the manual runs are the things the skill should automate.
3. **Draft the skill** — applying the patterns in §1, the checklist in §3.
4. **Test against a real task** — not the happy path, the messy one.
5. **Save the skill** — and add a row to [CLAUDE.md](../../CLAUDE.md) so it is discoverable.
6. **Iterate** — every new instance reveals a missing case or an over-engineering. Adjust.

---

## 6. Related rules

- [`.claude/rules/quality-gates.md`](quality-gates.md) — shipping bars (80 / 90 / 95) for any artefact, including skill quality.
- [`.claude/rules/skill-telemetry.md`](skill-telemetry.md) — opt-in performance logging convention for skill invocations.
- [`.claude/rules/tool-limitations.md`](tool-limitations.md) — when a skill should hand off to a different tool rather than struggle.
- [`.claude/rules/claim-discipline.md`](claim-discipline.md) — claim-posture rules that apply *within* a skill's output prose.
- [`.claude/rules/prose-clarity.md`](prose-clarity.md) — paragraph-level discipline that applies to skill-authored prose.
