---

## Documentation & profiling

- [x] Complete **Requirement Documentation and Assumption** (e.g. docs/01_discovery_and_assumptions.md or equivalent); include scope, limitations, assumptions.
- [X] Complete **Dataset Profiling** (run profiling notebook on raw files; record row counts, columns, nulls, sample); document findings (e.g. profiling_findings.md or in discovery doc).

---

### Dataset Profiling

**Code:** [src/notebooks/Profiling/profile_raw_csvs.py](../../../src/notebooks/Profiling/profile_raw_csvs.py) — run on raw CSVs (widget: `base_path`); outputs row count, columns, null counts, 5 sample rows per file. Catalogs uses semicolon.

**Findings:** [docs/profiling_findings.md](../../../docs/profiling_findings.md) — summary table (row counts, columns, nulls, delimiter) and links to per-file docs (02–06).

---

### Requirement Documentation and Assumption (simple)

**Full doc:** [docs/01_discovery_and_assumptions.md](../../../docs/01_discovery_and_assumptions.md)

- **Scope:** Medallion pipeline (Bronze/Silver/Gold) on 5 CSVs (1_main, 1_photo, 1_text, catalogs, final_geografic). Convert some to JSON/XML per chunking plan. Use Databricks (Volumes, Unity Catalog, Jobs, DABs). KPIs by brand/model/geo/time.
- **Limitations:** Only these 5 CSVs (&lt; 2 GB). No JPGs, no full 33 GB dataset. No single primary key across files. Delimiters/encoding differ per file. Listing data append-only; no update/delete flags.
- **Assumptions:** UTF-8 for Cyrillic. `id` in 1_main = listing key for deduplication. Dates DD.MM.YYYY. Catalogs and final_geografic = reference. Databricks Free Edition (workspace/Volumes only).

---