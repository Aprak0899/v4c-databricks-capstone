---

## Notebooks & Job

- [x] Implement or confirm **notebook(s)** for chunking/conversion pipeline (CSV→JSON, CSV→XML, and any first-time/incremental CSV logic as required for Day 1).
- [x] Ensure **notebook code handles multiple run scenarios** (idempotent: re-run does not duplicate data; use overwrite or MERGE as appropriate).
- [x] In Databricks, create a **Job** named **Data Chunking** that runs the above pipeline (notebooks).
- [x] Run the Job once and confirm it completes without error.

**Notebooks confirmed (chunking/conversion pipeline):**

| Chunk | Purpose | Notebook |
|-------|---------|----------|
| **Chunk 3** | CSV → JSON (catalogs.csv → catalogs.json) | `src/notebooks/Chunks/Convert CSV Data to JSON with Audit Columns.ipynb` |
| **Chunk 4** | CSV → XML (final_geografic.csv → final_geografic.xml) | `src/notebooks/Chunks/Convert CSV Data to XML with Audit Columns.ipynb` |

Chunk 1 (first-time load CSV: 1_photo.csv, 1_text.csv) and Chunk 2 (incremental CSV: 1_main.csv) are documented in [chunking_mapping.md](../Data%20chunking%20(4%20chunks)/chunking_mapping.md); load logic can be added as separate notebooks or in Bronze phase as needed.

**Multiple run scenarios (idempotent):** Both conversion notebooks write output with **overwrite** (JSON: `open(..., "w")`; XML: `ElementTree.write()`). Re-running with the same `input_path` and `output_path` produces the same result — no duplicate data. Safe for scheduled or manual re-runs.

---
