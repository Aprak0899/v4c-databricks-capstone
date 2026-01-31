# Internal Project - Databricks

**copyright@vasu.c.bajaj@outlook.com**  
**Version 6.0 | Date: January 28 2026**

---

## Project Details

The associates will design and implement an end-to-end data pipeline on Databricks using a medallion architecture (Bronze → Silver → Gold) to integrate data from multiple formats (CSV, JSON, XML).

The business objective is to provide Business Analytics.

- Ingest multi-format data into a Bronze layer (landing).
- Clean/standardize data into Silver layer.
- Model and aggregate into Gold layer.
- Use Unity Catalog for governance.
- Implement Row Level Security, Column Level Security and Dynamic Data Masking
- Orchestrate pipelines via Databricks Jobs.
- Add unit tests, monitoring

**Please note:**

1. This is an individual project, please do not use common code base. The groups are assigned only to facilitate common connects, evaluations.
2. All the dataset files (Except the metadata files) needs to be ingested till the Gold layer model
3. Data model must be in the Gold Layer
4. Data Model must include the relationships between the PK and FK
5. Audit columns mandatory in all layers

---

## Environments

**Databricks Free Edition** (DO NOT USE DBX TRIAL VERSION)

---

## Deliverable Standards

- Code standards, naming conventions as per best practices are implicit
- Unit testing and evidence collection are applicable to all code being used
- Sanity check for pipelines for each ingestion
- Framework methodology - Reusable components (Preferred)
- No HARD CODING - USE Variables wherever possible
- Email Notification for all code failures (Optional, but Preferred)
- Jobs deployable using DABs

---

## Data Modelling Details

- Design and implement scalable data models using Delta Lake to manage large datasets.
- **Primary Strategy:** Use Liquid Clustering for modern optimization (recommended approach)
- **Comparative Analysis:** Implement both Liquid Clustering and traditional partitioning/Z-ordering to demonstrate performance differences
- Document benefits of Liquid Clustering over Partitioning and ZOrder with benchmarking results
- Design Dimensional Models for analytical workloads, ensuring efficient querying and aggregation.

---

## Git Integration & CI/CD Details

- **Repository:** Create PRIVATE GitHub repository named **vstone-databricks-pipeline**
- **Git Workflow:** Configure Databricks Git integration (without VSCode) for version control
- **Branch Strategy:** Create feature branches for each milestone:
  - feature/data-profiling
  - feature/bronze-layer
  - feature/silver-layer
  - feature/gold-layer
- **Merge Policy:** Merge to **dev** branch only after milestone completion with error-free code
- **DABs Integration:** Use Databricks Asset Bundles for deployment automation
- **GitHub Actions:** Implement CI/CD pipeline for automated testing and deployment
- **Repository Structure:** Organize code with proper folder structure for DABs compatibility

---

## Unit Testing & Performance Optimization Details

- Choose the appropriate configs for environments and dependencies, high memory for notebook tasks, and auto-optimization to disallow retries.
- Develop unit and integration tests using assertDataFrameEqual, assertSchemaEqual, DataFrame.transform, and testing frameworks, to ensure code correctness, including a built-in debugger

---

## Git Setup & Repository Structure

### Initial Setup

```
# Repository structure for DABs
project-root/
├── .github/
│   └── workflows/
│       └── databricks-ci-cd.yml
├── databricks.yml
├── src/
│   ├── notebooks/
│   ├── pipelines/
│   └── jobs/
├── tests/
├── resources/
└── README.md
```

### Branch Strategy

1. **Main Branch:** main - Production ready code
2. **Development Branch:** dev - Integration branch
3. **Feature Branches:**
   - feature/data-profiling
   - feature/bronze-layer
   - feature/silver-layer
   - feature/gold-layer

### Merge Requirements

- All feature branches must pass unit tests
- Code review required before merging to dev
- No direct commits to main branch
- Automated deployment via GitHub Actions

---

## Project Deliverables by Day

### Day 1

- **Git & CI/CD Setup:** Create PRIVATE GitHub repository **vstone-databricks-pipeline** with proper structure, configure Databricks Git integration, create initial **databricks.yml** for DABs, setup GitHub Actions workflow
- Project kickoff, architecture overview (Medallion, Unity Catalog, Jobs).
- Setup Databricks workspace, clusters [Shared Cluster], Unity Catalog, and mount storage.
- Land raw datasets into Volumes
- Break the dataset into chunks (4) so that
  - chunk 1 is used for first time load to CSV
  - chunk 2 for incremental to CSV
  - chunk 3 to be converted to JSON format
  - chunk 4 to be converted to XML format
- Separate Job for the above pipeline
- **Git:** Create and work in **feature/data-profiling** branch
- Divide the data in the chunks accordingly

**Deliverables**

- PRIVATE GitHub repository vstone-databricks-pipeline with proper structure
- Working Git integration with Databricks
- Initial GitHub Actions workflow
- databricks.yml configuration
- Requirement Documentation and Assumption
- Dataset Profiling
- A notebook and a Job (Job Name: Data Chunking)
- Git: Merge feature/data-profiling to dev after testing
- Notebook code must handle multiple run scenarios

---

### Day 2

- **Git:** Create and work in **feature/bronze-layer** branch
- Ingest CSV (transactions) into Bronze (Delta) Using Copy INTO Command
- Apply schema enforcement & add audit columns (load_dt, source).
- Create and add descriptions/metadata about enterprise data to make it more discoverable.
- Job for the above pipeline and should be part of DABs

