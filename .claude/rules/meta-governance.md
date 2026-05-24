# Meta-Governance: Dogfooding Principles

**This project follows the Claude Code academic workflow. We practice what we preach.**

## Non-Negotiable Principles

### Plan-First Workflow
- Enter plan mode for non-trivial tasks (>3 files, >1 hour, multi-step)
- Save plans to `quality_reports/plans/YYYY-MM-DD_description.md`
- Don't skip planning for "quick fixes" that could turn into multi-hour tasks

### Quality Gates
- Nothing ships below 80/100
- Run quality checks before commits
- User can override with justification

### Documentation Standards
- Update MEMORY.md with `[LEARN]` entries after sessions
- Keep session logs current during substantial work
- Save active plans to disk before compression

### Context Survival
- Plans, specs, and session logs live on disk (not just in conversation)
- Pre-compact hook captures state automatically
- Post-compact hook restores context

## Amendment Process

When deviating from a principle, clarify:
- "Amending permanently" (the principle changes)
- "Overriding for this task" (one-time exception)
