# Session Logging

**Location:** `quality_reports/session_logs/YYYY-MM-DD_description.md`
**Template:** `templates/session-log.md`

## Three Triggers (all proactive)

### 1. Post-Plan Log

After plan approval, immediately capture: goal, approach, rationale, key context.

### 2. Incremental Logging

Append 1-3 lines whenever: a design decision is made, a problem is solved, the user corrects something, or the approach changes. Do not batch.

### 3. End-of-Session Log

When wrapping up: high-level summary, quality scores, open questions, blockers.

## Quality Reports

Generated **only at merge time** -- not at every commit or PR.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md` using `templates/quality-report.md`.

## Helpers

Two Python helpers live in `.claude/scripts/`:

- `atomic_write.py` — wrapper sobre `os.replace()` para escribir session logs sin riesgo de corrupción cuando el directorio está sincronizado con Dropbox / OneDrive. Usar en lugar de `Write`/`>>` para `quality_reports/session_logs/*.md`.
- `session_log_prune.py` — pruning tiered determinístico (>10k lines→7d, >6k→14d, >3k→30d, >1.5k→60d). Mueve entradas viejas a `*_archive.md` en el mismo directorio. Default target: `quality_reports/session_logs/`. Correr periódicamente:

  ```bash
  python .claude/scripts/session_log_prune.py            # ejecuta
  python .claude/scripts/session_log_prune.py --dry-run  # reporta sin tocar
  ```
