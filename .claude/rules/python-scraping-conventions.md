---
paths:
  - "<pipeline-path>/**/*.py"
---

# Python Web Scraping Conventions

**Standard:** Reliable, reproducible web scraping for research data construction.

---

## 1. Project Structure

- All scrapers live in `<pipeline-source-path>/`
- Virtual environment: `<pipeline-source-path>/.venv/`
- Output: `<pipeline-output-path>/` (CSV and DTA formats)
- Cache: `<pipeline-cache-path>/` for intermediate results

## 2. Script Organization

```python
"""
[Descriptive title]
Author: [Your name]
Date: YYYY-MM-DD
Purpose: [What this scraper collects]
Output: [File paths of output]
"""

# Imports at top, standard library first
import os
import json
from pathlib import Path

# Third-party imports
import requests
import pandas as pd
```

## 3. Error Handling

- All HTTP requests must have `try/except` blocks
- Set reasonable timeouts on requests
- Log failures (don't silently skip)
- Save intermediate results to cache to allow resumption

## 4. Output Standards

- Primary output: CSV with UTF-8 encoding
- Secondary output: Stata .dta file for direct use in analysis
- Include a debug/raw output for verification
- Column names: `snake_case`, descriptive

## 5. Reproducibility

- Pin package versions in requirements.txt
- Document data sources and access dates
- Cache raw HTML/JSON responses for re-processing
- Deduplication logic must be explicit and documented

## 6. Rate Limiting

- Respect `robots.txt` and site terms
- Include delays between requests
- User-agent string should be descriptive

## 7. Data Validation

- Check for expected columns after parsing
- Validate date formats
- Report summary statistics after scraping (N events, date range, completeness)
