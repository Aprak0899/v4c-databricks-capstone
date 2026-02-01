# Databricks notebook source
# MAGIC %md
# MAGIC # Notebook 2 — Bronze Ingestion (XML)
# MAGIC **Purpose:** Heal empty tags on executors, read healed XML, add metadata, append to Bronze. Uses decisions from Notebook 1 (rowTag, path).

# COMMAND ----------

dbutils.widgets.text(
    "xml_path",
    "/Volumes/dev_automotive/landing/landing_raw/final_geografic.xml",
    "XML file path (volume)",
)
dbutils.widgets.text("row_tag", "record", "rowTag (from Notebook 1)")
dbutils.widgets.text(
    "bronze_table",
    "dev_automotive.bronze.geografic",
    "Bronze table (catalog.schema.table)",
)

xml_path = dbutils.widgets.get("xml_path").strip()
row_tag = dbutils.widgets.get("row_tag").strip()
bronze_table = dbutils.widgets.get("bronze_table").strip()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Healer

# COMMAND ----------

from pyspark.sql import functions as F

# Temp path for healed XML (same Volume); removed after ingest
temp_path = f"{xml_path}_healed"

(
    spark.read.text(xml_path)
    .withColumn("value", F.regexp_replace("value", r"<>([^<]*)</>", r"<index>$1</index>"))
    .write.mode("overwrite")
    .text(temp_path)
)

print(f"✅ Structural fix applied and saved to: {temp_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Reader — load healed XML and infer schema

# COMMAND ----------

df_bronze = (
    spark.read
    .format("xml")
    .option("rowTag", row_tag)
    .option("inferSchema", "true")
    .load(temp_path)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Row & column counts (profiling)

# COMMAND ----------

row_count = df_bronze.count()
col_count = len(df_bronze.columns)
print(f"📊 INGESTION SUMMARY: {row_count:,} rows | {col_count} columns detected")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Add metadata and write to Bronze (append)

# COMMAND ----------

(
    df_bronze
    .withColumn("bronze_ingested_at", F.current_timestamp())
    .withColumn("source_file", F.lit(xml_path))
    .write.format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .saveAsTable(bronze_table)
)
print(f"✅ Written to {bronze_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Cleanup temp path (no _healed directory left behind)

# COMMAND ----------

dbutils.fs.rm(temp_path, recurse=True)
print("Temp path removed.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Display Bronze table

# COMMAND ----------

display(spark.table(bronze_table))
