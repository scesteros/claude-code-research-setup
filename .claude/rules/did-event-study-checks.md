---
paths:
  - "analysis/**/*.do"
  - "output/**"
---

# DiD & Event Study Quality Checks

**Domain-specific quality checks for causal inference in this project.**

---

## Treatment Variable Construction

- [ ] Treatment events sourced from verified scraping output (`<pipeline-output-path>/`)
- [ ] Events deduplicated (check for same event reported by multiple sources)
- [ ] Geographic matching documented (how raids are assigned to spatial units)
- [ ] Treatment timing is precise (date, not just month/year)
- [ ] Treatment intensity or type is captured if relevant

## Standard DiD Checks

- [ ] Treatment and control groups clearly defined
- [ ] Pre-treatment period balance: compare means of key outcomes
- [ ] Common support: treatment and control overlap in observables
- [ ] Treatment is not anticipated (check for pre-trends)
- [ ] Appropriate clustering of standard errors (spatial unit level)
- [ ] Multiple time frequencies tested (daily, weekly, monthly)

## Event Study Design Checks

- [ ] Event window is justified (how many pre/post periods?)
- [ ] Reference period explicitly chosen and documented
- [ ] Pre-trend coefficients are insignificant (parallel trends)
- [ ] Post-treatment dynamics are interpreted correctly
- [ ] Stacking approach handles overlapping treatment windows
- [ ] Pure control group construction is documented (for stacked DiD)

## Robustness Checks

- [ ] Alternative treatment definitions tested
- [ ] Different geographic granularity tested
- [ ] Different crime categories tested separately
- [ ] Sensitivity to event window length
- [ ] Heterogeneous effects by settlement size/type
- [ ] Callaway-Sant'Anna or other robust DiD estimator as alternative

## Figure Standards for Event Studies

- [ ] Clear x-axis: relative time to treatment
- [ ] Reference period marked (vertical line or highlighted)
- [ ] Confidence intervals shown (95%)
- [ ] Point estimates clearly visible
- [ ] Treatment date marked
- [ ] Publication-ready formatting (scheme s1color, proper labels)

## Common Pitfalls in This Project

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Multiple raids in same area | Contaminated control group | Restrict to first raid or use stacked design |
| Spillover to adjacent areas | Biased treatment effects | Test with spatial buffers |
| Seasonal crime patterns | Confound treatment effects | Include time fixed effects, test with placebo dates |
| Media reporting bias | Selective treatment measurement | Cross-validate with official sources |
| Staggered treatment timing | TWFE bias | Use Callaway-Sant'Anna, stacked DiD, or de Chaisemartin-D'Haultfoeuille |
