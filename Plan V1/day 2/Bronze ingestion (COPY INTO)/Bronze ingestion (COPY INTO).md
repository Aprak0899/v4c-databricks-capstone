---

## Bronze ingestion (COPY INTO)

- [ ] Ingest **CSV (transactions)** into Bronze as **Delta** using **COPY INTO** (e.g. from landing volume to Bronze table(s)).
- [ ] Apply **schema enforcement** (define and enforce schema on the Bronze Delta table).
- [ ] Add **audit columns**: **load_dt** (load date/time) and **source** (e.g. file or path) to Bronze records.
- [ ] Ensure pipeline is **idempotent** (re-run does not duplicate; use COPY INTO with appropriate options or merge logic).

---