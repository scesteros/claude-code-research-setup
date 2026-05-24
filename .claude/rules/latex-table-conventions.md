# LaTeX Table Conventions

**Applies to:** every `.tex` table emitted by a do-file (Stata `file write`, `esttab`, etc.) and every table inserted into a report or paper draft in this repo.

**Established:** 2026-04-22. Recorded as a project convention for all future tables.

---

## Canonical table skeleton

```latex
\begin{table}[H]
\centering
\caption{[Descriptive title --- DO NOT include "Sample II" or any sample-label suffix]}
\label{[tab:short_key]}
\vspace{0.6em}                                  % separates caption from tabular (see Rule 3)
\resizebox{\textwidth}{!}{%                     % Rule 1: table width = text width
\begin{tabular}{[col spec]}
\hline\hline \\ [-1.5ex]                        % Rule 2: double line at top
[header row] \\
\hline \\ [-1.5ex]                              % Rule 2: single line inside
[body rows, with \hline simple between panels]
[.3ex] \hline\hline                             % Rule 2: double line at bottom
\end{tabular}%
}
\vspace{0.4em}                                  % separates tabular from notes
\begin{minipage}{\textwidth}                    % Rule 4: notes match table width
\scriptsize                                     % Rule 4: notes are smaller than body
\textit{Notes.} [notes text, with \textit{} / \textbf{} as needed]
\end{minipage}
\end{table}
```

---

## Rules

1. **Width = text width.** Wrap the `tabular` in `\resizebox{\textwidth}{!}{%...}`. Do NOT use `\scalebox{.9}{...}` on top of it -- that shrinks the table below the text width and leaves asymmetric margins.

2. **Horizontal lines.** Double (`\hline\hline`) at the very top of the table body and at the very bottom. Single (`\hline`) between panels, under headers, and nowhere else. Do NOT use booktabs (`\toprule`, `\midrule`, `\bottomrule`) in tables emitted from our do-files, for consistency with this project's convention.

3. **Caption--tabular separation.** Add `\vspace{0.6em}` between `\label{}` and the `\resizebox` to prevent the caption overlapping the top of the table. This is needed because the project preamble sets `\captionsetup[table]{skip=-0.2cm}` which pulls the caption down.

4. **Notes block.** Use `\begin{minipage}{\textwidth} \scriptsize ... \end{minipage}` instead of `\begin{threeparttable}\begin{tablenotes}`. The minipage pattern guarantees that the notes block is exactly the same width as the (resized) table, and `\scriptsize` keeps the notes visibly smaller than the body. Avoid `threeparttable` because it sizes the notes to the natural (pre-resize) tabular width, which is usually smaller than `\textwidth`.

5. **Sample labels.** Do NOT include "Sample II" or any sample-ID suffix in captions, notes, or section headings. Sample II is the only sample used across the project and the label adds no information. (Filenames keep the `_SII` suffix for disk organisation; that is fine.)

6. **Do-file and output coherence.** When a do-file is updated to match these rules, also update the already-written `.tex` outputs that feed current reports, so the report compiles correctly without re-running the do-file. Conversely, when editing an output by hand for a specific report, mirror the change in the emitting do-file so the next run does not regress.

---

## Affected do-files (current audit)

| File | Status |
|---|---|
| `analysis/9_Exploratory_Tables.do` | Compliant (updated 2026-04-22) |
| `analysis/9_Exploratory_Graphs_Clean.do` (G5 summary block) | Compliant (updated 2026-04-22) |
| `analysis/13_Descriptive_Villas_vs_Barrios.do` | Compliant (updated 2026-04-22) |
| `analysis/12_Descriptive_Cross_Section_Response.do` | **Pending** -- still emits `threeparttable` + booktabs |
| `analysis/12_Descriptive_Crime_Type_Decomposition.do` | **Pending** |
| `analysis/12_Descriptive_Sanity_Checks.do` | **Pending** |

Any new Stata `file write` block that emits a LaTeX table must follow the canonical skeleton above.
