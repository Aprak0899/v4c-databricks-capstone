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
