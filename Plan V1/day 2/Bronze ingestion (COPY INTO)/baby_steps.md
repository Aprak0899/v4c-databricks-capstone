# Bronze ingestion (COPY INTO) — Baby steps (ordered, SQL)

One ordered sequence. All implementation in **SQL**. Check off as you go.

---

## Ordered steps (1 → 12)

- [x] **1** — Define **schema** (column names and types) that matches your CSV (e.g. for 1_photo.csv and 1_text.csv). No auto-evolution; strict schema.
- [x] **2** — **Create** Bronze Delta table(s) in SQL with that schema **plus** audit columns: `load_dt TIMESTAMP`, `source STRING` (e.g. `dev_automotive.bronze.photo_raw`, `dev_automotive.bronze.text_raw`).
- [x] **3** — In the same table definition, rely on **schema enforcement** (default for Delta): only data matching the table schema is accepted; do not use `mergeSchema` / `overwriteSchema`.
- [x] **4** — Write a **COPY INTO** (SQL) that reads from the landing path (file or pattern, e.g. `1_photo.csv` or `*.csv`) using a source that supports adding columns (e.g. `read_files` in a subquery).
- [x] **5** — In that COPY INTO, add **load_dt** and **source** in the `SELECT`: use `current_timestamp()` for `load_dt` and `input_file_name()` (or equivalent) for `source` so every row has audit columns.
- [x] **6** — Use **COPY INTO** with no options that re-ingest the same files; by default COPY INTO is **idempotent** (same file(s) not loaded again).
- [ ] **7** — Run the **CREATE TABLE** (if not exists) once so the Bronze table(s) exist.
- [ ] **8** — Run the **COPY INTO** once for each table (or one COPY INTO per source file/pattern).
- [ ] **9** — Confirm **row count** and **sample rows** in the Bronze table(s).
- [ ] **10** — Confirm **load_dt** and **source** are populated for every row.
- [ ] **11** — Re-run the COPY INTO (same input files); confirm **row count does not double** (idempotent).
- [ ] **12** — Optionally: add table/column **descriptions** (comments) in SQL for discoverability.

---

## Summary (SQL only)

| Step | What (SQL) |
|------|------------|
| 1–3 | Define schema; `CREATE TABLE ... (cols, load_dt TIMESTAMP, source STRING) USING DELTA`; schema enforcement by default. |
| 4–6 | `COPY INTO` from landing path; in `SELECT` include `current_timestamp() AS load_dt`, `input_file_name() AS source`; rely on default idempotency. |
| 7–9 | Run CREATE TABLE then COPY INTO; check row count and sample. |
| 10–11 | Verify audit columns; re-run and verify no duplicate rows. |
| 12 | Add `COMMENT ON TABLE` / column comments if needed. |

All code for steps 1–11 can live in one SQL notebook (e.g. `02_bronze_copy_into.sql` or a notebook with SQL cells).
