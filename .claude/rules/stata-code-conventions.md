---
paths:
  - "**/*.do"
  - "analysis/**"
---

# Stata Code Conventions

**Standard:** Publication-quality empirical economics code.

---

## 1. File Header

Every .do file must start with a header block matching the project style:

```stata
/* -----------------------------------------------------------------------------------------
[DESCRIPTIVE TITLE]
Creation date: DD/MM/YYYY
Last modification date: DD/MM/YYYY
Last modification person: [Name]

Do file notes:
1. [What this file does]
2. [Dependencies and inputs]
----------------------------------------------------------------------------------------- */
```

## 2. Setup Block

```stata
drop _all
clear all
set more off
set scheme s1color
```

## 3. Path Management

- All paths use globals defined in `0_Master.do`
- **Never** use hardcoded absolute paths in analysis files
- Standard globals: `$path`, `$data`, `$do`, `$data_dir`, `$output`, `$events`
- Reference files as: `"$data_dir/filename.dta"`, `"$output/figures/filename.png"`

## 4. Package Management

- Package installation controlled by `install_packages` local in master file
- Key packages: `did_multiplegt_dyn`, `csdid`, `eventdd`, `reghdfe`, `ftools`, `coefplot`, `stackedev`, `event_plot`, `xtevent`, `pretrends`

## 5. Naming Conventions

- Variables: `snake_case` (e.g., `crime_count`, `post_treatment`)
- Locals/globals: descriptive names, no single letters except loop indices
- Temporary variables: prefix with `_tmp_` or use `tempvar`
- Generated variables: document what they represent

## 6. Section Organization

Use numbered sections with clear dividers:

```stata
/*==============================================================================
                        1: Data Creation
==============================================================================*/

/* --------------------------------------------------------------------------
   1.1: Load and merge crime data
-------------------------------------------------------------------------- */
```

## 7. Comments

- Explain **why**, not what
- Document non-obvious merge decisions, sample restrictions, variable definitions
- Label key estimation outputs (what specification, what sample)

## 8. Output Standards

- Figures: publication-ready, `scheme s1color`, explicit dimensions
- Tables: include standard errors, significance stars, N, R-squared
- All outputs saved to `$output/` subdirectories (figures/, tables/, maps/, logs/)

## 9. DiD / Event Study Specific

- Document treatment definition clearly
- Label pre-period and post-period windows
- Include parallel trends tests where applicable
- Comment which estimator is used and why (TWFE vs. robust DiD)

## 10. Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Forgetting `drop _all` | Residual data in memory | Always start with `drop _all` |
| Wrong merge direction | Lost/duplicated observations | Check `_merge` variable |
| Not setting `scheme` | Inconsistent figure style | Set `scheme s1color` in setup |
| Hardcoded sample restrictions | Breaks with data updates | Use locals for cutoffs |
