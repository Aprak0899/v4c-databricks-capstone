
---

## Data chunking (4 chunks)

- [ ] **Chunk 1:** Assign files for **first-time load to CSV** (e.g. 1_photo.csv, 1_text.csv) — document which files and that it’s full load.
- [ ] **Chunk 2:** Assign files for **incremental load to CSV** (e.g. 1_main.csv) — document which files and incremental strategy.
- [ ] **Chunk 3:** Convert assigned source to **JSON** (e.g. catalogs.csv → catalogs.json); place in volume for later ingestion.
- [ ] **Chunk 4:** Convert assigned source to **XML** (e.g. final_geografic.csv → final_geografic.xml); place in volume for later ingestion.
- [ ] Divide the data into chunks accordingly and document the mapping (e.g. in discovery/chunking doc).

---