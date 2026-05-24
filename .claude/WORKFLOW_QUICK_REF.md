# Workflow Quick Reference

**Model:** Contractor (you direct, Claude orchestrates)

---

## The Loop

```
Your instruction
    ↓
[PLAN] (if multi-file or unclear) → Show plan → Your approval
    ↓
[EXECUTE] Implement, verify, done
    ↓
[REPORT] Summary + what's ready
    ↓
Repeat
```

---

## I Ask You When

- **Design forks:** "Option A (fast) vs. Option B (robust). Which?"
- **Code ambiguity:** "Spec unclear on X. Assume Y?"
- **Identification concerns:** "This threatens parallel trends. Investigate?"
- **Scope question:** "Also refactor Y while here, or focus on X?"

---

## I Just Execute When

- Code fix is obvious (bug, pattern application)
- Verification (syntax checks, path validation)
- Documentation (logs, commits)
- Writing .do files per approved specification
- Deployment (after you approve, I ship automatically)

---

## Quality Gates (No Exceptions)

| Score | Action |
|-------|--------|
| >= 80 | Ready to commit |
| < 80  | Fix blocking issues |

---

## Non-Negotiables (adapt to your project)

- **Path convention:** project-specific globals/macros defined in a master script (e.g. Stata `$path`/`$data`/`$do`/`$output` in `0_Master.do`, R `here()` paths, etc.)
- **Figure standards:** publication-ready, consistent theme, proper labels
- **Edit-only:** Claude writes/edits source files; user runs the analysis pipeline manually
- **Tolerance thresholds:** Point estimates to display precision, observation counts exact match

---

## Preferences

**Visual:** Publication-ready — polished, no shortcuts, correct dimensions
**Reporting:** Structured, concise, rigorous
**Session logs:** Always (post-plan, incremental, end-of-session)
**Early sessions:** Check in more often so user learns the workflow

---

## Exploration Mode

For experimental work, use the **Fast-Track** workflow:
- Work in `explorations/` folder
- 60/100 quality threshold (vs. 80/100 for production)
- No plan needed — just a research value check
- See `.claude/rules/exploration-fast-track.md`

---

## Next Step

You provide task → I plan (if needed) → Your approval → Execute → Done.
