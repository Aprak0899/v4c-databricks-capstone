# Data Profiling Guide — Engineering-Focused

**Engineering-focused.** Not exploratory data analysis (EDA). Not data science.

**Validation mindset:** Treat profiling as a data quality gate. Identify ingestion issues early. Raise red flags instead of fixing silently. Assume data is broken until proven otherwise.

**Profiling:** Run once on raw files. Document findings. No second profiling run.

---

## Baby steps — code walkthrough (profile_csv.py)

Step-by-step explanation of what the notebook does and why.

### Step 1 — Config

**What:** Set `BASE_PATH` (e.g. your UC volume path) and a list of CSV filenames (`DATA_FILES`).

**Why:** One place to change paths. No hard-coded paths inside the loop. Matches your five CSVs in landing.

**Code:** Widget for `base_path`; normalize with `.rstrip("/") + "/"` so paths join correctly. List of file names only (e.g. `"1_main.csv"`, `"catalogs.csv"`).

---

### Step 2 — Loop over files

**What:** For each file in `DATA_FILES`, run the same checks.

**Why:** One notebook profiles all CSVs. Clear header per file (`========== Profiling {file} ==========`) so output is easy to read.

**Code:** `for file in DATA_FILES:`. Skip non-CSV with a WARNING and `continue`.

---

### Step 3 — Read CSV (one read per file)

**What:** Build full path (`BASE_PATH + file`) and read with Spark: header=true, encoding UTF-8, inferSchema=true.

**Why:** One read gives you both structure and types. UTF-8 preserves Cyrillic. inferSchema=true so you see inferred types (and any column that becomes null after cast — document in findings).

**Code:** `spark.read.format("csv").option("header", "true").option("encoding", "UTF-8").option("inferSchema", "true").load(full_path)`.

---

### Step 4 — File readability

**What:** If the read succeeds, print "File readability: OK".

**Why:** Confirms the file loaded. If it failed (wrong path, encoding, malformed CSV), Spark would raise; no extra try/except needed for minimal flow.

---

### Step 5 — Record count

**What:** `df.count()` → total number of rows. Print it. If 0, print ERROR and skip to next file.

**Why:** Mandatory check. First thing people expect. Empty file = red flag; skip so you don't waste time on null report.

**Code:** `record_count = df.count()`. `if record_count == 0: print("ERROR: ..."); continue`.

---

### Step 6 — Column names and order

**What:** Print `df.columns` (list of column names in order).

**Why:** Mandatory check. You need names and order for schema contract and to spot column shift (e.g. wrong delimiter pushed a column).

**Code:** `print(df.columns)`.

---

### Step 7 — Schema (inferred)

**What:** `df.printSchema()` — column names and inferred types (string, long, double, etc.).

**Why:** Documents what Spark thinks the types are. If you later cast in Bronze and see new nulls (e.g. salary was full, now has nulls), that’s schema casting impact — document in findings.

**Code:** `df.printSchema()`.

---

### Step 8 — Null count per column (single pass)

**What:** One aggregation that counts nulls for every column at once. No loop of `.count()` per column.

**Why:** Mandatory check. Single pass = one Spark job, not N jobs. High null % or new nulls after Bronze cast = red flag.

**Code:** `df.agg(*[F.sum(F.when(F.col(c).isNull(), F.lit(1)).otherwise(F.lit(0))).alias(c) for c in df.columns]).collect()[0]`. That returns one row (as a dict-like object) with one value per column = null count. Then loop and print `column: N nulls`.

---

### Step 9 — Sample rows

**What:** `df.show(5, truncate=40)` — show 5 rows, truncate long strings to 40 chars.

**Why:** Mandatory check. Eyeball for CSV malformation: column shift (e.g. comma inside a field), delimiter/qualifier issues, junk. No histogram, no EDA — just look and note in profiling_findings.md.

**Code:** `df.show(5, truncate=40)`.

---

### Step 10 — Document outside code

**What:** After the run, write observations in profiling_findings.md. After Bronze cast, run the same null check on the Bronze table and compare.

