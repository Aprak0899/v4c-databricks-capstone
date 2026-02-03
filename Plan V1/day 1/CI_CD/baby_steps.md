# CI/CD — Baby steps

Check each step in order. Use this to complete every point in [CI_CD.md](CI_CD.md).

---

## 1. Add **databricks.yml** at repo root (DABs bundle config)

- [x] **1.1** In your project root (same folder as README.md), confirm file **`databricks.yml`** exists.
- [x] **1.2** Open `databricks.yml` and confirm it has at least: **`bundle.name`** and **`targets.dev.workspace.host`** (your Databricks workspace URL).
- [x] **1.3** If you use **resources.jobs**, ensure the YAML is valid (no syntax errors). Optionally run `databricks bundle validate -t dev` from the repo root (requires Databricks CLI) to validate.
- [x] **1.4** Commit and push `databricks.yml` on your feature branch so it is in the repo.

---

## 2. Add **.github/workflows/databricks-ci-cd.yml** (or equivalent) for GitHub Actions

- [x] **2.1** In your project root, confirm folder **`.github/workflows/`** exists (create it if not).
- [x] **2.2** Confirm file **`.github/workflows/databricks-ci-cd.yml`** exists (create it if not).
- [x] **2.3** Open the workflow file and confirm it has: **`name`** (e.g. "Databricks CI/CD"), **`on`** (e.g. `push: branches: [dev]` and/or `workflow_dispatch`), and a **`jobs`** section with at least one step (e.g. checkout, check for databricks.yml).
- [x] **2.4** Ensure the workflow does not reference secrets or deploy steps until you have configured them (a minimal "check bundle exists" step is enough for Day 1).
- [x] **2.5** Commit and push `.github/workflows/databricks-ci-cd.yml` on your feature branch so it is in the repo.

---

## 3. Confirm workflow runs on push/merge (e.g. to dev) as required

- [X] **3.1** On GitHub, open your repo → **Actions** tab. Confirm the workflow **"Databricks CI/CD"** (or your workflow name) appears in the list.
- [X] **3.2** Merge **feature/data-profiling** into **dev** (or push a commit to **dev**). The workflow is set to run on **push to dev**.
- [X] **3.3** In **Actions**, open the latest run. Confirm it started (trigger: push to dev) and that the **"Check bundle"** step (or equivalent) passed (e.g. "databricks.yml found").
- [X] **3.4** If the run failed, fix the reported error (e.g. missing file, YAML syntax) and push again; re-check the run.
- [X] **3.5** Optional: Trigger manually via **workflow_dispatch** (Actions → select workflow → Run workflow) and confirm it runs.

---

## Quick checklist (same 3 points)

| # | Point | Done |
|---|--------|------|
| 1 | databricks.yml at repo root (DABs bundle config) |x|
| 2 | .github/workflows/databricks-ci-cd.yml for GitHub Actions |x|
| 3 | Workflow runs on push/merge to dev; run confirmed in Actions |X|
