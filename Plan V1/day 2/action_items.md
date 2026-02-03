# Day 2 — Action items

Check off as you complete. Based on [day2_deliverables.md](day2_deliverables.md).

---

## Git

- [ ] Create branch **feature/bronze-layer** and do all Day 2 work on it (no direct commits to main/dev).
- [ ] Commit Bronze pipeline, job, tests, and docs to **feature/bronze-layer**.
- [ ] After Day 2 is tested: merge **feature/bronze-layer** into **dev** (or open PR).

---

## Bronze ingestion (COPY INTO)

- [ ] Ingest **CSV (transactions)** into Bronze as **Delta** using **COPY INTO** (e.g. from landing volume to Bronze table(s)).
- [ ] Apply **schema enforcement** (define and enforce schema on the Bronze Delta table).
- [ ] Add **audit columns**: **load_dt** (load date/time) and **source** (e.g. file or path) to Bronze records.
- [ ] Ensure pipeline is **idempotent** (re-run does not duplicate; use COPY INTO with appropriate options or merge logic).

---

## Discoverability (descriptions / metadata)

- [ ] Add **descriptions** and **metadata** for Bronze tables (e.g. table comment, column comments in Unity Catalog) so enterprise data is more discoverable.
- [ ] Document which tables/columns exist and what they represent (e.g. in README or docs).

---

## Job & DABs

- [ ] Create a **Job** that runs the Bronze ingestion pipeline (notebook(s) or SQL).
- [ ] Add the Bronze **Job to databricks.yml** (DABs) under `resources.jobs` so it is deployed with the bundle.
- [ ] Run the Job once and confirm it completes without error.

---

## Deliverables

- [ ] **Unit testing:** Implement and run unit tests for Bronze logic; capture and document **Unit Testing Results**.
- [ ] **Git:** Commit all Day 2 work to **feature/bronze-layer** branch.

---

## Quick checklist

| # | Area | Done |
|---|------|------|
| 1 | Git: feature/bronze-layer branch, commit, merge/PR | |
| 2 | Bronze: COPY INTO, schema enforcement, audit columns (load_dt, source) | |
| 3 | Descriptions/metadata for discoverability | |
| 4 | Job for Bronze pipeline + in databricks.yml (DABs) | |
| 5 | Unit testing results + commit to feature/bronze-layer | |
