# Knowledge Base Template

When the project accumulates domain-specific knowledge (variable definitions, data source details, institutional context), store it in a knowledge base file.

## Suggested Format

```markdown
# Project Knowledge Base

## Variable Definitions

| Variable | Definition | Source | Notes |
|----------|-----------|--------|-------|
| `crime_count` | Total reported crimes per unit-period | City Open Data | Excludes contraventions |

## Data Sources

| Source | Coverage | Frequency | Access |
|--------|----------|-----------|--------|
| City Crime Map | 2016-present | Daily | Open data portal |

## Institutional Context

- [Key facts about the setting that inform analysis decisions]

## Methodology Notes

- [Key decisions about estimation strategy and why]
```

Save to `quality_reports/knowledge_base.md` as the project grows.
