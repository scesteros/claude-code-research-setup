# Research-Archive Protocol

**Applies to:** every time a discoverable research artefact reaches the `COMPLETED` / `FINALIZED` state in this repo.

**Established:** 2026-05-24. Implements the federated-archive pattern from [chrisblattman/claudeblattman / skills/deep-research.md Phase 4](https://github.com/chrisblattman/claudeblattman/blob/main/skills/deep-research.md) (MIT).

**External resource:** `~/research-archive/` — the central INDEX lives there. See its [`README.md`](~/research-archive/README.md) for the full schema, column definitions, and `append_index.py` helper documentation.

---

## When to append

Append a row to the central INDEX whenever an artefact transitions to `COMPLETED` / `FINALIZED`. The artefact stays in its project folder (raw outputs are not moved). The INDEX only holds the pointer.

**Artefacts that get registered (this project-specific):**

| Artefact | Typical path | Trigger |
|---|---|---|
| Literature review (`.md` workflow) | `quality_reports/lit_reviews/lit_review_*.md` | When `/lit-review` produces the final report |
| Literature review (`.tex` compileable) | `internal_reports/<project>/lit_review.tex` | When the `.tex` compiles cleanly |
| Citation audit | `quality_reports/lit_reviews/.citation-audit.md` (or `internal_reports/<project>/.citation-audit.md`) | When `/audit-citations` returns 0 MISMATCH / 0 AMBIGUOUS |
| Novelty audit | `internal_reports/<project>/.novelty-audit.md` | When the two-pass novelty protocol concludes |
| Fact audit | `<paper-or-section>/.fact-audit.md` | When the audit is current (no DRIFT / no STALE) |
| Research plan (major version) | `internal_reports/research-plan/research_plan.tex` | On version bumps with substantive changes only |
| Council report | `quality_reports/council/*.md` | After `/council` approval gate, when the ranking is preserved as a decision artefact |
| Seminar feedback | `quality_reports/seminar-feedback/*.md` | After `/seminar` approval gate, when the constructive-discussant report is preserved as a pre-seminar checklist |
| Synthesis report (`/synthesize-reviews`) | `quality_reports/<project>/synthesis_*.md` | After the synthesis runs |

**Artefacts that are NOT registered:** session logs, plans in progress, drafts in progress, ephemeral exploration, code artefacts under `analysis/` or `<pipeline-path>/`. The INDEX is for finalised research artefacts only.

---

## How to append

Use the helper. It enforces the schema, normalises paths to `~`-relative form, and refuses duplicate `(project, type, path)` rows unless `--update` is passed.

```bash
python "~/research-archive/append_index.py" \
  --date 2026-05-24 \
  --project this project \
  --type lit-review \
  --topic "<≤60-char human topic>" \
  --path "<absolute path to the artefact>" \
  --notes "<≤80-char one-line state>"
```

Valid `--type` values: `lit-review` / `citation-audit` / `novelty-audit` / `fact-audit` / `research-plan` / `synthesis` / `council-report` / `seminar-feedback`.

For a minor revision of an existing artefact:

```bash
python "~/research-archive/append_index.py" \
  --update \
  --project this project --type lit-review --topic "<same topic as before>" \
  --date 2026-06-15 --notes "v2: added Lindo & Padilla-Romo 2018"
```

The helper supports `--dry-run` to preview the row before writing.

---

## Discovery queries

```bash
# All this project artefacts
jq -c 'select(.project=="this project")' "~/research-archive/INDEX.jsonl"

# All lit-reviews across all projects
jq -c 'select(.type=="lit-review")' "~/research-archive/INDEX.jsonl"

# Recent (last 90 days) artefacts
jq -c --arg c "$(date -d '90 days ago' +%Y-%m-%d 2>/dev/null || date -v-90d +%Y-%m-%d)" \
  'select(.date >= $c)' "~/research-archive/INDEX.jsonl"
```

For interactive scanning, `INDEX.md` is human-readable; for programmatic queries, `INDEX.jsonl` is faster.

---

## When a row goes stale

If a registered artefact is moved, renamed, or deprecated:

- **Path change:** update the row's `path` via `--update` (`--path` field), do not delete and re-add.
- **Deprecation:** leave the row but prepend `[DEPRECATED]` to `notes` via `--update`. The historical record is preserved.
- **Deletion:** only delete the row from `INDEX.md` and `INDEX.jsonl` manually if the artefact was a smoke-test / wrong-by-mistake / never-real.

---

## Related rules

- [`.claude/rules/skill-design-patterns.md`](skill-design-patterns.md) — pattern reference; the federated-archive pattern is mentioned in §1.7 context.
- [`.claude/rules/citation-audit-log.md`](citation-audit-log.md) — schema for `.citation-audit.md` files (which the INDEX points to).
- [`.claude/rules/fact-audit-log.md`](fact-audit-log.md) — schema for `.fact-audit.md` files (which the INDEX points to).
- [`.claude/rules/session-logging.md`](session-logging.md) — session logs are explicitly *not* registered in the INDEX (they live in `quality_reports/session_logs/` and are subject to a separate prune rule).
