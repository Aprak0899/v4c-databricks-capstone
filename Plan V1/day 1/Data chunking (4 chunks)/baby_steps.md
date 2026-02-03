# Data chunking — Baby steps

Check each step in order. Use this to complete every point in [Data chunking.md](Data%20chunking.md).

---

## 1. Chunk 1 — First-time load to CSV (full load)

- [x] **1.1** Decide which raw CSV files are **first-time / full load** (e.g. `1_photo.csv`, `1_text.csv`). List them.
- [x] **1.2** Document in your chunking doc: **Chunk 1 = full load**, and the exact file names (e.g. `1_photo.csv`, `1_text.csv`).
- [x] **1.3** Confirm these files exist in your landing volume (e.g. `/Volumes/dev_automotive/landing/landing_raw/`) and will be ingested as-is (no incremental logic for Chunk 1).

---

## 2. Chunk 2 — Incremental load to CSV

- [x] **2.1** Decide which raw CSV file(s) are **incremental** (e.g. `1_main.csv`). List them.
- [x] **2.2** Choose and document the **incremental strategy** (e.g. column for watermark/CDC, append vs merge, frequency).
- [x] **2.3** Document in your chunking doc: **Chunk 2 = incremental load**, file names, and the strategy (e.g. “1_main.csv — incremental by date column X”).

---

## 3. Chunk 3 — Convert source to JSON and place in volume

- [x] **3.1** Pick the source file for JSON conversion (e.g. `catalogs.csv` → `catalogs.json`). Confirm the CSV exists in the landing volume.
- [x] **3.2** Run your **CSV → JSON** conversion (notebook or job) so that the output is valid JSON.
- [x] **3.3** Write the output to your volume (e.g. same volume path or a dedicated path). Confirm `catalogs.json` (or your chosen name) is present in the volume.
- [x] **3.4** Document in your chunking doc: **Chunk 3** = which file was converted to JSON and where it is stored.

---

## 4. Chunk 4 — Convert source to XML and place in volume

- [x] **4.1** Pick the source file for XML conversion (e.g. `final_geografic.csv` → `final_geografic.xml`). Confirm the CSV exists in the landing volume.
- [x] **4.2** Run your **CSV → XML** conversion (notebook or job) so that the output is valid XML.
- [x] **4.3** Write the output to your volume. Confirm `final_geografic.xml` (or your chosen name) is present in the volume.
- [x] **4.4** Document in your chunking doc: **Chunk 4** = which file was converted to XML and where it is stored.

---

## 5. Document the mapping (chunking doc)

- [x] **5.1** Create or update a **discovery/chunking** document (e.g. `chunking_mapping.md` or a section in your discovery doc).
- [x] **5.2** In that doc, add a clear **mapping table** (or list):
  - Chunk 1: files + “full load”
  - Chunk 2: files + “incremental” + strategy
  - Chunk 3: source file → JSON output + volume path
  - Chunk 4: source file → XML output + volume path
- [x] **5.3** Keep the doc in the repo (e.g. under `Plan V1/day 1/Data chunking (4 chunks)/` or `resources/`) and commit it.

---

## Quick checklist (same 5 points)

| # | Point | Done |
|---|--------|------|
| 1 | Chunk 1: First-time load to CSV (full load) — files assigned and documented |X|
| 2 | Chunk 2: Incremental load to CSV — files and strategy documented |X|
| 3 | Chunk 3: Source → JSON; output in volume; documented |X|
| 4 | Chunk 4: Source → XML; output in volume; documented |X|
| 5 | Chunking mapping doc created/updated and in repo | x |
