---
paths:
  - "analysis/**/*.do"
  - "<pipeline-path>/**/*.py"
  - "output/**"
---

# Task Completion Verification Protocol

Tras editar `.do` / `.py` / `.tex` o producir un output de análisis, verificar antes de cerrar la tarea con el procedimiento que aplica abajo. Si la verificación detecta un problema, fix y re-verify; máximo 2 retries antes de surfacing al usuario.

## For Stata .do Files (Edit-Only):

Since Claude edits but does not run Stata:
1. Review the .do file for syntax errors (missing semicolons, unmatched quotes, wrong variable names)
2. Check that all referenced globals exist in `0_CABA_Master.do`
3. Verify file paths use globals, not hardcoded paths
4. Check merge logic: correct `using` files, appropriate merge type (1:1, m:1, 1:m)
5. Verify output paths exist and are correct (`$output/figures/`, `$output/tables/`, etc.)
6. Flag any commands that require packages not in the `install_packages` block
7. Report what the user should verify by running the file

## For Python Scripts (Edit-Only):

Since Claude edits but does not run scrapers:
1. Review for syntax errors
2. Check import statements are complete
3. Verify output paths are correct
4. Check error handling around web requests
5. Verify data validation logic
6. Report what the user should verify by running the script

## For Research Outputs (Tables, Figures):

When reviewing existing outputs:
1. Check figures exist and are non-zero size
2. Verify table formatting meets publication standards
3. Check that coefficient signs and magnitudes are reasonable
4. Verify all required statistics are present (N, SE, R-squared)

## Verification Checklist:

```
[ ] Code reviewed for syntax/logic errors
[ ] All file paths use project globals
[ ] No hardcoded absolute paths
[ ] Output destinations are correct
[ ] Dependencies documented
[ ] User told what to verify by running the code
```
