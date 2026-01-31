# Data Chunking Job — Baby steps

Check each step in order. Use this to complete the "Create a Job named **Data Chunking**" and "Run the Job once" items in [Notebooks & Job.md](Notebooks%20&%20Job.md).

---

## 1. Create the Job in Databricks (UI)

- [x] **1.1** In your Databricks workspace, go to **Workflows** → **Jobs** → **Create Job**.
- [x] **1.2** Set **Job name** to **Data Chunking** (exactly as required).
- [x] **1.3** Leave **Task name** as the default (e.g. "Task 1") or rename to something clear (e.g. "CSV_to_JSON") — you will add a second task next.

---

## 2. Add Task 1: CSV → JSON (Chunk 3)

- [x] **2.1** In the job editor, for the first task, set **Type** to **Notebook**.
- [x] **2.2** Click **Select notebook** and choose: **Convert CSV Data to JSON with Audit Columns** (under your repo path, e.g. `Repos/<your-folder>/v4c-databricks-capstone/src/notebooks/Chunks/Convert CSV Data to JSON with Audit Columns.ipynb`).
- [x] **2.3** Add **Widget values** (Parameters) so the notebook receives:
  - **input_path:** `/Volumes/dev_automotive/landing/landing_raw/catalogs.csv`
  - **output_path:** `/Volumes/dev_automotive/landing/landing_raw/catalogs.json`
- [x] **2.4** Set **Cluster** to your existing **Serverless** (or shared) cluster, or create a new job cluster (e.g. Serverless).
- [x] **2.5** Save the task (e.g. name it **CSV_to_JSON**).

---

## 3. Add Task 2: CSV → XML (Chunk 4)

- [x] **3.1** Click **Add task** (or **+ Add** below the first task). Create a second task.
- [x] **3.2** Set **Type** to **Notebook**.
- [x] **3.3** Select notebook: **Convert CSV Data to XML with Audit Columns** (same repo path, `.../Chunks/Convert CSV Data to XML with Audit Columns.ipynb`).
- [x] **3.4** Add **Widget values:**
  - **input_path:** `/Volumes/dev_automotive/landing/landing_raw/final_geografic.csv`
  - **output_path:** `/Volumes/dev_automotive/landing/landing_raw/final_geografic.xml`
- [x] **3.5** Set **Cluster** (same as Task 1 or same type).
- [x] **3.6** Set **Depends on** to the first task (e.g. **CSV_to_JSON**) so the pipeline runs in order: JSON first, then XML.
- [x] **3.7** Save the task (e.g. name it **CSV_to_XML**).

---

## 4. Save and run the Job

- [x] **4.1** Click **Save** (or **Create**) to save the **Data Chunking** job.
- [x] **4.2** Click **Run now** to trigger the job once.
- [x] **4.3** Open the **Run** and confirm both tasks complete successfully (green).
- [x] **4.4** In **Catalog Explorer** → volume `dev_automotive.landing.landing_raw`, confirm **catalogs.json** and **final_geografic.xml** are present and updated (optional but recommended).

---

## 5. Optional: Define the Job in DABs (`databricks.yml`)

If you want the job to be deployed via Git / CI-CD (Databricks Asset Bundles), add a job definition under `resources.jobs` in **databricks.yml** that references the same two notebooks and passes the same widget values. You can do this after the UI job works.

- [x] **5.1** Open **databricks.yml** at the repo root.
- [x] **5.2** Under `resources.jobs`, add a job named `data_chunking` (or `data-chunking`) with two tasks: one for the JSON notebook (with `input_path` / `output_path` for catalogs), one for the XML notebook (with paths for final_geografic), and `task_key` dependencies so XML runs after JSON.
- [ ] **5.3** Run `databricks bundle validate -t dev` (if you have the CLI) and deploy when ready.

---

## Quick checklist

| # | Step | Done |
|---|------|------|
| 1 | Create Job in Databricks UI, name = **Data Chunking** | x |
| 2 | Task 1: CSV → JSON notebook + widget paths (catalogs) | x |
| 3 | Task 2: CSV → XML notebook + widget paths (final_geografic), depends on Task 1 | x |
| 4 | Save job, Run now, confirm both tasks pass | x |
| 5 | (Optional) Add job to databricks.yml for DABs | x |
