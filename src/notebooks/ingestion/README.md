# Ingestion — 2-notebook pattern (XML)

For a **one-time XML load**, we first explore and validate the file, then ingest it into Bronze in a separate notebook. Minimal ceremony, no blind ingestion.

| Notebook | Purpose |
|----------|---------|
| **01_xml_understand_validate** | Understand the file: exists, well-formed (ET), structure & schema (Spark XML). No Bronze writes. |
| **02_bronze_ingest_xml** | Ingest: read XML (rowTag from Notebook 1), add _source_file & _ingest_ts, write to Bronze, minimal validation. |

**Widgets**

- **01:** `xml_path`, `row_tag` (default `record`)
- **02:** `xml_path`, `row_tag`, `bronze_table` (default `dev_automotive.bronze.geografic`)

**Note:** If Notebook 2 infers only `_corrupt_record` (no data columns), use `mode FAILFAST` instead of PERMISSIVE + `columnNameOfCorruptRecord`, or provide an explicit schema. See Profiling/README for XML validation options.
