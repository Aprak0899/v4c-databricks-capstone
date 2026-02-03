# Chunking mapping

Document mapping for the 4 data chunks. Full strategy and reasoning: [step_1c_chunking_strategy.md](../../plan/day%201/step_1c_chunking_strategy.md).

---

## Mapping

| Chunk | Load type | Files | Volume path |
|-------|-----------|-------|-------------|
| **Chunk 1** | Full load | `1_photo.csv`, `1_text.csv` | `/Volumes/dev_automotive/landing/landing_raw/` |
| **Chunk 2** | Incremental load | `1_main.csv` | `/Volumes/dev_automotive/landing/landing_raw/` |
| **Chunk 3** | Dimension (full) | `catalogs.csv` → `catalogs.json` | Same volume (JSON output in volume) |
| **Chunk 4** | Dimension (full) | `final_geografic.csv` → `final_geografic.xml` | Same volume (XML output in volume) |

---

## Chunk 1 (first-time / full load)

- **Files:** `1_photo.csv`, `1_text.csv`
- **Load type:** Full load (no incremental logic).
- **Location:** `/Volumes/dev_automotive/landing/landing_raw/`

---

## Chunk 2 (incremental load)

- **Files:** `1_main.csv`
- **Load type:** Incremental load.
- **Location:** `/Volumes/dev_automotive/landing/landing_raw/`
- **Strategy:**
  - **Watermark column:** `date` (listing posting date, format DD.MM.YYYY). Use max(`date`) per run to read only new/updated rows in subsequent runs.
  - **Deduplication key:** `id` (listing identifier). Use for upsert/merge or dedupe within a batch.
  - **Approach:** Append or merge new rows; treat source as append-only. Frequency (e.g. daily/hourly) to be set in the job.

---

## Chunk 3 (source → JSON, place in volume)

- **Source file:** `catalogs.csv`
- **Output file:** `catalogs.json`
- **Load type:** Dimension (full). Convert to JSON for semi-structured ingestion.
- **Location:** `/Volumes/dev_automotive/landing/landing_raw/` (same volume; JSON written here).
- **Conversion:** Use notebook `src/notebooks/Chunks/Convert CSV Data to JSON with Audit Columns.ipynb` (or equivalent job). Ensure output is valid JSON.

---

## Chunk 4 (source → XML, place in volume)

- **Source file:** `final_geografic.csv`
- **Output file:** `final_geografic.xml`
- **Load type:** Dimension (full). Convert to XML for semi-structured ingestion.
- **Location:** `/Volumes/dev_automotive/landing/landing_raw/` (same volume; XML written here).
- **Conversion:** Use notebook `src/notebooks/Chunks/Convert CSV Data to XML with Audit Columns.ipynb` (or equivalent job). Ensure output is valid XML.
