---
name: create-slides
description: Create Beamer presentation sections from project outputs (figures, tables, maps). Use when building new slides or adding sections to an existing presentation.
argument-hint: "[section-name or topic]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Agent"]
---

# Create Slides

Create new Beamer slides or sections by pulling results from the project's `output/` directory.

## Instructions

Step 1: **Understand the request**
- What section or topic? (introduction, data, methodology, results, conclusions, or custom)
- Which figures/tables/maps to include? If not specified, scan `output/` for relevant files
- Audience and level of detail?

Step 2: **Inventory available outputs**
- Scan `output/figures/`, `output/tables/`, `output/maps/`, `output/presentation/` for relevant files
- List candidate figures and tables with filenames
- Present inventory to user if selection is ambiguous

Step 3: **Create the section file**
- Write to `presentation/sections/NN_section_name.tex`
- Follow conventions in `.claude/rules/beamer-slides-conventions.md`:
  - One message per slide
  - Concise frame titles (content-descriptive, not generic)
  - Figures: `width=0.95\textwidth`, with source attribution
  - Tables: reformatted for slides (max 5 cols, 8 rows) using `\resizebox`
  - No `\pause` unless explicitly requested
- Use `\graphicspath` paths (just filenames for standard output directories)

Step 4: **Update main.tex if needed**
- If creating a new section not yet in `presentation/main.tex`, add the `\input{}` line
- Maintain section ordering

Step 5: **Verify**
- Check all referenced figure/table files exist in `output/`
- Check LaTeX syntax (matching `\begin`/`\end`, braces, brackets)
- Check no hardcoded absolute paths
- Present summary of slides created

## Examples

### Example 1: Create results section
**User says:** "/create-slides results"
**Actions:** Scan `output/figures/` for DiD and event study figures, `output/tables/` for regression tables. Create `presentation/sections/04_results.tex` with one slide per key figure/table.
**Result:** A complete results section with 8-12 slides ready for compilation.

### Example 2: Create custom section
**User says:** "/create-slides maps overview"
**Actions:** Scan `output/maps/` for crime maps. Create a section showing crime distribution by year and type.
**Result:** A maps overview section with geographic visualizations.

## Troubleshooting

**Error:** Figure not found during compilation
**Cause:** Filename mismatch or missing from `\graphicspath`
**Solution:** Verify exact filename in `output/` and check `\graphicspath` in `preamble.tex`
