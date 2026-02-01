# Databricks notebook source
# MAGIC %md
# MAGIC ## Part 2: JSON validation (pre–Bronze)
# MAGIC Single read (multiLine). Row count, columns, nulls; fail fast if zero records. Serverless-safe.

# COMMAND ----------

dbutils.widgets.text("base_path", "/Volumes/dev_automotive/landing/landing_raw/", "Base path (volume)")
base_path = dbutils.widgets.get("base_path").strip().rstrip("/")

# COMMAND ----------

JSON_FILES = [
    "catalogs.json",
]

# COMMAND ----------

from pyspark.sql import functions as F


def validate_json(path: str) -> None:
    """
    Pre-Bronze JSON validation (serverless-safe).
    - Single read (multiLine supported)
    - Row count, columns, nulls per column
    - Fail fast if zero records; sample + pass
    """
    print(f"\n{'='*60}\nValidating JSON: {path}\n{'='*60}")

    df = (
        spark.read
        .option("multiLine", True)
        .option("encoding", "utf-8")
        .json(path)
    )
    cols = df.columns
    stats = (
        df
        .agg(
            F.count("*").alias("row_count"),
            *[
                F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(f"{c}__null")
                for c in cols
            ]
        )
        .collect()[0]
    )
    row_count = stats["row_count"]

    if row_count == 0:
        raise Exception("❌ JSON has zero records")

    print("[JSON READ]")
    print(f"  Rows    : {row_count:,}")
    print(f"  Columns : {len(cols)}\n")
    for c in cols:
        print(f"  {c:<12}: nulls = {stats[f'{c}__null']:,}")

    print("\n[SAMPLE]")
    df.limit(5).show(truncate=50)
    print("\n✅ JSON PASSED PRE-BRONZE VALIDATION")


# COMMAND ----------

for name in JSON_FILES:
    path = f"{base_path}/{name}"
    validate_json(path)

# COMMAND ----------

# MAGIC %md
# MAGIC Part 2 (JSON) done. Run Part 1 (CSV) and Part 3 (XML) via main notebook or separately.
