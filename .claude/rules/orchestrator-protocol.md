# Orchestrator Protocol: Contractor Mode

**After a plan is approved, the orchestrator takes over autonomously.**

## The Loop

```
Plan approved
  │
  Step 0 (opcional): /review-plan en fresh context
  │         Trigger: plan complejo (>3 archivos, >1h), spec econométrica,
  │                  cambio infra grande, o usuario pidió "stress-test".
  │         Si verdict = REVISE: aplicar revisiones al plan, re-aprobar, retry.
  │         Skip cuando el plan es trivial o ya iteró con el usuario.
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Check outputs exist, results reasonable
  │         If verification fails → fix → re-verify
  │
  Step 3: REVIEW — Run review agents (by file type)
  │
  Step 4: FIX — Apply fixes (critical → major → minor)
  │
  Step 5: RE-VERIFY — Confirm fixes are clean
  │
  Step 6: SCORE — Apply quality-gates rubric
  │
  └── Score >= threshold?
        YES → Present summary to user
        NO  → Loop back to Step 3 (max 5 rounds)
              After max rounds → present with remaining issues
```

## Limits

- **Main loop:** max 5 review-fix rounds
- **Verification retries:** max 2 attempts
- Never loop indefinitely

## "Just Do It" Mode

When user says "just do it" / "handle it":
- Skip final approval pause
- Auto-commit if score >= 80
- Still run the full verify-review-fix loop
- Still present the summary
