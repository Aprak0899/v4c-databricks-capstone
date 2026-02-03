# Bronze ingestion (COPY INTO) — Notes

---

## Landing path

**Path:** `/Volumes/dev_automotive/landing/landing_raw/`

---

## CSVs to ingest

- **1_photo.csv**
- **1_text.csv**

(From landing volume → Bronze Delta table(s).)

---

## Bronze schema

- **Catalog:** `dev_automotive`
- **Schema:** `bronze` — created ✅

---

## Baby steps reference

- **1.1** Identify CSVs and path — ✅ Path and files above.
- **1.2** Create Bronze schema in Unity Catalog — ✅ Bronze schema created.

Next: create Bronze Delta table(s), then COPY INTO with schema enforcement and audit columns (load_dt, source).

---

## Step 1.3 — Create Delta table(s) in Bronze

**Notebook name:** `01_create_bronze_tables.ipynb`

**Where to keep the file:**  
`src/jobs/bronze_ingestion/01_create_bronze_tables.ipynb`

**Full path in project:**  
`src/jobs/bronze_ingestion/`

**What the notebook does:**  
Creates empty Delta table(s) in `dev_automotive.bronze` with schema (and audit columns `load_dt`, `source`). For example:
- `dev_automotive.bronze.photo_raw` (for 1_photo.csv)
- `dev_automotive.bronze.text_raw` (for 1_text.csv)

**In Databricks:**  
Notebook path will be `src/jobs/bronze_ingestion/01_create_bronze_tables` (no `.ipynb` in job config).

---

## Ordered baby steps + SQL (all in SQL)

- **Ordered steps:** See [baby_steps.md](baby_steps.md) — single list (steps 1–12), all implementation in SQL.
- **SQL file:** `src/jobs/bronze_ingestion/02_bronze_copy_into.sql` — CREATE TABLE (with schema + load_dt, source), COPY INTO with `current_timestamp()` and `input_file_name()`, and verification queries. Adjust table columns to match your 1_photo.csv and 1_text.csv.
