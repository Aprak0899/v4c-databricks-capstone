# Project folder & naming review (excluding `local/`)

**Last checked:** Current structure after your updates.

---

## Current structure (summary)

```
src/
├── jobs/
│   ├── chunk 1 ingestion CSV/     → profile_raw_csv.ipynb
│   ├── chunk 3 ingestion JSON/    → 01_profile_raw_json.ipynb
│   └── chunk 4 ingestion XML/     → 01_profile_raw_xml.ipynb, 02_bronze_ingest_xml.ipynb, Repair XML empty tags.py
├── notebooks/
│   ├── Chunks/                   → Convert CSV→JSON, Convert CSV→XML
│   ├── Profiling/                → ingest_json_bronze_autoloader.py, json read, json_reference_code.py, README
│   └── Utilities/                → Catalog setup, Delete schemas
├── pipelines/   (.gitkeep)
```

**Improvements already made:**
- Data Profiling folder removed; CSV profiling notebook now in `jobs/chunk 1 ingestion CSV`.
- Chunk folders clarified: chunk 1 = CSV, chunk 3 = JSON, chunk 4 = XML.
- No duplicate `profile_raw_csv` notebook; single place per chunk.
- `ingestion/` and profile_raw_*.py scripts removed from notebooks/Profiling.

---

## 1. Remaining naming convention issues

### Folders — use lowercase, hyphen or underscore (no spaces)

| Current | Suggested |
|---------|-----------|
| `chunk 1 ingestion CSV` | `chunk-1-ingestion-csv` |
| `chunk 3 ingestion JSON` | `chunk-3-ingestion-json` |
| `chunk 4 ingestion XML` | `chunk-4-ingestion-xml` |
| `Chunks` | `chunks` |
| `Utilities` | `utilities` |
| `Profiling` | `profiling` (lowercase) |

### Files — use snake_case, clear extension

| Current | Suggested |
|---------|-----------|
| `json read` | `json_read_reference.md` or `json_read_reference.sql` |
| `Repair XML empty tags.py` | `repair_xml_empty_tags.py` |

Notebook names with spaces are fine for Databricks; optional renames only if you want strict consistency.

---

## 2. Redundancy check

- **profile_raw_csv** — Only in `jobs/chunk 1 ingestion CSV/profile_raw_csv.ipynb`. No duplicate. ✓
- **Data Profiling vs Profiling** — Resolved (Data Profiling removed). ✓
- **`json read`** — Still no extension; rename for clarity (see above).

---

## 3. Summary

| Item | Status |
|------|--------|
| Chunk folders (1 CSV, 3 JSON, 4 XML) | Clear; optional: remove spaces → `chunk-1-ingestion-csv` etc. |
| Chunks, Utilities, Profiling | Optional: lowercase → `chunks`, `utilities`, `profiling` |
| `json read` | Rename to `json_read_reference.md` or `.sql` |
| `Repair XML empty tags.py` | Rename to `repair_xml_empty_tags.py` |
| Redundant files | None; structure is clean. |

If you want, next step can be a concrete rename list (old path → new path) or a small script to apply these renames.