**Why:** Code only prints. Findings (e.g. "salary has new nulls after cast", "column X looks shifted") live in the doc. Schema casting impact = new nulls can appear after Bronze cast; document in findings if you see that.

---

## Mandatory profiling checks

Each check has a short WHY and a code idea. One read per file (inferSchema true) is enough for all of these.

### Columns: names, count, order consistency

**WHY:** Schema contract and downstream joins. Column order must be consistent across files and runs.

**Code idea:** `df.printSchema()` for names and types. `df.columns` for order (eyeball or compare across files).

---

### Record counts: total per file (and consistency across stages)

**WHY:** First thing people expect. Contract for ingestion. Later, compare counts across Bronze/Silver to catch drops.

**Code idea:** `df.count()`. If 0, skip or raise. Document per file in profiling_findings.md.

---

### Null checks: null count per column (and after transformations)

**WHY:** Quality gate. High null % → drop or default. 0% null → candidate key or required field. After Bronze cast, re-profile to see new nulls introduced by bad types.

**Code idea:** For each column: null count (and null %). Build a small table (list of dicts → createDataFrame). After Bronze, run the same on the Bronze table and compare.

---

### Structure: file format (CSV / JSON / XML), flat vs nested

**WHY:** How to read and whether to flatten. CSV = flat. JSON/XML = possibly nested (arrays, structs).

**Code idea:** CSV: one print "Structure: flat (CSV)." JSON/XML: note nesting in findings; no fancy code.

---

### Column shifts: misaligned columns (delimiter / qualifier issues)

**WHY:** Catches bad parsing. Extra commas or wrong qualifiers shift columns.

**Code idea:** Eyeball sample rows. No automated heuristic. Note in profiling_findings.md: "Sample checked; no shifted columns" or "Column X misaligned — fix delimiter."

---

### Schema casting impact: before vs after schema, new nulls after cast

**WHY:** Bad types introduce nulls when you cast in Bronze. Profile once with inferred schema; document inferred types. If Bronze cast introduces new nulls, note that in findings.

**Code idea:** Profile raw with `inferSchema=true`. Document inferred types. After Bronze cast, run null report again on Bronze table; document any new nulls.

---

## One code flow (no redundancy)

Use one read per file. Then: count → empty check → columns → schema → null count (single pass) → sample. No describe(), no stats.

```python
df = spark.read.format("csv").option("header", "true").option("encoding", "UTF-8").option("inferSchema", "true").load(full_path)
record_count = df.count()
if record_count == 0:
    continue
print(df.columns)
df.printSchema()
null_counts = df.agg(*[F.sum(F.when(F.col(c).isNull(), F.lit(1)).otherwise(F.lit(0))).alias(c) for c in df.columns]).collect()[0]
# print null_counts per column
df.show(5, truncate=40)
```

**Full multi-file notebook:** See [profile_csv.py](profile_csv.py) for BASE_PATH + DATA_FILES loop and all checks in one place.

---

## Profiling at scale: sample vs full

**Sample:** For discovery or large files (e.g. 10 GB), read with `.limit(n)` (e.g. 200_000 rows). Record count and null % are then approximate but usually enough for schema and quality checks.

**Full scan:** When you need exact record count or exact distinct for a key. Run once; accept longer run time.

```python
# Optional: profile on sample for large files
df = spark.read.format("csv").option("header", "true").option("encoding", "UTF-8").option("inferSchema", "true").load(path).limit(200_000)
```

---

## Mandatory checklist

| Check | What to record |
|-------|----------------|
| Columns | Names, count, order consistency |
| Record count | Total per file (and later, consistency across stages) |
| Null count per column | Per column; re-check after Bronze cast |
| Structure | Format (CSV/JSON/XML), flat vs nested |
| Column shifts | Eyeball sample; note misaligned columns |
| Schema casting impact | Inferred types; document if new nulls appear after Bronze cast |
| Document findings | profiling_findings.md; raise red flags |

---

## Next steps

- Write findings in **profiling_findings.md** (observations, not code).
- Feed limitations and risks into **docs/01_discovery_and_assumptions.md**.
- Use profiling to decide Bronze schema, null handling, casting, and dedup. Do not jump to transformations until profiling is documented and reviewed.
