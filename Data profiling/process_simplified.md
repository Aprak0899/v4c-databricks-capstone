# Data profiling + Bronze ingestion — simplified

Plain-language overview. No jargon.

---

## What is data profiling?

**Profiling = look at your raw data and write down what you see. You do not change the data.**

You answer:

1. **Can I read the file?** (If not, path/encoding/delimiter is wrong.)
2. **How many rows?** (Record count.)
3. **What columns?** (Names and order.)
4. **What types?** (String, number, date — what Spark inferred.)
5. **How many nulls per column?** (So you know what’s missing.)
6. **Do a few rows look right?** (Eyeball sample — e.g. column shift, junk.)

You **do not** clean, transform, or build KPIs. You only **observe and document**. That’s profiling.

---

## What is Bronze ingestion?

**Bronze = load the same raw files into tables in Databricks (Bronze layer).**

- **Input:** Raw files (e.g. CSVs in your volume).
- **Output:** Delta tables in `dev_automotive.bronze` (one table per file or per chunk).
- **What you do:** Read the file, maybe add audit columns (e.g. `loaded_at`, `source_file`), write to a Bronze table. Data is still “raw” — same content, now in a table you can query.

You do **not** clean or transform in Bronze. You only **land** the data.

---

## How do they connect?

```
Raw files (CSV in volume)
        │
        ▼
   DATA PROFILING
   (look, count, note — no changes)
        │
        ▼
   Write findings (e.g. profiling_findings.md)
        │
        ▼
   BRONZE INGESTION
   (load same files into Delta tables)
        │
        ▼
   Bronze tables (e.g. dev_automotive.bronze.listing_main)
```

**Order:**  
1. **Profiling once** — run it once on raw files; know row counts, nulls, column order, issues.  
2. **Bronze** — load those files into Bronze tables. No second profiling run.

---

## What you do in practice

### Step 1 — Data profiling

1. Set `BASE_PATH` to your volume (e.g. `/Volumes/dev_automotive/landing/landing_raw/`).
2. Run **profile_csv.py** in Databricks (it loops over your CSV list).
3. Read the output: record count, columns, schema, null count per column, sample rows.
4. Write what you see in **profiling_findings.md** (e.g. “1_main.csv: 1M rows, 24 columns, column X has 5% nulls, sample looks OK”).

That’s it. No code changes to the data — only observation and notes.

### Step 2 — Bronze ingestion

1. Write (or run) a **Bronze notebook/job** that:
   - Reads each CSV from the same volume path.
   - Optionally adds audit columns (`loaded_at`, `source_file`).
   - Writes to a Delta table in `dev_automotive.bronze` (e.g. `bronze_listing_main`).
2. Run it. Your raw data now sits in Bronze tables.

---

## One-sentence summary

- **Data profiling** = Look at raw files, count rows/columns/null, look at a sample, write it down; don’t change data.  
- **Bronze ingestion** = Load those same raw files into Delta tables (Bronze layer); still raw, just stored in tables.  
- **Order:** Profile first (know what you have), then ingest into Bronze (load it).

If you want, next step is a **minimal Bronze ingestion notebook** (one CSV → one Bronze table, with audit columns) that matches this process.
