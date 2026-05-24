---
name: format-table-for-slides
description: Reformat a Stata .tex regression table from paper format to slide-readable Beamer format. Use when including analysis tables in presentations.
argument-hint: "[table filename or path]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob"]
---

# Format Table for Slides

Reformat Stata-generated `.tex` tables from paper-width format to slide-readable Beamer format.

## Instructions

Step 1: **Read the source table**
- Read the `.tex` file from `output/tables/`
- Identify: number of columns, rows, variable labels, statistics shown

Step 2: **Assess what needs changing**
- **Too many columns?** Select key specifications (e.g., 3 of 6 columns)
- **Too many rows?** Group or drop control variables, keep key regressors
- **Labels too long?** Shorten variable names and column headers
- **Font too small?** Will need `\resizebox` or `\footnotesize`

Step 3: **Create slide version**
- Write reformatted table to `output/tables/[original_name]_slides.tex`
- Apply these transformations:
  - Max 5 columns (select most important specifications)
  - Max 8 visible rows (group controls under "Controls: Yes/No")
  - Shortened labels (e.g., "Narco Raid (t-1)" not "Lagged Treatment Variable: Police Raid in Period t-1")
  - Use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`)
  - Add `\footnotesize` or `\scriptsize` if needed
  - Keep significance stars and standard errors
  - Add table notes as `\vspace{0.3em}{\tiny Note: ...}`

Step 4: **Verify**
- Numbers match the original table exactly (no rounding changes)
- LaTeX compiles (matching environments, braces)
- Present before/after summary: columns kept, rows kept, changes made

## Reformatting Rules

| Paper Format | Slide Format |
|-------------|-------------|
| 6+ columns | Select 3-5 key specs |
| Full variable list | Key regressors + "Controls: Yes/No" |
| Long labels | Abbreviated labels |
| `\begin{table}` wrapper | Remove — frame provides the float |
| `\caption{}` | Remove — frame title serves as caption |
| `\label{}` | Remove |

## Examples

### Example 1: Reformat DiD regression table
**User says:** "/format-table-for-slides did_daily_total.tex"
**Actions:** Read table, select 3 key specifications, shorten labels, remove float wrapper, output slide version.
**Result:** `output/tables/did_daily_total_slides.tex` ready for `\input{}` in Beamer frame.
