# Merge feature/data-profiling → dev — Step-by-step

The **merge** is done in **GitHub** (or Git CLI), not in the Databricks UI. Use Databricks for testing before and after.

---

## Part 1: Test in Databricks (before merge)

1. **Open your workspace**  
   `https://dbc-38c502e9-24ad.cloud.databricks.com` (or your dev workspace URL).

2. **Confirm repo is on `feature/data-profiling`**  
   - Go to **Repos** (or **Workspace** → your repo).  
   - Check the branch shown (e.g. in the repo title or branch dropdown).  
   - If it’s not `feature/data-profiling`, switch to it (branch dropdown → **feature/data-profiling**).

3. **Pull latest**  
   - In the repo view, use **Pull** / **Sync** so the repo matches GitHub.

4. **Run the Data Chunking job**  
   - Go to **Workflows** (or **Jobs**) → open the **Data Chunking** job.  
   - Click **Run now**.  
   - Wait until the run completes successfully (both tasks green).

5. **Optional: run again**  
   - Run the job once more to confirm idempotent behavior (no duplicate data).

If all runs succeed, you’re ready to merge.

---

## Part 2: Merge in GitHub (this does the actual merge)

### Option A: Merge via GitHub website (recommended)

1. **Open the repo on GitHub**  
   `https://github.com/Aprak0899/v4c-databricks-capstone`

2. **Create a Pull Request (PR)**  
   - Click **Pull requests** → **New pull request**.  
   - **Base:** `dev`  
   - **Compare:** `feature/data-profiling`  
   - Click **Create pull request**.

3. **Fill in the PR**  
   - Title: e.g. `Merge feature/data-profiling into dev (Day 1 complete)`.  
   - Add a short description (e.g. “Day 1 deliverables: Data Chunking job, profiling, DABs variables”).  
   - Click **Create pull request**.

4. **Review and merge**  
   - Check the **Files changed** tab.  
   - When satisfied, click **Merge pull request** (choose “Merge commit” or “Squash and merge” as you prefer).  
   - Confirm **Confirm merge**.

5. **Optional: delete the branch**  
   - After merge, GitHub may show “Delete branch”; you can delete `feature/data-profiling` if you don’t need it anymore.

---

### Option B: Merge via Git CLI (local)

1. **Open a terminal** in your project folder (e.g. `D:\v4c project`).

2. **Fetch and switch to dev**  
   ```bash
   git fetch origin
   git checkout dev
   git pull origin dev
   ```

3. **Merge the feature branch**  
   ```bash
   git merge origin/feature/data-profiling -m "Merge feature/data-profiling into dev (Day 1)"
   ```

4. **Push dev**  
   ```bash
   git push origin dev
   ```

5. **Optional: switch back to feature branch**  
   ```bash
   git checkout feature/data-profiling
   ```

---

## Part 3: After merge (Databricks + CI/CD)

1. **Databricks: point repo to `dev`**  
   - In **Repos** (or Workspace → repo), use the branch dropdown.  
   - Switch to **dev**.  
   - Use **Pull** / **Sync** so the workspace has the latest `dev` (including the merge).

2. **Confirm Data Chunking still works**  
   - In **Workflows** → **Data Chunking**, run the job again.  
   - It should still run successfully (same code, now on `dev`).

3. **Check GitHub Actions (if you use it)**  
   - On GitHub: **Actions** tab.  
   - Your workflow runs on push to `dev`; confirm the latest run for `dev` is green.

---

## Quick reference

| Step | Where | Action |
|------|--------|--------|
| 1. Test job | Databricks UI | Repos → branch `feature/data-profiling` → Workflows → Data Chunking → Run now |
| 2. Merge | GitHub | Pull requests → New PR (base: dev, compare: feature/data-profiling) → Merge |
| 3. Sync | Databricks UI | Repos → switch to `dev` → Pull |
| 4. Verify | Databricks UI | Workflows → Data Chunking → Run now |

---

**Note:** The “Git: feature/data-profiling merged to dev after testing” deliverable is completed once the PR is merged (Option A) or you’ve pushed the merge to `dev` (Option B). Databricks UI is used for testing and syncing the branch, not for performing the merge.
