---
name: review-paper
description: Comprehensive manuscript review covering argument structure, econometric specification, citation completeness, and potential referee objections. Orchestrates fresh-context paper-reviewer agent (prose) and optionally domain-reviewer (substance).
argument-hint: "[paper filename or path to .tex/.pdf]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Manuscript Review

Produce a thorough, constructive review of an academic manuscript — the kind of report a top-journal referee would write. Skill orquesta dos pasadas:

1. **Prose review** vía `paper-reviewer` agent en fresh context (argument structure, clarity, voice, reader calibration).
2. **Substance review** vía `domain-reviewer` agent en fresh context (treatment, identification, specification, robustness) — opcional, on-demand.

Las dos pasadas corren en agents separados con su propio contexto, no en la conversación que escribió el paper. Esto evita self-bias del modelo defendiendo decisiones previas.

**Input:** `$ARGUMENTS` — path al paper (`.tex`, `.pdf`, `.md`), o keyword para glob en project directories. Flags opcionales:
- `prose` — solo prose review (default)
- `substance` — solo domain-reviewer
- `full` — ambos en paralelo
- `focus:section` — limitar a una sección (e.g., `focus:intro`)

---

## Steps

### Step 1: Locate the manuscript

1. Si `$ARGUMENTS` empieza con `/` o contiene `\`: tratar como path directo.
2. Si no: glob en `paper/`, `overleaf_crime_in_BA/`, `meetings/`, `literature_*/` por matches.
3. Si hay múltiples matches: listar y pedir al usuario cuál.
4. Si el archivo es `.pdf`: leer via Read (chunked si es largo).

### Step 2: Parse flags

- Default: `prose` (paper-reviewer solo).
- `full`: dispatch both agents en paralelo (un solo mensaje con dos Task calls).
- `substance`: solo domain-reviewer.
- `focus:X` se pasa al agent prompt.

### Step 3: Dispatch agent(s) en fresh context

**Para prose review** — Task tool:
- `subagent_type`: `paper-reviewer`
- `description`: "Prose review of [filename]"
- `prompt`: include manuscript path + focus + voice pack reference si existe (`.claude/rules/voice-paper.md`)

**Para substance review** — Task tool:
- `subagent_type`: `domain-reviewer`
- `description`: "Substance review of [filename]"
- `prompt`: include manuscript path + focus

Si `full`: enviar las dos Task calls en un solo mensaje (paralelo).

### Step 4: Aggregate and present

Cuando el/los agents retornan:

1. Para single-agent: surface el report file path al usuario.
2. Para `full`: ambos agents escribieron a `quality_reports/`. Presentar:
   - Resumen 2-3 líneas de cada agent.
   - Rojos comunes (issues que ambos agents flaggearon — high confidence).
   - Discrepancias (algo que un agent flaggeó y el otro no).
   - Recomendación priorizada combinada.

### Step 5: Telemetry (opt-in)

Si querés trackear uso de esta skill, agregar al final:

```bash
date +%Y-%m-%d | xargs -I{} echo "{},review-paper,$TOOL_CALLS,$NOTES" >> .claude/state/skill-performance.csv
```

Ver `.claude/rules/skill-telemetry.md` para schema completo.

---

## Output Locations

- Prose review: `quality_reports/paper_review_[name]_prose.md`
- Substance review: `quality_reports/paper_review_[name]_substance.md`
- Combined summary (si `full`): `quality_reports/paper_review_[name]_combined.md`

## Notes

- **No edites el paper.** Esta skill genera reports, no modifica `.tex`/`.md` source.
- Si el paper está en formato Overleaf con múltiples archivos, leer el `.tex` master y los `\input{}` referenciados.
- Para revisar slides Beamer, usar `slide-reviewer` agent (no esta skill).
