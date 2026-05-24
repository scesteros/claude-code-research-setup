---
name: learn
description: |
  Extract reusable knowledge from the current session into a persistent skill.
  Use when you discover something non-obvious, create a workaround, or develop
  a multi-step workflow that future sessions would benefit from.
argument-hint: "[skill-name (kebab-case)]"
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep"]
---

# /learn — Skill Extraction Workflow

Extract non-obvious discoveries into reusable skills that persist across sessions.

## When to Use This Skill

Invoke `/learn` when you encounter:

- **Non-obvious debugging** — Investigation that took significant effort
- **Misleading errors** — Error message was wrong, found the real cause
- **Workarounds** — Found a limitation with a creative solution
- **Repeatable workflows** — Multi-step task you'd do again
- **Stata/Python gotchas** — Package quirks, version differences, data issues

## Workflow

### PHASE 1: Evaluate

1. "What did I just learn that wasn't obvious before starting?"
2. "Would future-me benefit from this being documented?"
3. "Is this a multi-step workflow I'd repeat?"

**Continue only if YES to at least one.**

### PHASE 2: Check Existing Skills

```bash
ls .claude/skills/ 2>/dev/null
grep -r -i "KEYWORD" .claude/skills/ 2>/dev/null
```

### PHASE 3: Create Skill

Create at `.claude/skills/[skill-name]/SKILL.md` with:
- Problem description
- Trigger conditions
- Step-by-step solution
- Verification steps
- Example

### PHASE 4: Quality Gates

- [ ] Description has specific trigger conditions
- [ ] Solution was verified to work
- [ ] Content is actionable and reusable
- [ ] No sensitive information

## Output

```
Skill created: .claude/skills/[name]/SKILL.md
  Trigger: [when to use]
  Problem: [what it solves]
```
