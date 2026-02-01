# Databricks notebook source
# MAGIC %md
# MAGIC # Notebook 1 — XML Understanding & Validation
# MAGIC **Purpose:**
# MAGIC - Confirm the XML file is readable
# MAGIC - Validate it is well-formed (not malformed)
# MAGIC - Understand structure & schema
# MAGIC
# MAGIC **No Bronze writes. One-time profiling only.**

# COMMAND ----------

# Widget for XML path (Volume)
dbutils.widgets.text(
    "xml_path",
    "/Volumes/dev_automotive/landing/landing_raw/final_geografic.xml",
    "XML file path (volume)",
)
xml_path = dbutils.widgets.get("xml_path").strip()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. File existence & readability (Spark-level)

# COMMAND ----------

df_text = spark.read.text(xml_path)
line_count = df_text.count()

assert line_count > 0, "❌ XML file is empty or not readable by Spark"
print(f"✅ File readable by Spark. Line count: {line_count:,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Structural validation — strict XML (serverless-safe)

# COMMAND ----------

import xml.etree.ElementTree as ET

def is_valid_xml(volume_path: str) -> bool:
    """
    Validates whether an XML file is well-formed.
    Uses Python XML parser (no Spark, no RDDs, no collect).
    Suitable for one-time loads on Serverless.
    """
    dbfs_path = volume_path.replace("/Volumes", "/dbfs/Volumes")
    try:
        ET.parse(dbfs_path)
        return True
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        return False

assert is_valid_xml(xml_path), "❌ Malformed XML file detected"
print("✅ XML is well-formed")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Structure & schema discovery (Spark XML)

# COMMAND ----------

dbutils.widgets.text("row_tag", "record", "rowTag (element per row)")
row_tag = dbutils.widgets.get("row_tag").strip()

sample_df = (
    spark.read
        .format("xml")
        .option("rowTag", row_tag)
        .option("charset", "UTF-8")
        .option("inferSchema", True)
        .load(xml_path)
)

print(f"Row tag used: {row_tag}")

print("\nSchema:")
sample_df.printSchema()

print("\nSample rows:")
sample_df.limit(10).show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC **Outcome of this notebook:**
# MAGIC - File exists and is readable
# MAGIC - XML is confirmed well-formed
# MAGIC - Root / row structure understood
# MAGIC - Schema and nesting observed
# MAGIC
# MAGIC Use these decisions to configure **Notebook 2 — Bronze Ingestion**.
