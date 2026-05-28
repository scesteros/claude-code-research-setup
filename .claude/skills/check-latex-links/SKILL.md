---
name: check-latex-links
description: User-invoked static check for broken LaTeX cross-references and file links in a .tex document. Trigger when the user runs `/check-latex-links` or explicitly asks to check refs/labels/inputs — e.g., "check the links in this paper", "are any \ref broken?", "do all the \input tables and figures exist?", "find undefined references without compiling". Catches \ref/\eqref/\cref pointing at a missing \label, duplicate \label definitions, missing \input/\include targets, and missing \includegraphics images — before compilation, so you do not have to dig through the .log. Resolves path macros (e.g. a \newcommand path shortcut), follows \input recursively so labels emitted by input-ed files are found, and respects \IfFileExists branch selection so placeholder labels in dead branches are not miscounted. Do NOT auto-trigger from .tex edits.
argument-hint: "[path/to/main.tex] (the document's root .tex)"
allowed-tools: ["Bash", "Read", "Edit", "Grep", "Glob"]
---

# /check-latex-links — Static LaTeX link checker

Find broken cross-references and file links in a `.tex` project **without
compiling**. It reads what `pdflatex` would otherwise only tell you as
`Reference ... undefined` / `File ... not found` warnings buried in the `.log`.

## When to use

- The user runs `/check-latex-links` or asks to check refs/labels/inputs/figures.
- After renaming labels, tables, or figures, to confirm every `\ref` still
  resolves to its `\label` and every `\input`/`\includegraphics` target exists.
- Before handing a document to the user to compile, as a cheap pre-flight.

Do **not** auto-trigger on `.tex` edits; this is opt-in.

## What it catches

| Check | Failure reported |
|---|---|
| `\ref` / `\eqref` / `\pageref` / `\autoref` / `\cref` / `\Cref` / `\nameref` | target name has no `\label` anywhere in the project |
| `\label` | the same name is defined more than once (LaTeX "multiply defined") |
| `\input` / `\include` | the target `.tex` file does not exist |
| `\includegraphics` | the image is not found on `\graphicspath` (tries `.png/.pdf/.jpg/.jpeg/.eps` if no extension) |

## Why a script and not a grep

A single-file grep produces false positives on two common patterns:

1. **Labels that live inside `\input`-ed files.** When a sub-file (e.g. a
   generated table) emits its own `\label` that the main document `\ref`s, a
   grep of the main file alone flags every such `\ref` as broken. The script
   resolves path macros (e.g. a `\newcommand{\figdir}{...}` shortcut) and
   follows `\input`/`\include` recursively, so those labels are found.

2. **`\IfFileExists{file}{\input{file}}{placeholder \label}` guards.** A grep
   reports the placeholder `\label` in the dead branch as a duplicate. The
   script keeps only the live branch (based on whether the guarded file exists
   on disk) and ignores labels in the dead branch.

Comments (`%`) are stripped first, so a commented-out `\ref` is not flagged.

## Workflow

Step 1 — **Resolve the target.** Use the `.tex` the user named, or the
document's root `.tex` (the one with `\documentclass` / `\begin{document}`). To
check a whole folder, pass each top-level `.tex`.

Step 2 — **Run the checker** (Python 3, stdlib only — safe to execute):

```bash
python3 .claude/skills/check-latex-links/check_latex_links.py path/to/main.tex
```

Pass several files to check them in one go. Exit code is `0` when clean, `1`
when any problem is found.

Step 3 — **Interpret and fix.**
- **BROKEN REFS** — the `\label` is misspelled / was renamed (fix the `\ref` to
  match, or vice-versa), or the sub-file that should emit the label is missing.
  Check both sides before editing.
- **DUPLICATE LABELS** — rename one, or inspect the two locations it prints to
  see whether it is a real conflict.
- **MISSING INPUT FILES** — the file has not been generated yet, or the path /
  filename drifted. If a tool/script emits the file, confirm the emitter and the
  `\input` path agree.
- **MISSING GRAPHICS** — the figure has not been exported yet, or the filename
  in `\includegraphics` does not match the exported image.

If a label or filename is wrong in a **generated** `.tex` (one emitted by a
script), fix the emitting script too so the next run does not regress.

Step 4 — **Re-run** until the checker prints `OK - no broken links found.`

## Notes & limits

- Static analysis: it checks names and file existence, not whether a number in a
  referenced table is correct.
- It does not resolve macro-built label names (e.g. `\label{tab:\bracket}`); such
  cases need a compile.
- It does not check BibTeX `\cite*{}` keys — use the project's citation-audit
  skill (e.g. `/audit-citations`) for those.
