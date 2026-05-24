---
name: compile-latex
description: Provide LaTeX compilation instructions for the Beamer presentation. Edit-only — shows commands and troubleshoots errors, does not execute compilation.
argument-hint: "[optional: error log or issue]"
allowed-tools: ["Read", "Grep", "Glob"]
---

# Compile LaTeX

Provide compilation instructions and troubleshoot LaTeX errors. Edit-only mode — Claude does not run the compiler.

## Instructions

Step 1: **Provide compilation commands**

```bash
cd presentation/
xelatex main.tex
# Run twice for table of contents and references:
xelatex main.tex
```

Or with pdflatex:
```bash
cd presentation/
pdflatex main.tex
pdflatex main.tex
```

Step 2: **If user provides an error log, diagnose it**
- Read the `.log` file or error output
- Identify the error type and location
- Provide specific fix

Step 3: **Common issues and fixes**

| Error | Cause | Fix |
|-------|-------|-----|
| `File not found` | Wrong figure path | Check `\graphicspath` and filename |
| `Undefined control sequence` | Missing package | Add `\usepackage{}` to preamble |
| `Missing \begin{document}` | Preamble syntax error | Check preamble.tex for typos |
| `Overfull \hbox` | Content too wide | Use `\resizebox` or reduce content |
| `Too many unprocessed floats` | Too many figures | Use `[H]` placement or reduce |

## Examples

### Example 1: First compilation
**User says:** "/compile-latex"
**Actions:** Show compilation commands for the project's presentation.
**Result:** Step-by-step instructions to compile `presentation/main.tex`.

### Example 2: Debug error
**User says:** "/compile-latex" (with error log pasted)
**Actions:** Read error, identify cause, suggest fix to the .tex file.
**Result:** Specific edit to resolve the compilation error.
