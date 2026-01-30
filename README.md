# v4c-databricks-capstone

## Repository structure (DABs-style)

```
v4c-databricks-capstone/
├── .gitignore
├── README.md
├── databricks.yml              # asset bundle config
├── .github/
│   └── workflows/
│       └── databricks-ci-cd.yml   # (optional) CI/CD for Databricks
├── src/
│   ├── notebooks/              # Databricks notebooks (.ipynb, .py, .scala, .r)
│   ├── pipelines/              # Delta Live Tables (DLT) pipeline definitions
│   └── jobs/                   # Databricks job definitions
├── tests/                      # unit / integration tests
├── resources/                  # config, schemas, static assets for bundles
│
│   # --- ignored (local only, not pushed) ---
│   DataSet/                    # raw CSVs, large data
│   docs/                       # discovery, profiling, assumptions
│   plan/                       # capstone / day plans
│   Orientation/                # recordings, transcripts
```

- **Tracked (pushed):** `src/`, `tests/`, `resources/`, `README.md`, `.gitignore`, `databricks.yml`, and optionally `.github/workflows/`.
- **Ignored (local only):** `DataSet/`, `docs/`, `plan/`, `Orientation/`.

---

## Unity Catalog naming conventions (this project)

Following **&lt;env&gt;_&lt;domain&gt;** and medallion schema patterns.

### Catalog

| Convention | Format | This project |
|------------|--------|--------------|
| Catalog | `<env>_<domain>[_<qualifier>]` | `dev_automotive` |

- **Rationale:** Environment = `dev` (Databricks Free / capstone); domain = `automotive` (car listings). Lowercase, underscores only.

### Schemas

| Convention | Format | This project |
|------------|--------|--------------|
| Medallion | bronze, silver, gold | `landing`, `bronze`, `silver`, `gold` |

- **Rationale:** `landing` holds the volume and raw file references; `bronze` / `silver` / `gold` align with data lifecycle. Two levels only (catalog + schema).

### Volume

| Convention | Purpose | This project |
|------------|---------|--------------|
| Volume | descriptive, lowercase_with_underscores | `landing_raw` |

- **Full path example:** `/Volumes/dev_automotive/landing/landing_raw/`
- Use this volume for initial CSVs and any converted JSON/XML before they are ingested into bronze tables.

### Tables and views

| Type | Format | Examples |
|------|--------|----------|
| Table | `<noun>_<descriptor>` | `listing_main`, `catalog_brand`, `sales_summary` |
| View | prefix `vw_` | `vw_listing_stats`, `vw_customer_orders` |

- Business-centric names; avoid abbreviations unless standard.

### Columns

- **Format:** `lowercase_with_underscores`
- **Sensitive fields:** prefix `pii_` (e.g. `pii_email`)

### Git (already in use)

| Type | Format | This project |
|------|--------|--------------|
| Feature branch | `feature/<feature_name>` | `feature/day1-discovery` |
| Repo | `<team>_<project>_<component>` | `v4c-databricks-capstone` |

---

## Where to store your initial dataset (Databricks Free)

- **Use the project volume** `dev_automotive.landing.landing_raw` for all files you ingest (CSVs, JSON/XML). Create catalog `dev_automotive`, schema `landing`, and volume `landing_raw` in Unity Catalog; put initial files there so jobs and DLT read from one place.
- **Path pattern:** `/Volumes/dev_automotive/landing/landing_raw/<filename>`  
  Example: upload `1_main.csv` → `/Volumes/dev_automotive/landing/landing_raw/1_main.csv`
- **Do not commit the actual data** — keep CSVs in local `DataSet/` (ignored); in Databricks, upload them into the volume via the UI, CLI, or a one-off notebook.

---

## How many catalogs to build

- **One catalog:** `dev_automotive` (env + domain per naming conventions).
- **Four schemas:** `landing`, `bronze`, `silver`, `gold` (medallion + landing for raw files). Full names: `dev_automotive.landing`, `dev_automotive.bronze`, `dev_automotive.silver`, `dev_automotive.gold`.

---

## Keeping files in volumes

- **Yes — keep ingested files in the volume** `landing_raw` inside schema `landing`. Put initial CSVs (and any converted JSON/XML) there.
- **In code:** read using the volume path, e.g. `spark.read.csv("/Volumes/dev_automotive/landing/landing_raw/1_main.csv")`. This keeps data in Unity Catalog and out of the repo.

---

## How to sync with Databricks Free Edition

1. Clone this repo into a Databricks Repo; use the `feature/day1-discovery` branch.
2. Add or edit notebooks under `src/notebooks/`, jobs under `src/jobs/`, and DLT pipelines under `src/pipelines/`; push from Databricks Repo UI or CLI.
3. Keep large CSVs and planning docs in the ignored folders locally; in Databricks, use the volume for data.
4. Run `git status` before committing so only tracked paths are included.

---

## Sanity check (Databricks + Git)

Use this to confirm everything is set up correctly.

### Databricks (Free) — in the workspace

| Check | What to verify |
|-------|----------------|
| **Repo** | Repo `v4c-databricks-capstone` is connected to GitHub and cloned in Workspace. |
| **Branch** | Current branch is `feature/day1-discovery`. |
| **Catalog** | Catalog `dev_automotive` exists (create in Data → Catalogs if not). |
| **Schemas** | Under `dev_automotive`: schemas `landing`, `bronze`, `silver`, `gold` exist. |
| **Volume** | Volume `landing_raw` exists in `dev_automotive.landing` (for CSVs/JSON/XML). |
| **Structure** | Repo shows `README.md`, `src/` (with `notebooks/`, `pipelines/`, `jobs/`), `tests/`, `resources/` after you push. |

If anything is missing on Databricks, create it in Data → Catalogs (catalog → schemas → volume) and ensure the Repo is on `feature/day1-discovery`.

### Git — local repo

| Check | What to verify |
|-------|----------------|
| **Remote** | `origin` points to your GitHub repo (e.g. `.../v4c-databricks-capstone.git`). |
| **Branch** | You are on `feature/day1-discovery`; do not commit directly to `dev` or `main`. |
| **Ignored** | `DataSet/`, `docs/`, `Orientation/`, `plan/` do **not** appear in `git status`. |
| **Tracked** | Only `README.md`, `.gitignore`, `src/`, `tests/`, `resources/` (and optionally `databricks.yml`, `.github/`) are added/committed. |
| **Push** | After commit, push to `origin feature/day1-discovery`; then Databricks Repo can pull. |

**Quick commands:**  
`git status` — should show no files from DataSet/docs/plan/Orientation.  
`git branch` — current branch should be `feature/day1-discovery`.

---

## Notes

- `databricks.yml` and `resources/` are the right place for asset bundle and deployment config.
- To stop tracking something that was committed from an ignored folder: `git rm --cached <path>` once.
