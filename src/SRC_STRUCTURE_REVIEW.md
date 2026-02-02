# src/ folder structure — industry-standard review

**Updated:** Reorganized to match industry layout. Current structure:

```
src/
├── jobs/                           # All job entry points
│   ├── data_chunking/              → csv_to_json.ipynb, csv_to_xml.ipynb (Data Chunking job)
│   ├── chunk_1_ingestion_csv/      → profile_raw_csv.ipynb
│   ├── chunk_3_ingestion_json/     → 01_profile_raw_json.ipynb
│   └── chunk_4_ingestion_xml/      → 01_profile_raw_xml.ipynb, 02_bronze_ingest_xml.ipynb, repair_xml_empty_tags.py
├── notebooks/
│   ├── profiling/                  → json_read_reference.md, README.md
│   ├── utilities/                  → Catalog setup, Delete schemas
│   └── Reference/                  → (existing)
├── lib/                             # Shared Python modules
│   ├── ingest_json_bronze_autoloader.py
│   ├── json_reference_code.py
│   └── README.md
└── pipelines/                       → .gitkeep (empty)
```

---

## Industry-standard expectations

| Folder    | Typical use |
|-----------|-------------|
| **jobs/** | All **job entry points** — notebooks/scripts that a Databricks Job runs. One place for “what runs in a job”. |
| **notebooks/** | Exploratory, shared, or ad-hoc notebooks; or reusable notebooks that jobs call. Not mixed with shared .py libraries. |
| **lib/** or **utils/** | Shared Python modules (.py) used by notebooks or jobs. Importable code. |
| **pipelines/** | DLT pipelines, workflow definitions, or orchestration configs. |

---

## 1. Job entry points in two places

**Current:**  
- **Data Chunking** job (in `databricks.yml`) runs:
  - `src/notebooks/Chunks/Convert CSV Data to JSON with Audit Columns`
  - `src/notebooks/Chunks/Convert CSV Data to XML with Audit Columns`
- **jobs/** contains chunk 1, 3, 4 **ingestion** notebooks (profiling, profile JSON/XML, bronze ingest).

So job-related notebooks live in both **jobs/** and **notebooks/Chunks/**. Industry norm is: **all job entry points under jobs/**.

**Recommendation:**  
- **Option A (recommended):** Move the Data Chunking notebooks into **jobs/** so every job entry point is under `src/jobs/`, e.g.:
  - `src/jobs/data_chunking/csv_to_json.ipynb` (move from notebooks/Chunks/Convert CSV Data to JSON…)
  - `src/jobs/data_chunking/csv_to_xml.ipynb` (move from notebooks/Chunks/Convert CSV Data to XML…)
  - Update `databricks.yml` `notebook_path` to these paths.
  - Then use **notebooks/Chunks/** only for ad-hoc or duplicate copies if needed, or remove if redundant.
- **Option B:** Keep as-is and document: “Data Chunking job runs notebooks from `notebooks/Chunks/`; `jobs/` holds ingestion job notebooks only.”

---

## 2. Python scripts under notebooks/Profiling/

**Current:**  
`src/notebooks/Profiling/` contains:
- `ingest_json_bronze_autoloader.py`
- `json_reference_code.py`
- `json read` (no extension)
- README.md

**Industry norm:**  
Reusable `.py` code lives in a **lib/** or **utils/** (or **common/**) so it can be imported by notebooks/jobs. Notebooks stay in **notebooks/** or **jobs/**; shared code does not sit under **notebooks/**.

**Recommendation:**  
- Add **src/lib/** (or **src/utils/**).
- Move **ingest_json_bronze_autoloader.py** and **json_reference_code.py** to **src/lib/** (e.g. `src/lib/ingest_json_bronze_autoloader.py`, `src/lib/json_reference_code.py`). If any notebook or job imports them, update the import path (e.g. add `src` to `PYTHONPATH` or use a proper package).
- Keep **README.md** in **notebooks/Profiling/** or move to **docs/**; rename **json read** to e.g. **json_read_reference.md** and keep under **notebooks/Profiling/** or move to **docs/**.

---

## 3. jobs/chunk 4 ingestion XML/Repair XML empty tags.py

**Current:**  
One `.py` file next to the chunk 4 notebooks.

**Industry norm:**  
If this script is used only by the notebooks in that folder, co-locating is acceptable. If it is shared across jobs or notebooks, it belongs in **lib/**.

**Recommendation:**  
- If used only by chunk 4 notebooks → keep in place; optionally rename to **repair_xml_empty_tags.py** (snake_case).
- If shared → move to **src/lib/repair_xml_empty_tags.py**.

---

## 4. notebooks/Utilities/

**Current:**  
Catalog setup and “Delete schemas” notebooks.

**Industry norm:**  
Admin/setup notebooks are often under **notebooks/admin**, **notebooks/setup**, or **notebooks/infrastructure**. “Utilities” is fine; lowercase **utilities** is more consistent with common conventions.

**Recommendation:**  
Optional: rename **Utilities** → **utilities** (or **admin** / **setup**). No structural change required.

---

## 5. pipelines/

**Current:**  
Empty (only .gitkeep).

**Industry norm:**  
Used for DLT pipelines, workflow definitions, or pipeline code. Keeping it empty until you add pipelines is standard.

**Recommendation:**  
No change.

---

## 6. Suggested target structure (industry-aligned)

```
src/
├── jobs/                          # All job entry points
│   ├── data_chunking/             # Data Chunking job (move from notebooks/Chunks)
│   │   ├── csv_to_json.ipynb
│   │   └── csv_to_xml.ipynb
│   ├── chunk_1_ingestion_csv/     # Optional: rename for consistency
│   │   └── profile_raw_csv.ipynb
│   ├── chunk_3_ingestion_json/
│   │   └── 01_profile_raw_json.ipynb
│   └── chunk_4_ingestion_xml/
│       ├── 01_profile_raw_xml.ipynb
│       ├── 02_bronze_ingest_xml.ipynb
│       └── repair_xml_empty_tags.py   # OK here if only used by this job
├── notebooks/                     # Exploratory / ad-hoc / shared notebooks
│   ├── profiling/                 # Reference, README; .py moved to lib/
│   │   ├── json_read_reference.md
│   │   └── README.md
│   └── utilities/                 # Admin notebooks (optional rename)
│       ├── catalog_setup_bronze_silver_gold.ipynb
│       └── delete_schemas_catalog_dynamic.ipynb
├── lib/                           # Shared Python modules
│   ├── ingest_json_bronze_autoloader.py
│   └── json_reference_code.py
└── pipelines/                     # DLT / workflow definitions
    └── .gitkeep
```

---

## 7. Summary — are files in the correct folder?

| Location | Current | Industry-aligned? | Action |
|----------|--------|--------------------|--------|
| Data Chunking notebooks (CSV→JSON, CSV→XML) | **notebooks/Chunks/** | No — job entry points usually in **jobs/** | Move to **jobs/data_chunking/** and update **databricks.yml** |
| Chunk 1, 3, 4 ingestion notebooks | **jobs/** | Yes | Optional: rename folders to snake_case |
| Profiling .py scripts | **notebooks/Profiling/** | No — shared code in **lib/** | Move to **src/lib/** |
| Repair XML empty tags.py | **jobs/chunk 4 ingestion XML/** | Yes if only used by that job | Optional: rename to snake_case |
| Utilities notebooks | **notebooks/Utilities/** | Yes | Optional: lowercase **utilities** |
| pipelines/ | Empty | Yes | No change |

**Bottom line:**  
- **Not in the right place by industry standard:** (1) Data Chunking job notebooks should live under **jobs/** (e.g. **jobs/data_chunking/**), and (2) Profiling **.py** files should live under **src/lib/** (or **src/utils/**).  
- Everything else is in a reasonable place; renames (snake_case, lowercase) are optional consistency improvements.

If you want, next step can be a concrete list of moves (old path → new path) and the exact **databricks.yml** changes.
