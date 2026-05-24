# Skill Telemetry (opcional)

Tracking ligero de cuántas veces se invocan las skills, cuántos tool calls usan, y notas estructuradas para análisis post-hoc. Patrón adaptado de `chrisblattman/claudeblattman` (`skills/done.md` v2.4.2 y `skills/council.md` v1.3).

**Estado:** opt-in. Cada skill que el usuario quiera trackear se opta agregando un snippet al final de su `SKILL.md`. No hay enforcement automático.

## Schema

Archivo único: `.claude/state/skill-performance.csv`

```
date,skill,tool_calls,notes
```

| Campo | Descripción | Ejemplo |
|---|---|---|
| `date` | `YYYY-MM-DD` (fecha de invocación) | `2026-04-30` |
| `skill` | Nombre de la skill | `review-plan` |
| `tool_calls` | Estimación de tool calls usados en esta invocación | `12` |
| `notes` | String estructurado `key:value key:value ...` o texto libre breve | `depth:standard role:DiD verdict:REVISE` |

## Snippet para incluir en una SKILL.md

Al final de la skill, después de presentar el output al usuario:

```bash
# Opt-in telemetry — comentar para deshabilitar
CSV=".claude/state/skill-performance.csv"
mkdir -p "$(dirname "$CSV")"
[ ! -f "$CSV" ] && echo "date,skill,tool_calls,notes" > "$CSV"
echo "$(date +%Y-%m-%d),<SKILL_NAME>,<TOOL_CALLS_ESTIMATE>,<NOTES>" >> "$CSV"
```

## Path y privacidad

- **Path canónico:** `.claude/state/skill-performance.csv` (relativo al repo root).
- **Gitignored:** sí. La telemetría es local al usuario; no se commitea. Ver `.gitignore` (entrada `.claude/state/skill-performance.csv`).
- **No PII.** Las notas no deben incluir paths de archivos privados, contenido de email/Drive, ni nombres de personas. Estructura `key:value` corta es suficiente.

## Lectura post-hoc

Para ver invocaciones recientes:

```bash
tail -20 .claude/state/skill-performance.csv
```

Para conteos por skill:

```bash
awk -F, 'NR>1 {print $2}' .claude/state/skill-performance.csv | sort | uniq -c | sort -rn
```

Para skills más caras (en tool calls promedio):

```bash
awk -F, 'NR>1 {sum[$2]+=$3; n[$2]++} END {for (s in sum) print sum[s]/n[s], s}' \
  .claude/state/skill-performance.csv | sort -rn | head
```

## Cuándo activar

Considerar activar telemetría en una skill cuando:

- La skill se va a usar repetidamente (no one-off).
- Hay sospecha de costo alto en tool calls.
- Se está iterando el diseño de la skill y conviene medir antes/después.

No activar para skills triviales o que no se van a usar más de una vez.

## Skills con telemetría activa

(Mantener manualmente esta tabla cuando se activa la telemetría en una skill.)

| Skill | Activada | Notas-format |
|---|---|---|
| `review-plan` | 2026-04-30 | `depth:X role:Y verdict:APPROVE/REVISE` |

(El resto: opt-in pendiente.)
