# claude-code-research-setup

A working [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) configuration for empirical economics research — the agents, skills, hooks, and rules I use every day.

This is the lightly-genericized, ready-to-fork version of the setup I run across my active research projects. The most-developed working example is [`narcos-ba`](https://github.com/scesteros) — a study of anti-narcotics police raids and crime in Buenos Aires informal settlements — so most of the concrete examples below are drawn from it. Drop the `.claude/` directory into your own repo, adapt the placeholders, and you have an opinionated starting point — instead of a blank `.claude/` slate.

> **Use as a template:** click **"Use this template"** above to spin up your own copy without forking. Adapt to your project (paths, conventions, examples) and commit forward.

---

## What's inside

```
.claude/
├── settings.json          Permissions + hook routing (entry point)
├── WORKFLOW_QUICK_REF.md  One-page workflow overview
├── agents/                14 subagents — invoked via Task tool or by name
├── skills/                24 slash-commands — invoked with /<skill-name>
├── hooks/                 7 lifecycle scripts (Python + shell)
├── rules/                 25 on-demand rule files — referenced by other components
└── scripts/               Helper Python scripts called by hooks/skills
```

### Agents (`.claude/agents/`)

Subagents that run in fresh context — useful for review tasks where you want an independent perspective with no defensive attachment to prior choices.

| Agent | What it does |
|---|---|
| `paper-reviewer` | Fresh-context review of academic prose (argument structure, evidence integration, clarity) |
| `domain-reviewer` | Substantive review by a "top-journal referee" persona — identification, specification, causal validity |
| `plan-reviewer` | Tough external review of plans before execution |
| `stata-reviewer` | Senior-Stata-developer review of `.do` files |
| `proofreader` | Grammar/typos/LaTeX issues on Beamer slides |
| `slide-reviewer` | Slide-deck content + narrative review |
| `beamer-builder` | Builds Beamer slides from analysis outputs |
| `verifier` | Verification of research code outputs |
| `cross-doc-checker` | Cross-document consistency between paper, slides, and outputs |
| `source-fact-checker` | Verifies prose claims against source documents |
| `citation-adversary` | Adversarial reviewer of citations (lit-review claims) |
| `citation-verifier` | Verifies that citations support the claims made |
| `council-critic` | Adoption-focused critic in a fresh context |
| `seminar-discussant` | Channels a seminar discussant persona for talk-prep feedback |

### Skills (`.claude/skills/`)

Slash-commands invoked manually with `/skill-name` (or with arguments via `/skill-name <arg>`).

| Skill | Purpose |
|---|---|
| `audit-citations` | Audit every citation in a paper draft |
| `claim-evidence-map` | Map each claim in the prose to its supporting evidence |
| `commit` | Structured commit message workflow |
| `compile-latex` | Compile a LaTeX project with diagnostics |
| `context-status` | Quick status report on the current Claude Code context window |
| `council` | Multi-agent council review of a target document |
| `create-slides` | Build new Beamer slides from spec |
| `cross-doc-audit` | Audit consistency between two or more documents |
| `data-analysis` | Run a structured data-analysis pass |
| `deep-audit` | Deep-pass audit on a target file or section |
| `devils-advocate` | Devil's-advocate critique of an argument or design |
| `format-table-for-slides` | Reformat a LaTeX paper-table into a slide-table |
| `interview-me` | Interview the user to extract structured information |
| `learn` | Build a knowledge-base note from a source |
| `lit-review` | Structured literature-review pass on a topic |
| `prompt-master` | Vendored from [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) — meta-skill for crafting better prompts (see [`PROVENANCE.md`](.claude/skills/prompt-master/PROVENANCE.md)) |
| `research-ideation` | Structured ideation pass for a new research project |
| `review-paper` | Self-invoked paper review |
| `review-plan` | Self-invoked plan review |
| `seminar` | Seminar-feedback workflow |
| `source-audit` | Audit prose claims against source documents |
| `stata-regression` | Structured Stata regression workflow |
| `update-slides` | Update existing Beamer slides |
| `verify-citations` | Verify a citation against the original source |

### Hooks (`.claude/hooks/`)

Lifecycle scripts wired into `settings.json` — these fire automatically.

| Hook | Trigger | What it does |
|---|---|---|
| `notify.sh` | `Notification` | OS notification when Claude needs attention |
| `protect-files.sh` | `PreToolUse:Edit\|Write` | Blocks edits to designated protected files |
| `pre-compact.py` | `PreCompact` | Saves session state before context compaction |
| `post-compact-restore.py` | `SessionStart:compact\|resume` | Restores session state after compaction/resume |
| `context-monitor.py` | `PostToolUse:Bash\|Task` | Tracks context usage after expensive tool calls |
| `verify-reminder.py` | `PostToolUse:Write\|Edit` | Prompts a verification step after writes |
| `log-reminder.py` | `Stop` | Reminds to log session decisions at end-of-session |

### Rules (`.claude/rules/`)

On-demand reference files — not auto-loaded into context, but referenced by agents/skills via `@.claude/rules/<file>.md` or invoked explicitly. Covers:

- **Writing discipline:** `claim-discipline`, `paraphrase-discipline`, `prose-clarity`
- **Citation integrity:** `citation-integrity`, `citation-audit-log`, `fact-audit-log`
- **Verification:** `verification-protocol`, `quality-gates`, `replication-protocol`
- **Domain-specific quality:** `did-event-study-checks`, `stata-code-conventions`, `python-scraping-conventions`, `latex-table-conventions`, `beamer-slides-conventions`
- **Workflow:** `plan-first-workflow`, `meta-governance`, `orchestrator-protocol`, `exploration-fast-track`, `exploration-folder-protocol`
- **Logging / archive:** `session-logging`, `research-archive-protocol`, `knowledge-base-template`
- **Skill design:** `skill-design-patterns`, `skill-telemetry`
- **Tool boundaries:** `tool-limitations`

---

## Quickstart

### 1. Use as a template

Click **"Use this template"** at the top of this repo's GitHub page (or fork it the old way).

Then clone your new repo into the directory where your research project lives:

```bash
git clone https://github.com/<you>/<your-new-repo>.git my-research-project
cd my-research-project
```

If you already have a research repo, copy the `.claude/` directory into it instead:

```bash
cp -r path/to/claude-code-research-setup/.claude my-research-project/
```

### 2. Edit a handful of things first

Before you start working, adapt these to your project:

1. **`.claude/settings.json`** — review the `permissions.allow` list. Add/remove commands to fit your stack (Stata, R, Python, etc.). Leave the `hooks` block alone unless you know what you're changing.
2. **`.claude/WORKFLOW_QUICK_REF.md`** — replace the placeholder Stata/R/Python conventions with whatever yours look like.
3. **`.claude/rules/did-event-study-checks.md`** (and other `*-conventions.md` rules) — adapt path placeholders like `<pipeline-output-path>/` to your real paths.
4. **`.claude/rules/research-archive-protocol.md`** — if you don't keep a central research archive, delete this rule.
5. **CLAUDE.md** at your repo root — write a short project context note. The agents and skills assume some grounding ("what is this repo, what's the research question, what's the stack") that lives best in `CLAUDE.md`.

### 3. Try it out

Open Claude Code in your project and run one of the skills:

```
/context-status
/lit-review treatment displacement effects in urban policing
/council .claude/agents/paper-reviewer.md
```

Or invoke an agent directly via the Task tool — see the agent file for the role it plays.

---

## Philosophy

The setup is opinionated in a few ways worth flagging upfront:

- **Plan-first.** Multi-file or non-trivial changes go through a plan that the user approves before execution. See `rules/plan-first-workflow.md`.
- **Fresh-context review.** Several agents (`paper-reviewer`, `domain-reviewer`, `plan-reviewer`, `council-critic`, `seminar-discussant`) are designed to arrive without history — they don't see the iteration trail, which is the point.
- **Quality gates with a score threshold.** Production work targets ≥ 80/100; exploration mode relaxes to ≥ 60/100. See `rules/quality-gates.md`.
- **Edit-only on user-run code.** Claude writes/edits `.do`, `.py`, `.R` files; the user runs the pipeline manually. Avoids the "I ran it and it broke" loop on long-running analyses.
- **Verification reminders fire on writes.** The `verify-reminder.py` hook gently nudges toward verification after every `Write`/`Edit`. Annoying at first, load-bearing in practice.
- **Citation discipline is its own subsystem.** Several skills, agents, and rules form a coordinated citation-integrity layer. It ships *dormant* (most repos don't have a paper draft yet) — invoke manually when you start writing.

---

## About the examples

Many rules, skills, and agents contain concrete illustrative examples drawn from the running example project — a study of anti-narcotics police raids and crime in informal settlements (*villas*) in Buenos Aires, using event-study DiD on a scraped panel of raid events. You will see references to *villas*, *raids*, *CABA agencies*, *staggered DiD*, etc.

These are intentionally preserved as templates rather than rewritten into sterile placeholders. They show what good rules, fact-audit logs, and review prompts look like applied to a real research project — concrete enough to learn from. Adapt them to your own context: replace the substantive examples with your own treatments, units, and institutional setting.

If you'd prefer fully sanitized versions, the substitution patterns to look for are:
- `villas`, `raids`, `CABA`, `Buenos Aires`, `SEDRONAR`, etc. → your own substantive examples
- `<pipeline-output-path>/`, `<pipeline-source-path>/` → your real data paths

---

## What you'll need beyond this repo

- **Claude Code** installed. See [Claude Code docs](https://docs.claude.com/en/docs/claude-code/overview).
- **Python 3.10+** for the hooks (`pre-compact.py`, `context-monitor.py`, etc.). Standard library only — no `pip install` required.
- **A research codebase** to point this at. The setup assumes a structured project: `analysis/`, `output/`, `paper/`, `presentation/`, `literature/`, etc.

---

## Credits and license

Released under the [MIT license](LICENSE).

Built and maintained by [Santiago Rodrigo Cesteros](https://scesteros.github.io). If you build on this and would like to share back, issues and pull requests are welcome.

### Starting points

This setup did not start from scratch. Two earlier public setups by economists in the community served as the initial scaffolding, before being adapted, extended, and pushed in different directions to fit my own research workflow:

- **[Chris Blattman](https://claudeblattman.com/)** — whose public Claude Code setup was a major reference for how to structure a research-oriented `.claude/` directory. The `tool-limitations` rule here is adapted from [chrisblattman/claudeblattman](https://github.com/chrisblattman/claudeblattman) (MIT).
- **[Pedro H. C. Sant'Anna](https://psantanna.com/claude-code-my-workflow/workflow-guide.html)** — whose workflow guide shaped the plan-first / verify-after conventions and the framing of the overall loop.

If you are building your own setup from scratch, both are worth reading directly — they explain the *why* behind many of the conventions you will find here.

### Vendored components

The `prompt-master` skill is vendored from [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) (MIT) — see [`.claude/skills/prompt-master/PROVENANCE.md`](.claude/skills/prompt-master/PROVENANCE.md) for the modification log.
