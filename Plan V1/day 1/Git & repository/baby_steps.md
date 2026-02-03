# Git & repository — Baby steps

Check each step in order. Use this to verify every point in [Git & repository.md](Git%20%26%20repository.md).

---

## 1. Create or confirm PRIVATE GitHub repository **vstone-databricks-pipeline**

- [x] **1.1** Log in to GitHub.
- [x] **1.2** Check if you already have a repo named **vstone-databricks-pipeline**. If yes, go to 1.5.
- [x] **1.3** If not: click **New repository** (or + → New repository).
- [x] **1.4** Set repository name to **vstone-databricks-pipeline**. Set visibility to **Private**. Create the repository (you can leave README/.gitignore empty and add from local later).
- [x] **1.5** Copy the repo URL (e.g. `https://github.com/YOUR_USERNAME/vstone-databricks-pipeline.git`).
- [x] **1.6** If you use a different repo name (e.g. v4c-databricks-capstone), get written approval from L&D and note it; then use that repo URL for the rest.

---

## 2. Ensure repo has DABs structure

- [x] **2.1** In your project root, confirm folder **`.github/workflows/`** exists. If not, create it.
- [x] **2.2** Confirm file **`databricks.yml`** exists at repo root. If not, add it (DABs bundle config).
- [x] **2.3** Confirm folder **`src/`** exists. Under `src/`, confirm **`notebooks/`**, **`pipelines/`**, **`jobs/`** exist (create if missing).
- [x] **2.4** Confirm folder **`tests/`** exists.
- [x] **2.5** Confirm folder **`resources/`** exists.
- [x] **2.6** Confirm **`README.md`** exists at repo root.
- [x] **2.7** Run `git status` (or list dirs) and verify: `.github/workflows/`, `databricks.yml`, `src/` (with notebooks, pipelines, jobs), `tests/`, `resources/`, `README.md`.

---

## 3. Create branch **feature/data-profiling** and do all Day 1 work on it

- [x] **3.1** Open a terminal in your project root. Run `git status`. Ensure you are on **dev** or **main** (and have a clean or committed state).
- [x] **3.2** Create branch: `git checkout -b feature/data-profiling` (or `git switch -c feature/data-profiling`).
- [x] **3.3** Confirm current branch: `git branch` — you should see `* feature/data-profiling`.
- [ ] **3.4** Do all Day 1 work (notebooks, databricks.yml, workflows, profiling, chunking, Job) on this branch. Do **not** commit directly to **main** or **dev**.
- [ ] **3.5** Commit and push: `git add .` (only intended files), `git commit -m "Day 1: ..."`, `git push -u origin feature/data-profiling`.
- [x] **3.6** In Databricks Repo settings, ensure the repo is connected to the same GitHub repo and that you can switch to **feature/data-profiling** there if you work from Databricks.

---

## 4. After Day 1 is tested and error-free: merge **feature/data-profiling** into **dev**

- [ ] **4.1** Confirm all Day 1 deliverables are done and tested (repo structure, databricks.yml, GitHub Actions, Requirement Doc, Dataset Profiling, Data Chunking notebook + Job, multiple run scenarios).
- [ ] **4.2** Ensure **feature/data-profiling** is pushed: `git push origin feature/data-profiling`.
- [ ] **4.3** Switch to **dev**: `git checkout dev` (or `git switch dev`). Pull latest: `git pull origin dev`.
- [ ] **4.4** Merge: `git merge feature/data-profiling` (resolve any conflicts if needed).
- [ ] **4.5** Push **dev**: `git push origin dev`.
- [ ] **4.6** Confirm on GitHub (or `git log`) that **dev** now contains the Day 1 work. Optionally delete or keep **feature/data-profiling** branch.

---

## Quick checklist (same 4 points)

| # | Point | Done |
|---|--------|------|
| 1 | Create or confirm PRIVATE repo **vstone-databricks-pipeline** (or approved name) | [x] |
| 2 | Repo has DABs structure: .github/workflows, databricks.yml, src/(notebooks, pipelines, jobs), tests, resources, README.md | [x] |
| 3 | Branch **feature/data-profiling** created; all Day 1 work on it; pushed | |
| 4 | **feature/data-profiling** merged into **dev** after testing | |