**Deliverables**

- Unit Testing Results
- Git: Commit to feature/bronze-layer branch

---

### Day 3

- **Git:** Continue in **feature/bronze-layer** branch
- Ingest JSON data into Bronze using Auto Loader
- Ingest XML data into Bronze using Pyspark read and write commands
- Ingest CSV data (2nd Part) into Bronze using Delta Live Tables
- Create and add descriptions/metadata about enterprise data to make it more discoverable.
- Job for the above pipeline and should be part of DABs

**Deliverables**

- Unit Testing Results
- databricks.yml
- Git: Merge feature/bronze-layer to dev after testing

---

### Day 4 (Evaluation 1)

**Evaluation 1 Deliverables Checklist**

- Deliver working ingestion pipelines for all three formats.
- Check: schema validation, error handling, audit columns, data landed in Unity Catalog Bronze.
- Individual assessment.

| Day | Deliverable |
|-----|-------------|
| Day 1 | PRIVATE GitHub repository vstone-databricks-pipeline setup, Databricks Git integration, GitHub Actions workflow, Initial databricks.yml, Databricks Free Edition (No Deviation from the Free Edition Unless explicitly approved by L&D Team), Requirement Documentation and Assumption, Dataset Profiling, A notebook and a Job (Job Name: Data Chunking), Notebook code must handle multiple run scenarios, Git: feature/data-profiling merged to dev |
| Day 2 & 3 | CSV (transactions) into Bronze (Delta) using COPY INTO command, JSON data into Bronze using Auto Loader, XML data into Bronze using PySpark read/write commands, CSV data (4th Part) into Bronze using Delta Live Tables, Unit Testing Results, Git: feature/bronze-layer merged to dev |
| Day 4 | Silver Layer |

---

### Day 4 - Silver Layer

- **Git:** Create and work in **feature/silver-layer** branch
- Transform Bronze → Silver: clean nulls, dedupe, standardize column names.
- Manage malformed records → quarantine.
- Develop User-Defined Functions (UDFs) using Pandas/Python UDF to standardize DataFrame/Table headers
- Create and add descriptions/metadata about enterprise data to make it more discoverable.
- Job for the above pipeline and should be part of DABs

**Deliverables**

- Demo
- Code & Unit Testing Results
- UDF documented
- databricks.yml
- Git: Commit to feature/silver-layer branch

---

### Day 5: Silver Layer

- **Git:** Continue in **feature/silver-layer** branch
- Apply business rules (currency normalization, date standardization).
- Demonstrate Delta Lake ACID, time travel.

**Deliverables**

- Code & Unit Testing Results
- Document with evidence for time travel
- Git: Merge feature/silver-layer to dev after testing

---

### Day 6: Checkpoint - Gold Layer Schema discussion

#### Day 6.A: (Use Delta Live Tables for Gold Layer)

- **Git:** Create and work in **feature/gold-layer** branch
- Build Gold Model - Fact and Dimensions (SCD2 dimensions, wherever applicable)

#### Day 6.B: (Create Aggregate Layer)

- Create aggregations: eg. Sales by customer, category, region. (choose based on your datasets)
- Top 10 customers by spend.
- Monthly sales trend.
- Job for the above pipeline and should be part of DABs

**Deliverables (For 6.A and 6.B)**

- Data Model, Demo
- Business Glossary
- Code & Testing Documents
- databricks.yml
- Git: Commit to feature/gold-layer branch

---

### Day 7: Performance Optimization & Comparative Analysis

- **Git:** Continue in **feature/gold-layer** branch
- Build as per datasets. eg. Build churn metric (example: customers with no transaction in last 6 months).
- **Optimization Strategy:** Implement BOTH approaches for comparison:
  - **Primary:** Optimize Gold layer with Liquid Clustering (recommended)
  - **Comparative:** Implement traditional partitioning and Z-ordering on duplicate tables
- **Benchmarking:** Document performance differences with query execution times
- Add incremental loads (simulate new data drop).
- Implement upserts (MERGE INTO) for late arriving data (if using standard tables)
- Create and add descriptions/metadata about enterprise data to make it more discoverable.

**Deliverables**

- Code & Unit Testing Results
- Performance Benchmarking
- Git: Merge feature/gold-layer to dev after testing

---

### Day 8-9

- Configure Databricks Jobs to orchestrate pipelines.
- Add monitoring/logging
- Build Databricks SQL dashboard on Gold tables.
- Add access controls via Unity Catalog (row/column level security).
- Resource Usage Analysis
- **Git:** Final integration testing in dev branch

**Deliverables**

- Code
- Documentation (Unit Testing)
- Git: Prepare for production deployment

---

### Day 10 (Final Demo & Submission)

- Submit end-to-end solution.
- Demo pipelines, dashboards, and governance setup.
- Candidate demo of Bronze → Silver → Gold pipeline.
- Must show Unity Catalog objects, Jobs orchestration, testing.
- **Git:** Merge dev to main for production release

**Deliverables**

- Case Study PPT (Walkthrough of Design, Implementation) — sample case study here
- **RLS and CLS Demo is mandatory**
- Gold Layer ER Diagram
- Flow Diagram
- Documentation and comments on code
- Unit testing evidences
- databricks.yml
- Git: Complete Git workflow documentation
- CI/CD: Working GitHub Actions pipeline
