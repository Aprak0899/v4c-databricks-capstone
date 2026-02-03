# Day 1 — Action items

Check off as you complete. Based on [day1_deliverables.md](day1_deliverables.md).

---

## ✅ Day 1 completed

All deliverables done. **feature/data-profiling** merged into **dev**. Ready for Day 2.

---

## Git & repository

- [x] Create or confirm PRIVATE GitHub repository **vstone-databricks-pipeline** (or get approval for current repo name).
- [x] Ensure repo has DABs structure: `.github/workflows/`, `databricks.yml`, `src/` (notebooks, pipelines, jobs), `tests/`, `resources/`, `README.md`.
- [x] Create branch **feature/data-profiling** and do all Day 1 work on it (no direct commits to main/dev).
- [x] After Day 1 is tested and error-free: merge **feature/data-profiling** into **dev**.

---

## CI/CD

- [X] Add **databricks.yml** at repo root (DABs bundle config).
- [X] Add **.github/workflows/databricks-ci-cd.yml** (or equivalent) for GitHub Actions.
- [ ] Confirm workflow runs on push/merge (e.g. to dev) as required.

---

## Databricks workspace

- [x] Configure Databricks Git integration (repo connected, no VSCode required).
- [x] Ensure workspace uses **Databricks Free Edition** (no DBX trial).
- [x] Create or confirm **Shared Cluster** (or cluster used for notebooks/jobs).
- [x] Create or confirm **Unity Catalog**: catalog, schemas (e.g. landing, bronze, silver, gold), and **mount/volume** for raw data.
- [x] Land raw datasets into **Volumes** (all CSVs/JSON/XML in the volume path you use for ingestion).

---

## Data chunking (4 chunks)

- [x] **Chunk 1:** Assign files for **first-time load to CSV** (e.g. 1_photo.csv, 1_text.csv) — document which files and that it’s full load.
- [x] **Chunk 2:** Assign files for **incremental load to CSV** (e.g. 1_main.csv) — document which files and incremental strategy.
- [x] **Chunk 3:** Convert assigned source to **JSON** (e.g. catalogs.csv → catalogs.json); place in volume for later ingestion.
- [x] **Chunk 4:** Convert assigned source to **XML** (e.g. final_geografic.csv → final_geografic.xml); place in volume for later ingestion.
- [x] Divide the data into chunks accordingly and document the mapping (e.g. in discovery/chunking doc).

---

## Notebooks & Job

- [x] Implement or confirm **notebook(s)** for chunking/conversion pipeline (CSV→JSON, CSV→XML, and any first-time/incremental CSV logic as required for Day 1).
- [x] Ensure **notebook code handles multiple run scenarios** (idempotent: re-run does not duplicate data; use overwrite or MERGE as appropriate).
- [x] In Databricks, create a **Job** named **Data Chunking** that runs the above pipeline (notebooks).
- [x] Run the Job once and confirm it completes without error.

---

## Documentation & profiling

- [X] Complete **Requirement Documentation and Assumption** (e.g. docs/01_discovery_and_assumptions.md or equivalent); include scope, limitations, assumptions.
- [X] Complete **Dataset Profiling** (run profiling notebook on raw files; record row counts, columns, nulls, sample); document findings (e.g. profiling_findings.md or in discovery doc).

---

## Sign-off before merge to dev

- [x] All Day 1 deliverables present: repo structure, Git integration, GitHub Actions, databricks.yml, Requirement Doc, Dataset Profiling, Data Chunking notebook + Job, multiple run scenarios.
- [x] Code on **feature/data-profiling** is tested and error-free (Job ran successfully; notebooks verified idempotent).
- [X] Merge **feature/data-profiling** into **dev**.

---

## Quick reference — Day 1 deliverables

| Deliverable | Done |
|-------------|------|
| PRIVATE GitHub repo vstone-databricks-pipeline with proper structure | Yes |
| Working Git integration with Databricks | Yes |
| Initial GitHub Actions workflow | Yes |
| databricks.yml configuration | Yes |
| Requirement Documentation and Assumption | Yes |
| Dataset Profiling | Yes |
| A notebook and a Job (Job Name: Data Chunking) | Yes |
| Git: feature/data-profiling merged to dev after testing | Yes |
| Notebook code handles multiple run scenarios | Yes |
