---
name: review-plan
description: Stress-test a plan with structured expert critique (6 dimensions) + optional web research on best practices. Use after writing a plan in plan mode, or on any plan file. Catches blind spots, missing steps, and wishful thinking before execution.
argument-hint: "[file:path | role:role | focus:dim | depth:quick/standard/deep | dryrun]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task", "WebSearch"]
---

# Review Plan

Stress-test un plan vía un agente de revisión en **fresh context**, opcionalmente fortificado con un research breve de best practices. Evita el self-bias del modelo que escribió el plan defendiéndolo. Inserta un control de calidad entre "plan aprobado" y "ejecución".

**Pre-approved tools:** `Task` (despacho de `plan-reviewer`), `WebSearch`, filesystem reads. Llamarlas directamente.

---

## Steps

### Step 0: Parse `$ARGUMENTS`

| Flag | Sintaxis | Default | Propósito |
|---|---|---|---|
| File path | `file:path` | Auto-detect | Localización explícita del plan |
| Expert role | `role:"..."` | Auto-detect | Override de la persona del agent |
| Focus area | `focus:dim` | All | Una dimensión en particular (e.g. `focus:feasibility`) |
| Depth | `depth:quick/standard/deep` | `standard` | Intensidad del web research |
| Quick | `quick` | Off | Atajo para `depth:quick` (skip web) |
| Dryrun | `dryrun` | Off | Mostrar el plan de revisión sin ejecutarlo |
| Help | `help` | — | Mostrar esta tabla y stop |

### Step 1: Localizar el plan

Tres-tier priority:

1. **Path explícito** — `file:path/to/plan.md`
2. **Plan-mode file** — `~/.claude/plans/*.md` (más reciente) si existe
3. **Project plans** — `quality_reports/plans/*.md` (más reciente, prioridad sobre plan-mode si ambos existen)
4. **Conversación** — escanear el contexto actual buscando un plan inline

Si ningún plan se encuentra:

> "No plan found. Usage: `/review-plan` (después de escribir un plan en `quality_reports/plans/`) o `/review-plan file:path/to/plan.md`"

Si el plan tiene <50 palabras: warning "El plan es inusualmente corto. Procediendo, pero la revisión va a ser limitada."

Leer el plan completo antes de continuar.

### Step 2: Asignar role al agent

Inferir el dominio del plan con keyword heuristics:

| Domain signals en el plan | Role asignado |
|---|---|
| `did`, `event study`, `parallel trends`, `csdid`, `staggered` | DiD methodologist |
| `scrap`, `python`, `selenium`, `requests`, `webscraping` | Data engineering specialist |
| `paper`, `manuscript`, `intro`, `referee`, `journal` | Academic writing specialist |
| `slide`, `beamer`, `presentation` | Academic presentation specialist |
| `skill`, `agent`, `hook`, `claude code`, `MCP` | AI engineering / skill design specialist |
| `proposal`, `grant`, `funder`, `budget` | Grant strategy specialist |
| Default | Strategic planning and implementation specialist |

Si `role:"..."` está en `$ARGUMENTS`, usar ese override.

Anunciar al usuario:

> **Reviewing as:** [role]. (Override con `role:"..."` si no encaja.)

Si `dryrun`: imprimir el plan de research (Step 3) y stop. No ejecutar.

### Step 3: Web research de best practices (opcional)

Construir queries:
- Query A: "[domain] best practices 2026"
- Query B: "[domain] common pitfalls" o "[domain] failure modes"
- Query C (`deep` only): "[specific technique] implementation guide"

| Depth | Web searches |
|---|---|
| `quick` | 0 (skip) |
| `standard` | 2 (A + B) |
| `deep` | 3 (A + B + C) |

Distillar resultados en 3-5 principios. Si web search falla o `quick`: continuar sin best-practice context, con nota "Best-practice research skipped/unavailable."

### Step 4: Dispatch `plan-reviewer` agent

Task tool:
- `subagent_type`: `plan-reviewer`
- `description`: "Plan review: [short title]"
- `prompt`: incluir:
  - Texto completo del plan (Step 1)
  - Role asignado (Step 2)
  - Focus area si se pasó (`focus:X`)
  - Best-practice principles (Step 3) si los hay

Esperar el output del agent.

### Step 5: Format and present

El agent ya devuelve output en formato estructurado (red/yellow/green + Verdict + Score). Tu job es:

1. Surface el report file path al usuario.
2. Resumen 3-5 líneas con: verdict (APPROVE/REVISE), # red flags, score, top action item.

### Step 6: Iteration gate

Después de presentar el review, preguntar:

> "Apply revisions? Or feedback to refine further?"

Opciones del usuario:
- **Accept** — usar las recomendaciones del review como base para revisar el plan (volver al plan original y editarlo).
- **Feedback** — loop a Step 4 con notas adicionales.
- **Dismiss** — cerrar sin cambios.

Tras 2 ciclos de revisión sobre el mismo plan, nota:

> "Este plan ya tuvo [N] rounds de review. Diminishing returns probable. Considerar implementar y iterar en práctica."

### Step 7: Telemetry (opt-in)

```bash
date +%Y-%m-%d | xargs -I{} echo "{},review-plan,$TOOL_CALLS,depth:$DEPTH role:$ROLE_SLUG verdict:$VERDICT" >> .claude/state/skill-performance.csv
```

Si `.claude/state/skill-performance.csv` no existe: crearlo con header. Ver `.claude/rules/skill-telemetry.md`.

---

## Integration con orchestrator-protocol

Esta skill encaja como **paso opcional** entre "Plan approved" y "Step 1: IMPLEMENT" del loop en `.claude/rules/orchestrator-protocol.md`:

```
Plan approved → /review-plan (opcional) → orchestrator activates
```

Triggers para invocar:
- Plan complejo (>3 archivos afectados, >1 hora estimada).
- Identification design o spec econométrica.
- Antes de un cambio infra grande (skills, agents, hooks).
- Cuando el usuario pide "stress-test" o "second opinion".

Skip cuando: plan es trivial (1-file edit), bug fix obvio, plan ya pasó por discussion iterativa con el usuario.

---

## Examples

```
/review-plan
/review-plan file:quality_reports/plans/2026-04-30_blattman-batch-A-B.md
/review-plan quick
/review-plan depth:deep focus:feasibility
/review-plan role:"DiD methodologist" file:quality_reports/plans/event-study-redesign.md
/review-plan dryrun
```

## Error Handling

| Condition | Behavior |
|---|---|
| No plan found | Usage message con ejemplos |
| Web search fails | Continue sin best-practice context, log it |
| `file:` path no existe | "File not found: [path]. Verificá el path." |
| Plan <50 words | Warning, proceed |
| Agent dispatch falla | Fallback inline review usando las 6 dimensiones de `plan-reviewer.md` |
