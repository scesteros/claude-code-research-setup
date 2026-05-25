---
paths:
  - "presentation/**/*.tex"
---

# Beamer Slide Conventions

## Edit-Only Mode

Claude writes and edits `.tex` files. The user compiles with `xelatex` or `pdflatex` manually.

## Directory Structure

```
presentation/
├── preamble.tex          # User's Beamer theme (do not modify without permission)
├── main.tex              # Master file — \input{} for each section
├── sections/             # Individual slide sections
│   ├── 01_introduction.tex
│   ├── 02_data.tex
│   ├── 03_methodology.tex
│   ├── 04_results.tex
│   └── 05_conclusions.tex
└── figures/              # Slide-specific figures (if any)
```

## Including Project Outputs

### Figures

Use relative paths from `presentation/` to `output/`:

```latex
\includegraphics[width=\textwidth]{../output/figures/figure_name.png}
```

The `\graphicspath` in `preamble.tex` already includes `../output/figures/`, `../output/maps/`, and `../output/presentation/`, so you can use just the filename:

```latex
\includegraphics[width=\textwidth]{figure_name.png}
```

### Tables

Stata `.tex` tables in `output/tables/` are formatted for paper width. For slides:
1. Use the `/format-table-for-slides` skill to reformat
2. Or manually adapt: reduce columns, increase font size, simplify labels

```latex
% Direct include (if already slide-formatted):
\input{../output/tables/table_name.tex}

% Or inline the reformatted version directly in the frame
```

### Maps

```latex
\includegraphics[width=\textwidth]{../output/maps/map_name.png}
```

## Frame Conventions

### Structure

```latex
\begin{frame}{Title — Short and Descriptive}
  % One key message per slide
  % Max 3-4 bullet points or one figure/table
\end{frame}
```

### Rules

- **One message per slide** — do not overload frames
- **Frame titles:** concise, informative (not "Results 1", but "DiD: Daily Crime Reduction")
- **No `\pause`** — avoid incremental reveals unless explicitly requested
- **Figures fill the frame** — use `width=\textwidth` or `height=0.8\textheight`
- **Tables on slides** — max 5 columns, max 8 rows visible. Simplify from paper format
- **Notes:** use `\note{}` for presenter notes if needed

### Figure Slides

```latex
\begin{frame}{Event Study: Total Crime (Weekly)}
  \centering
  \includegraphics[width=0.95\textwidth]{event_study_total_weekly.png}
  \vspace{-0.5em}
  {\footnotesize Source: City Crime Data, 2016--2023}
\end{frame}
```

### Table Slides

```latex
\begin{frame}{Main DiD Results}
  \centering
  \resizebox{\textwidth}{!}{%
    \input{../output/tables/did_main_results_slides.tex}
  }
\end{frame}
```

## Naming Conventions

- Section files: `NN_section_name.tex` (numbered for order)
- Slide-formatted tables: `*_slides.tex` suffix
- Slide-specific figures: store in `presentation/figures/`

## Quality Standards

- All figures must have source attribution
- All tables must have notes explaining key statistics
- Consistent font sizes within a presentation
- No overfull/underfull box warnings (check log)
- Spell-check all text content
