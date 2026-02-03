# Day 1 — File checklist

Verification that all files/folders required for Day 1 deliverables are present in the project (excluding `local/`).

**Status:** ✅ Day 1 completed — all files present; feature/data-profiling merged to dev.

---

## 1. Repo structure (DABs)

| Required | Location | Status |
|----------|----------|--------|
| `.github/workflows/` | `.github/workflows/databricks-ci-cd.yml` | ✅ Present |
| `databricks.yml` | Root | ✅ Present |
| `src/` (notebooks, pipelines, jobs) | `src/` | ✅ Present |
| `tests/` | `tests/` | ✅ Present |
| `resources/` | `resources/` | ✅ Present |
| `README.md` | Root | ✅ Present |

---

## 2. Requirement Documentation and Assumption

| Required | Location | Status |
|----------|----------|--------|
| Requirement doc (scope, limitations, assumptions) | `Plan V1/Project Req/project_requirements.md` | ✅ Present (equivalent to docs/01_discovery_and_assumptions.md) |

**Note:** If you prefer a root-level `docs/01_discovery_and_assumptions.md`, that would live under `local/docs/` (ignored). Current equivalent is in Plan V1.

---

## 3. Dataset Profiling

| Required | Location | Status |
|----------|----------|--------|
| Profiling notebook (run on raw files) | `src/jobs/chunk 1 ingestion CSV/profile_raw_csv.ipynb` | ✅ Present |
| Document findings (row counts, columns, nulls, sample) | `Plan V1/day 1/Documentation & profiling/Documentation & profiling.md` | ✅ Present |

---

## 4. Data Chunking — notebooks and job

| Required | Location | Status |
|----------|----------|--------|
| Notebook: CSV → JSON | `src/notebooks/Chunks/Convert CSV Data to JSON with Audit Columns.ipynb` | ✅ Present |
| Notebook: CSV → XML | `src/notebooks/Chunks/Convert CSV Data to XML with Audit Columns.ipynb` | ✅ Present |
| Chunk 1 (first-time CSV) / profiling | `src/jobs/chunk 1 ingestion CSV/profile_raw_csv.ipynb` | ✅ Present |
| Chunk 3 (JSON) | `src/jobs/chunk 3 ingestion JSON/01_profile_raw_json.ipynb` | ✅ Present |
| Chunk 4 (XML) | `src/jobs/chunk 4 ingestion XML/01_profile_raw_xml.ipynb`, `02_bronze_ingest_xml.ipynb` | ✅ Present |
| Job "Data Chunking" | In Databricks (not a repo file) | ✅ Confirmed earlier |

---

## 5. Chunking documentation

| Required | Location | Status |
|----------|----------|--------|
| Chunk mapping / discovery | `Plan V1/day 1/Data chunking (4 chunks)/chunking_mapping.md`, `Data chunking.md` | ✅ Present |

---

## 6. Summary

| Deliverable | Files / location | Status |
|-------------|------------------|--------|
| Repo structure | .github, databricks.yml, src, tests, resources, README.md | ✅ All present |
| Requirement Documentation | Plan V1/Project Req/project_requirements.md | ✅ Present |
| Dataset Profiling | src/jobs/…/profile_raw_csv.ipynb + Plan V1/…/Documentation & profiling | ✅ Present |
| Data Chunking notebooks + Job | Chunks (CSV→JSON, CSV→XML), jobs (chunk 1, 3, 4), Job in Databricks | ✅ Present |
| Chunking documentation | Plan V1/day 1/Data chunking (4 chunks)/ | ✅ Present |
| Multiple run scenarios | Notebooks use overwrite / idempotent logic | ✅ Verified |

---

## 7. Commit scope reminder

`.gitignore` is set so that only these are committed:

- `.github/`
- `resources/`
- `src/`
- `tests/`
- `databricks.yml`
- `README.md`
- `.gitignore`

`Plan V1/` and `FOLDER_AND_NAMING_REVIEW.md` are **not** in `.gitignore`, so they **will** be committed if you `git add` them. If you want Requirement Doc and profiling/chunking documentation to be in the repo, either:

- Keep committing `Plan V1/`, or  
- Add a committed docs location (e.g. `docs/` at root, with `01_discovery_and_assumptions.md` and profiling findings) and keep `Plan V1/` local-only by adding `Plan V1/` to `.gitignore`.

---

**Verdict:** All files required for Day 1 are present in the project. Only remaining action item from action_items.md is: **Merge feature/data-profiling into dev** (and optionally confirm the GitHub Actions workflow runs on push to dev).
