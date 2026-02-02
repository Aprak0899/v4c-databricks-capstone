# Bronze ingestion risks vs pre-ingestion profiling

Running `01_profile_raw_csv.ipynb` before Bronze ingestion (e.g. `02_bronze_copy_into.sql`) helps catch some issues early. This file maps each risk to whether profiling **solves**, **partially catches**, or **does not address** it.

---

## 1. Paths & files

| Risk | Profiling helps? | Notes |
|------|-------------------|--------|
| **Volume/path missing** | **Partially** | `dbutils.fs.ls(path)` fails → "Cannot access file". You see the failure before running COPY INTO. |
| **Files missing** | **Yes** | Same: `ls(path)` fails if `1_photo.csv` / `1_text.csv` (or `1_main.csv`) are not there. |
| **Wrong path/workspace** | **Yes** | Wrong path → ls/read fails in the notebook. |
| **Permissions** | **Yes** | No read on Volume → ls or `spark.read.csv` fails during profiling. |

---

## 2. Schema & CSV layout

| Risk | Profiling helps? | Notes |
|------|-------------------|--------|
| **Column names differ from Bronze** | **Partially** | Profiling shows **actual** column names (raw + inferred) and a 5-row sample. You can spot wrong names (e.g. `Photo_URL` vs `photo_url`, or no `_c0`). No automatic check against the Bronze schema. |
| **BOM / encoding** | **Partially** | First column may appear as `\ufeffid`. You’d see it in the column list/sample. Notebook uses `encoding: utf-8`; no explicit BOM strip or check. |
| **Wrong delimiter** | **Partially** | If file is semicolon/tab, raw read can get one or wrong columns; row count or column mismatch / null inflation may surface. Delimiter is fixed per file in the notebook (comma). |
| **No header / header in wrong row** | **Partially** | With `header=true`, if there’s no header you get `_c0`, `_c1`, … and a sample that looks like data in the “header” row. Human can spot; no automatic “expected column names” check. |

---

## 3. Data types & parsing

| Risk | Profiling helps? | Notes |
|------|-------------------|--------|
| **_c0 not castable to INT** | **Yes** | Infer schema then **null inflation** check: non-integers/empties become null → null count increases → notebook raises. |
| **id not castable to DOUBLE** | **Yes** | Same: non-numeric values → null after inference → null inflation → failure. |
| **Malformed rows (quotes, newlines)** | **Partially** | **Row count** check (raw vs inferred): if parsing drops or merges rows, counts differ → exception. PERMISSIVE mode may put bad rows in `_corrupt_record`; if that changes row count, you catch it. |

---

## 4. Tables & catalog

| Risk | Profiling helps? | Notes |
|------|-------------------|--------|
| **Catalog/schema missing** | **No** | Profiling only reads CSVs; it does not create or check Delta tables or catalog. |
| **Table already exists with different schema** | **No** | Same; no table access in the notebook. |

---

## 5. COPY INTO behavior

| Risk | Profiling helps? | Notes |
|------|-------------------|--------|
| **Idempotency skips updated file** | **No** | Profiling doesn’t track what COPY INTO has already loaded. |
| **_metadata.file_path unavailable** | **No** | Profiling doesn’t run COPY INTO; can’t detect runtime metadata issues. |

---

## 6. Data quality (load succeeds, data wrong)

| Risk | Profiling helps? | Notes |
|------|-------------------|--------|
| **Empty file** | **Yes** | Explicit checks: 0 MB file → exception; zero records after read → exception. |
| **Wrong file in path** | **Partially** | Different columns/schema and sample content visible; you can see e.g. photo columns in `1_text.csv`. No automatic “this file must have column X”. |
| **Duplicates in CSV** | **No** | Profiling doesn’t deduplicate or flag duplicates. |
| **Nulls / bad values allowed** | **Partially** | Per-column null/empty counts and sample are shown; no NOT NULL or business-rule checks. |

---

## 7. Operations & environment

| Risk | Profiling helps? | Notes |
|------|-------------------|--------|
| **Cluster can’t access Volume** | **Yes** | If the notebook runs (ls + read), the same cluster can read the path for COPY INTO. |
| **Concurrent runs** | **No** | Not covered by profiling. |
| **Very large files / timeouts** | **Partially** | File size is printed (MB); no timeout or size-limit check. |

---

## Summary

| Category              | Solved / caught | Partially | Not addressed |
|-----------------------|-----------------|-----------|-------------------------------|
| Paths & files         | 3               | 1         | 0                             |
| Schema & CSV layout   | 0               | 4         | 0                             |
| Data types & parsing  | 2               | 1         | 0                             |
| Tables & catalog      | 0               | 0         | 2                             |
| COPY INTO behavior    | 0               | 0         | 2                             |
| Data quality          | 1               | 2         | 1                             |
| Operations            | 1               | 1         | 1                             |

**Running `01_profile_raw_csv.ipynb` before ingestion:**

- **Directly helps:** Missing/wrong path or file, permissions, empty file, type errors on `_c0` (INT) and `id` (DOUBLE), null inflation from bad casts, and basic cluster/path access.
- **Partially helps:** Column names, encoding/BOM, delimiter, header issues, malformed rows, wrong file in path, null/bad value visibility, large files (size reported).
- **Does not address:** Catalog/schema/table existence, COPY INTO idempotency and metadata, duplicate rows, concurrent runs.

Use profiling as a **first-time / pre-ingestion gate** to avoid obvious path, file, schema, and type failures; then rely on Bronze validation and idempotency checks for the rest.
