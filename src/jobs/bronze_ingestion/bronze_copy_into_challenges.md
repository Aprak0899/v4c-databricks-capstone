# Basic challenges — Bronze COPY INTO (`02_bronze_copy_into.sql`)

Obvious issues this job can run into.

---

## Paths & files

- **Path or Volume doesn’t exist** — `dev_automotive` catalog, Volume, or `/Volumes/dev_automotive/landing/landing_raw/` missing → COPY INTO fails.
- **CSV files missing** — `1_photo.csv` or `1_text.csv` not in the path → 0 rows loaded or failure.
- **No read permission** on the path or **no write permission** on `dev_automotive.bronze` → job fails.

---

## Schema & CSV shape

- **Wrong column names** — CSV has different headers (e.g. no `_c0`, or `Photo_URL` instead of `photo_url`) → column not found or wrong mapping.
- **Wrong delimiter** — File is semicolon/tab but code assumes comma → wrong or merged columns.
- **No header row** — `header = 'true'` but file has no header → first row treated as header, data shifted.

---

## Data types

- **First column not integer** — `_c0` → `photo_seq_id` (INT): any non-integer (empty, text, null) → cast error, COPY INTO fails.
- **id not numeric** — `id` is DOUBLE: non-numeric values → cast error.


---

## Data & behavior

- **Empty file** — 0 rows loaded; no error, but tables stay empty.
-
- **Wrong file in path** — e.g. photo CSV in `1_text.csv` → wrong data in `text_raw`.

---

## Summary

| Area           | Obvious challenge                                      |
|----------------|--------------------------------------------------------|
| Paths & files  | Path/Volume/files missing; no read/write permission   |
| Schema/CSV     | Wrong column names; wrong delimiter; no header        |
| Types          | _c0 not INT; id not numeric → cast errors             |
| Data/behavior  | Empty file; same path = stale data; wrong file in path|

---

## Resilience (without running profiling every time)

Ways to absorb or fail gracefully so you don’t have to run profiling on every run.

### 1. New column added → absorb in a rescue column

**Goal:** Don’t fail the pipeline when the CSV gets an extra column; store it instead of failing schema enforcement.

**Option A — Add `_rescue` to Bronze table (recommended):**

- Add a column to the Bronze table, e.g. `_rescue STRING`.
- Before COPY INTO, read the CSV in a **notebook** (e.g. `spark.read.csv(...)` with `inferSchema=True`), then:
  - Define the list of **known** columns (e.g. `_c0`, `photo_url`, `id` for photo).
  - Build a SELECT: known columns + `to_json(struct(<all columns not in known>)) AS _rescue`.
  - Write to a temp view or a staging Delta table, then run COPY INTO from that view/table into the Bronze table (with `load_dt`, `source` added).
- Any new column in the CSV ends up inside `_rescue` as JSON; pipeline keeps running. You can promote columns from `_rescue` to real columns later.

**Option B — Delta mergeSchema (use with care):**

- Use `COPY_OPTIONS ('mergeSchema' = 'true')` so new columns in the source get added to the Delta table. New columns appear as nullable. This changes the table schema over time; only use if you’re okay with that.

**Pure SQL limitation:** COPY INTO with a fixed `SELECT _c0, photo_url, id, ...` fails if the CSV has an extra column (source has more columns than the SELECT). So “rescue” for new columns needs a notebook step that builds the SELECT dynamically or uses a view with `_rescue`.

---

### 2. Path access denied or wrong path → fail gracefully (try/catch)

**Goal:** Don’t get a raw stack trace; log and fail with a clear message.

Pure SQL has no try/catch. **Run the ingestion from a notebook** and wrap the SQL in Python:

```python
# In a notebook cell before running 02_bronze_copy_into.sql
try:
    spark.sql("CREATE TABLE IF NOT EXISTS ...")  # and COPY INTO
    # Or run the full SQL file
except Exception as e:
    err_msg = str(e).lower()
    if "path" in err_msg or "not found" in err_msg or "permission" in err_msg or "access" in err_msg:
        # Log to a table or job run, then fail
        print(f"Path or permission error: {e}")
        raise SystemExit(1)  # or dbutils.notebook.exit("FAIL")
    raise
```

- On path-not-found or permission-denied, you catch, log, and exit with a clear status so the pipeline fails gracefully instead of an opaque error.
- Optionally write the error to a small `dev_automotive.bronze.ingestion_log` table (timestamp, job_id, table_name, error_message) before re-raising.

---

### 3. Data/behavior: empty file; same path = stale data; wrong file in path

| Issue | What to do |
|-------|------------|
| **Empty file** | After COPY INTO, check **rows inserted** or **table row count**. In a notebook: get the COPY INTO result or run `SELECT COUNT(*) FROM ...`; if you expected data (e.g. file size &gt; 0 or file existed) and count is 0, **fail or alert** (e.g. `raise Exception("Expected rows from 1_photo.csv but got 0")`). |
| **Same path = stale data** | COPY INTO is idempotent: same path is skipped. If you **replaced the file in place** and want to re-load, run **COPY INTO ... FORCE** (or the Databricks equivalent) so that path is re-ingested. Document: “After replacing a file, run COPY INTO with FORCE for that path.” |
| **Wrong file in path** | Add a **post-load check** in a notebook: e.g. for `text_raw`, assert that column `text` exists and a sample row has non-null string content (or check min length). If the wrong file was loaded (e.g. photo CSV in `1_text.csv`), this validation fails → fail the job or flag. You can do the same for `photo_raw` (e.g. `photo_url` contains `http` or `/photo/`). |

---

### Summary of resilience options

| Challenge | Approach |
|-----------|----------|
| New column in CSV | Add `_rescue STRING` to Bronze; notebook reads CSV, projects known cols + `to_json(extra_cols)` → view → COPY INTO. Or use `mergeSchema` if you accept schema evolution. |
| Path wrong / access denied | Run ingestion from a notebook; wrap SQL in try/except; on path/permission errors log and fail with clear message (or write to ingestion_log). |
| Empty file | After COPY INTO, check row count; if 0 and data was expected, fail or alert. |
| Same path = stale data | Use COPY INTO … FORCE when the file was replaced in place. |
| Wrong file in path | Post-load validation (e.g. `text_raw.text` non-null/sample check; `photo_raw.photo_url` format check); fail or alert if validation fails. |

Using a **notebook** that runs the SQL (with try/catch, optional rescue view, and post-load checks) gives you these behaviors without running the full profiling notebook every time.
