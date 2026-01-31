# Databricks notebook source
# MAGIC %md
# MAGIC # Pre-Bronze data profiling (minimal)
# MAGIC
# MAGIC **Engineering only.** Not EDA, not data science.
# MAGIC
# MAGIC **Checks:** File readability, record count, column names and order, schema (inferred), null count per column (single Spark pass), sample rows.
# MAGIC
# MAGIC **After run:** Eyeball sample for CSV malformation (column shift, delimiter/qualifier). Document findings in profiling_findings.md. One run only.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Config — BASE_PATH and list of CSV files

# COMMAND ----------

dbutils.widgets.text(
    "base_path",
    "/Volumes/dev_automotive/landing/landing_raw/",
    "BASE_PATH (UC volume or DBFS, end with /)",
)
BASE_PATH = dbutils.widgets.get("base_path").strip().rstrip("/") + "/"

DATA_FILES = [
    "1_main.csv",
    "1_photo.csv",
    "1_text.csv",
    "catalogs.csv",
    "final_geografic.csv",
]

print(f"BASE_PATH: {BASE_PATH}")
print(f"Files: {DATA_FILES}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Loop — for each CSV: read, count, columns, schema, nulls, sample

# COMMAND ----------

from pyspark.sql import functions as F

for file in DATA_FILES:
    print(f"\n========== Profiling {file} ==========")

    if not file.lower().endswith(".csv"):
        print("WARNING: Not a .csv file. Skipping.")
        print("========================================")
        continue

    full_path = BASE_PATH + file
    df = (
        spark.read
        .format("csv")
        .option("header", "true")
        .option("encoding", "UTF-8")
        .option("inferSchema", "true")
        .load(full_path)
    )

    print("File readability: OK")

    record_count = df.count()
    print(f"Record count: {record_count}")

    if record_count == 0:
        print("ERROR: Empty dataset. Skipping.")
        print("========================================")
        continue

    print("Column names and order:")
    print(df.columns)

    print("Schema (inferred):")
    df.printSchema()

    print("Null count per column (single pass):")
    null_counts = df.agg(
        *[
            F.sum(F.when(F.col(c).isNull(), F.lit(1)).otherwise(F.lit(0))).alias(c)
            for c in df.columns
        ]
    ).collect()[0]
    for c in df.columns:
        print(f"  {c}: {null_counts[c]} nulls")

    print("Sample rows (eyeball for malformation — column shift, delimiter/qualifier):")
    df.show(5, truncate=40)

    print("========================================")

print("\nDone. Document findings in profiling_findings.md.")
