# Databricks notebook source
# MAGIC %md
# MAGIC # Ingest JSON into Bronze using Auto Loader
# MAGIC **Plan:** `plan_ingest_json_bronze_autoloader.md` in this folder.
# MAGIC Reads JSON from landing path with Auto Loader; optional base64 decode; adds audit columns; writes to Bronze Delta.

# COMMAND ----------

# Widgets: paths and options
dbutils.widgets.text(
    "landing_path",
    "/Volumes/dev_automotive/landing/landing_raw/",
    "Landing path (Volume or cloud path)",
)
dbutils.widgets.text(
    "bronze_table",
    "dev_automotive.bronze.json_events",
    "Bronze table (catalog.schema.table)",
)
dbutils.widgets.text(
    "checkpoint_path",
    "/Volumes/dev_automotive/checkpoints/json_bronze_autoloader",
    "Checkpoint + schema path (do not share between pipelines)",
)
dbutils.widgets.dropdown(
    "decode_base64",
    "false",
    ["true", "false"],
    "Apply base64 decode to key/value (Kafka-style source)",
)

landing_path = dbutils.widgets.get("landing_path").strip().rstrip("/")
bronze_table = dbutils.widgets.get("bronze_table").strip()
checkpoint_path = dbutils.widgets.get("checkpoint_path").strip().rstrip("/")
decode_base64 = dbutils.widgets.get("decode_base64").strip().lower() == "true"

schema_location = f"{checkpoint_path}/schema"
checkpoint_location = f"{checkpoint_path}/checkpoint"

# COMMAND ----------

from pyspark.sql import functions as F

# Auto Loader: read JSON stream from landing path
stream_df = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", schema_location)
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("encoding", "utf-8")
    .load(landing_path)
)

# Optional: base64 decode (match json read B3)
if decode_base64 and "key" in stream_df.schema.fieldNames() and "value" in stream_df.schema.fieldNames():
    stream_df = (
        stream_df
        .withColumn("decoded_key", F.expr("cast(unbase64(key) as string)"))
        .withColumn("decoded_value", F.expr("cast(unbase64(value) as string)"))
    )

# Audit columns (plan 3.3)
stream_df = (
    stream_df
    .withColumn("_ingest_timestamp", F.current_timestamp())
    .withColumn("_source_file", F.input_file_name())
)

# COMMAND ----------

# Write stream to Bronze Delta; trigger(availableNow=True) = process all new files then stop
(
    stream_df.writeStream
    .option("checkpointLocation", checkpoint_location)
    .trigger(availableNow=True)
    .toTable(bronze_table)
)

print(f"✅ Auto Loader run completed. Data written to {bronze_table}")

# COMMAND ----------

# Validation: row count and sample (plan 5.3)
df = spark.table(bronze_table)
row_count = df.count()
print(f"📊 Bronze row count: {row_count:,}")
df.limit(10).show(truncate=50)
