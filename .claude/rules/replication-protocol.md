---
paths:
  - "replication_packages/**"
  - "analysis/**/*.do"
---

# Replication-First Protocol

**Core principle:** Replicate original results BEFORE extending.

---

## Phase 1: Inventory & Baseline

Before modifying any replication code:

- [ ] Read the replication package README
- [ ] Inventory: language, data files, scripts, outputs
- [ ] Record gold standard numbers from the paper:

```markdown
## Replication Targets: [Paper Author (Year)]

| Target | Table/Figure | Value | SE/CI | Notes |
|--------|-------------|-------|-------|-------|
| Main effect | Table 2, Col 3 | -1.632 | (0.584) | Primary specification |
```

- [ ] Store targets in `quality_reports/replication_targets_[paper].md`

---

## Phase 2: Translate & Execute

- [ ] Follow project code conventions for all new code
- [ ] Translate line-by-line initially -- don't "improve" during replication
- [ ] Match original specification exactly (covariates, sample, clustering)
- [ ] Document any necessary adaptations (different Stata version, package updates)

### Common Stata Replication Pitfalls

| Original | Adaptation | Trap |
|----------|-----------|------|
| Old `reg` syntax | `reghdfe` for FE | Check demeaning method matches |
| `cluster()` | Verify same clustering level | Different default df adjustments |
| Specific data vintage | Current data version | Sample composition may differ |
| Older package versions | Current versions | Algorithm changes across versions |

---

## Phase 3: Verify Match

### Tolerance Thresholds

| Type | Tolerance | Rationale |
|------|-----------|-----------|
| Integers (N, counts) | Exact match | No reason for difference |
| Point estimates | < 0.01 | Rounding in paper display |
| Standard errors | < 0.05 | Clustering/bootstrap variation |
| P-values | Same significance level | Exact p may differ slightly |

### If Mismatch

**Do NOT proceed to extensions.** Isolate which step introduces the difference, document the investigation.

---

## Phase 4: Only Then Extend

After replication is verified:
- [ ] Commit replication script: "Replicate [Paper] Table X -- all targets match"
- [ ] Now extend with project-specific modifications
- [ ] Each extension builds on the verified baseline
