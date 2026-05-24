---
name: update-slides
description: Update existing Beamer slides with new or updated results (figures, tables, maps). Use when analysis outputs have changed and slides need refreshing.
argument-hint: "[section or file to update]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Agent"]
---

# Update Slides

Update existing Beamer slides when project outputs (figures, tables, maps) have changed.

## Instructions

Step 1: **Identify what changed**
- Read the target section file in `presentation/sections/`
- Check which figures/tables it references
- Compare with current files in `output/` — any new outputs? renamed files? removed files?

Step 2: **Determine update scope**
- New results to add (new figures/tables from latest analysis run)
- Existing references to update (filename changes, new versions)
- Slides to remove (results no longer relevant)
- Frame titles or text to update (if estimates changed)

Step 3: **Apply updates**
- Edit the section `.tex` file
- Follow `.claude/rules/beamer-slides-conventions.md`
- Update frame titles to reflect current results
- Add/remove `\includegraphics` or `\input` as needed
- Update source attributions if data coverage changed

Step 4: **Verify**
- All referenced files exist in `output/`
- No broken `\includegraphics` or `\input` references
- LaTeX syntax is valid
- Present diff summary to user

## Examples

### Example 1: Refresh after new analysis run
**User says:** "/update-slides results"
**Actions:** Read current results section, cross-reference with `output/figures/` and `output/tables/`, identify new/changed outputs, update slides.
**Result:** Results section updated with latest figures and tables.

### Example 2: Add new figure to existing section
**User says:** "/update-slides add robustness check to results"
**Actions:** Find robustness figures in `output/figures/`, add new frames to results section.
**Result:** New robustness slides appended to results section.
