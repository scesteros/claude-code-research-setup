---
name: deep-audit
description: |
  Deep consistency audit of the repository infrastructure.
  Launches parallel agents to find code bugs, path mismatches,
  cross-document inconsistencies, and convention violations.
  Presents findings before applying fixes (gate); auto-fix only with explicit override.
  Use when: after broad changes, before releases, or when user says
  "audit", "find inconsistencies", "check everything".
argument-hint: "[autofix to skip the review gate (use with care)]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
---

# /deep-audit — Repository Infrastructure Audit

Run a comprehensive consistency audit across the repository, fix issues, and loop until clean.

## When to Use

- After broad changes (new analysis files, scraper modifications)
- Before major commits
- When user asks to "audit", "find inconsistencies", "check everything"

## Workflow

### PHASE 1: Launch Parallel Audit Checks

#### Check 1: CLAUDE.md Accuracy
- Folder structure matches actual repo
- Skills table matches actual skill directories
- Analysis pipeline state is current
- All referenced paths exist

#### Check 2: Hook & Settings Integrity
- All hooks referenced in settings.json exist on disk
- Python hooks have fail-open pattern (try/except with sys.exit(0))
- `from __future__ import annotations` present
- Hook paths use correct Python command for platform

#### Check 3: Rules & Agents Consistency
- Valid YAML frontmatter in all rule/agent files
- Rule `paths:` reference existing directories
- No contradictions between rules
- Agent tool lists are sensible

#### Check 4: Code Conventions Compliance
- Sample .do files follow stata-code-conventions.md
- Python scripts follow python-scraping-conventions.md
- Master .do file include statements match actual filenames

### PHASE 1.5: Present findings (gate)

Antes de aplicar fixes, presentar la lista completa de findings clasificada por severity y check origen. Esperar la decisión del usuario. Saltear esta fase solo si el usuario pasó `autofix` en `$ARGUMENTS`.

**Formato a mostrar:**

```
────────────────────
AUDIT FINDINGS
────────────────────
Total: [N] issues found across [4] checks

| # | Severity | Check | File:Line | Issue | Fix sugerido |
|---|---|---|---|---|---|
| 1 | Critical | Hooks | settings.json:42 | hook script no existe | Crear .claude/hooks/X.py o quitar referencia |
| 2 | Major | Rules | rules/X.md:15 | path no existe | Actualizar a path correcto |
| 3 | Minor | CLAUDE.md | CLAUDE.md:88 | skill listada no existe en .claude/skills/ | Quitar de la tabla |
| ... | | | | | |
```

**Pregunta al usuario:**

> "¿Cómo procedo con [N] findings? (FIX-ALL / FIX-CRITICAL-ONLY / SELECT [#1,#3,#5] / DISMISS [solo guardar el report])"

Acción según respuesta:
- **FIX-ALL** → continuar a Phase 2 con todos los findings.
- **FIX-CRITICAL-ONLY** → continuar a Phase 2 solo con los Critical; dejar el resto en el report como nota.
- **SELECT [list]** → continuar a Phase 2 solo con los seleccionados.
- **DISMISS** → guardar el report en `quality_reports/audit_[date].md` y cerrar sin tocar archivos.

### PHASE 2: Triage & Fix (post-gate)

Aplicar los fixes según la decisión del usuario en Phase 1.5:

- **Genuine bug autorizado a fix**: aplicar el cambio.
- **False alarm**: documentar en el report por qué fue descartado.
- **Fix no autorizado**: dejar como nota pendiente en el report; no tocar el archivo.

### PHASE 3: Re-verify

After fixing, run checks again. Max 5 loops.

## Output

```markdown
## Audit Results

### Issues Found: X genuine, Y false alarms

| # | Severity | File | Issue | Status |
|---|----------|------|-------|--------|
| 1 | Critical | file:line | Description | Fixed |

### Result: [CLEAN | N issues remaining]
```
