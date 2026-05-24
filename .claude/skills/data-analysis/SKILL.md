---
name: data-analysis
description: End-to-end data analysis workflow for Stata and Python. Helps design analysis specifications, write .do files, and produce publication-ready output. Inserts a confirmation gate between spec design and code writing.
argument-hint: "[analysis goal or dataset description] [noconfirm to skip the spec gate]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
---

# Data Analysis Workflow

Design and implement an end-to-end data analysis in Stata (primary) or Python (supporting).

**Input:** `$ARGUMENTS` — an analysis goal (e.g., "estimate effect of raids on robbery at weekly frequency") or a dataset description.

---

## Constraints

- **Follow Stata conventions** in `.claude/rules/stata-code-conventions.md`
- **Follow DiD checks** in `.claude/rules/did-event-study-checks.md`
- **Claude edits .do files only** — user runs Stata manually
- **All outputs** go to `$output/` subdirectories (figures/, tables/, maps/, logs/)
- **Publication-ready figures** — scheme s1color, proper labels, correct dimensions

---

## Workflow Phases

### Phase 1: Understanding the Goal

1. Read `$ARGUMENTS` and understand what analysis is requested
2. Check existing .do files in `analysis/` for related specifications
3. Read `0_CABA_Master.do` for global definitions and pipeline structure
4. Identify which data files are needed and whether they exist

### Phase 2: Design the Specification

1. Define the estimating equation explicitly
2. Specify: outcome variable, treatment variable, fixed effects, clustering, sample
3. Document the identification assumption
4. Plan pre-trend tests and robustness checks

### Phase 2.5: Confirm the Specification (gate)

Antes de escribir código, presentar al usuario la spec completa en formato estructurado y esperar APPROVE / REVISE / DISMISS. Saltea esta fase solo si el usuario pasó `noconfirm` en `$ARGUMENTS`.

**Formato a mostrar:**

```
────────────────────
SPECIFICATION REVIEW
────────────────────
Goal:                    [from $ARGUMENTS]
Outcome variable:        [name + unit + transformation if any]
Treatment variable:      [name + definition + timing]
Sample:                  [units, time period, restrictions]
Estimating equation:     [in math notation, e.g.,
                         y_{it} = α_i + γ_t + β · D_{it} + ε_{it}]
Fixed effects:           [unit + time, or barrio×month, etc.]
Standard errors:         [clustering level + rationale]
Identification:          [parallel trends / exogenous timing /
                         IV exclusion / discontinuity]
Pre-trend tests:         [list specific tests]
Robustness checks:       [list specific checks]
Output destinations:     [$output/figures/X, $output/tables/Y]
Dependencies:            [data files needed, packages required]
Open uncertainties:      [things I'd want to confirm before coding]
```

**Pregunta al usuario:**

> "Apruebo esta spec antes de escribir el `.do`? (APPROVE / REVISE [+ feedback] / DISMISS)"

Acción según respuesta:
- **APPROVE** → continuar a Phase 3.
- **REVISE [feedback]** → loop a Phase 2 incorporando los cambios pedidos, re-presentar la spec.
- **DISMISS** → no escribir código; cerrar la skill con el spec guardado en una nota para el usuario.

Tras 2 rounds de REVISE sobre la misma spec, advertir: "Ya iteramos [N] veces sobre la spec. ¿Querés que arranque a escribir y ajustamos sobre código real, o sigo refinando spec?"

### Phase 3: Write the .do File

1. Create or edit the appropriate .do file in `analysis/`
2. Follow project header format and section conventions
3. Use globals for all paths
4. Include clear comments on each specification choice
5. Generate publication-ready output (esttab for tables, graph export for figures)

### Phase 4: Verification (Static)

1. Review .do file for syntax errors
2. Verify all globals and file paths are correct
3. Check merge logic and sample restrictions
4. Run the stata-reviewer agent on the generated code
5. Report what the user needs to verify by running the file

---

## Important

- **Edit-only.** Claude writes .do files; user runs Stata.
- **Match existing style.** New .do files should follow the conventions in existing analysis files.
- **Document everything.** Every estimation choice should have a comment explaining why.
- **Think like a referee.** Every specification should anticipate identification concerns.
