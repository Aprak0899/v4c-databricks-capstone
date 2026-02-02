# Profiling / validation notebooks

Validation is split into **3 parts** (CSV, JSON, XML). The main notebook runs all 3 in order.

| Notebook | Part | Files | Purpose |
|----------|------|-------|---------|
| **profile_raw_csvs.py** | Orchestrator | — | Runs Part 1 → Part 2 → Part 3 in sequence. Widget: `base_path`. |
| **profile_raw_csv.py** | Part 1: CSV | 1_main.csv, 1_photo.csv, 1_text.csv | Two-phase malformed detection (raw vs inferred); row count, null inflation, sample. |
| **profile_raw_json.py** | Part 2: JSON | catalogs.json | Single read; row count, columns, nulls, sample. |
| **profile_raw_xml.py** | Part 3: XML | final_geografic.xml | Single read (rowTag=record); row count, columns, nulls, sample. |

- **Widget:** `base_path` (default: `/Volumes/dev_automotive/landing/landing_raw/`). Set in orchestrator; inherited by child notebooks when run via `%run`.
- **Not EDA or histograms.** Record findings in **docs/profiling_findings.md** and per-file docs (02–06).
