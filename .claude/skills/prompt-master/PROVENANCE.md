# Provenance — prompt-master skill

This skill is a third-party import. It was incorporated into this project on **2026-05-24** at the request of the user.

## Upstream source

- **Repository:** [github.com/nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master)
- **Author:** Nidhin J. S.
- **Upstream version imported:** `1.6.0` (as declared in upstream `SKILL.md` frontmatter)
- **Upstream license:** MIT (preserved verbatim in [`LICENSE`](LICENSE))

## Files imported

| File | Source path in upstream | Status |
|---|---|---|
| [`SKILL.md`](SKILL.md) | `SKILL.md` (repo root) | Content preserved verbatim; frontmatter extended with `argument-hint` and `allowed-tools` to match this project's skill convention |
| [`references/patterns.md`](references/patterns.md) | `references/patterns.md` | Preserved verbatim |
| [`references/templates.md`](references/templates.md) | `references/templates.md` | Preserved verbatim |
| [`LICENSE`](LICENSE) | `LICENSE` | Preserved verbatim |

## Modifications made to the upstream content

Two additions to the `SKILL.md` frontmatter only, to align with this project's skill convention used by every other skill under `.claude/skills/`:

```yaml
argument-hint: "[describe the prompt you want to generate, fix, or adapt — name the target AI tool if known]"
allowed-tools: ["Read"]
```

No substantive content was changed. The PRIMACY ZONE, MIDDLE ZONE, and RECENCY ZONE — including all hard rules, tool-routing tables, output format, diagnostic checklist, memory block, and reference-file pointers — are exact copies of the upstream `SKILL.md` v1.6.0.

## How to update from upstream

When a new version is released upstream:

```bash
cd /tmp && rm -rf promptmaster && mkdir promptmaster && cd promptmaster
curl -fsSL https://raw.githubusercontent.com/nidhinjs/prompt-master/main/SKILL.md             -o SKILL.md
curl -fsSL https://raw.githubusercontent.com/nidhinjs/prompt-master/main/references/patterns.md  -o patterns.md
curl -fsSL https://raw.githubusercontent.com/nidhinjs/prompt-master/main/references/templates.md -o templates.md
curl -fsSL https://raw.githubusercontent.com/nidhinjs/prompt-master/main/LICENSE               -o LICENSE
```

Then copy into `.claude/skills/prompt-master/` and re-apply the two-line frontmatter extension above. Update the `Upstream version imported` line in this file.

## How to invoke

The skill is user-invoked only (consistent with this project's convention). Typical invocations:

- `/prompt-master <describe what you need>` — explicit slash-command invocation.
- "Write me a Midjourney prompt for X" / "Fix this Cursor prompt: …" / "Adapt this Claude prompt for ChatGPT" — natural-language requests that match the activation criteria in the upstream `SKILL.md` description.

The skill does **not** activate for general conversation, coding tasks, or document writing — see the `description` field of [`SKILL.md`](SKILL.md) for the exact activation criteria.
