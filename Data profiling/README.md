# Data profiling

Engineering-focused profiling. Mandatory checks only. Not EDA, not data science.

| File | Purpose |
|------|--------|
| **process_simplified.md** | **Start here.** Plain-language: what is profiling, what is Bronze ingestion, order of steps, what you do in practice. |
| **profiling_guide.md** | Mandatory checks (columns, record count, nulls, structure, column shift, schema impact); WHY and code baby steps. |
| **profile_csv.py** | Runnable Databricks notebook: multi-file loop (BASE_PATH + DATA_FILES). Set widget `base_path`; runs all checks per CSV. |
| **profiling_findings.md** | (Create this) Document observations per file; raise red flags. |

**Order:** Read **process_simplified.md** first, then run `profile_csv.py` (BASE_PATH = your volume; DATA_FILES = your CSV list). Write findings in `profiling_findings.md`. Then do Bronze ingestion (load same files into Bronze tables).
