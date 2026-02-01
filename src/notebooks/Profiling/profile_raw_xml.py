# Databricks notebook source
# MAGIC %md
# MAGIC ## Part 3: XML validation (pre–Bronze)
# MAGIC Single read with rowTag. Row count, columns, nulls; fail fast if zero records. **mode FAILFAST** — any corrupt/malformed XML row causes the read to throw (we detect corruption by exception). Requires spark-xml.

# COMMAND ----------

dbutils.widgets.text("base_path", "/Volumes/dev_automotive/landing/landing_raw/", "Base path (volume)")
base_path = dbutils.widgets.get("base_path").strip().rstrip("/")

# COMMAND ----------

# (file_name, row_tag) — rowTag must match XML root element per row (e.g. record)
XML_FILES = [
    ("final_geografic.xml", "record"),
]

# COMMAND ----------

from pyspark.sql import functions as F


def validate_xml(path: str, row_tag: str = "record") -> None:
    """
    Pre-Bronze XML validation (serverless-safe).
    - Single read with rowTag; charset UTF-8; **mode FAILFAST** — any corrupt/malformed row throws (we detect corruption by exception).
    - Row count, columns, nulls per column; fail fast if zero records; sample + pass.
    - Requires spark-xml (com.databricks.spark.xml).
    """
    print(f"\n{'='*60}\nValidating XML: {path}\n{'='*60}")

    df = (
        spark.read
        .format("xml")
        .option("rowTag", row_tag)
        .option("charset", "UTF-8")
        .option("mode", "FAILFAST")
        .load(path)
    )
    cols = df.columns

    if len(cols) == 0:
        raise Exception("❌ XML has zero columns — check rowTag and file structure.")

    stats = (
        df
        .agg(
            F.count("*").alias("row_count"),
            *[F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(f"{c}__null") for c in cols],
        )
        .collect()[0]
    )
    row_count = stats["row_count"]

    if row_count == 0:
        raise Exception("❌ XML has zero records")

    print("[XML READ]")
    print(f"  Rows    : {row_count:,}")
    print(f"  Columns : {len(cols)} (rowTag={row_tag})\n")
    for c in cols:
        print(f"  {c:<12}: nulls = {stats[f'{c}__null']:,}")

    print("\n[SAMPLE]")
    df.select(*cols).limit(5).show(truncate=50)
    print("\n✅ XML PASSED PRE-BRONZE VALIDATION")


# COMMAND ----------

for name, row_tag in XML_FILES:
    path = f"{base_path}/{name}"
    validate_xml(path, row_tag)

# COMMAND ----------

# MAGIC %md
# MAGIC Part 3 (XML) done. Record findings in `docs/profiling_findings.md`. Use for pre–Bronze validation only.
