# Databricks notebook source
# MAGIC %md
# MAGIC ## Load malformed XML to Bronze (inline repair, no new file)
# MAGIC Fixes invalid tags `<>value</>` in memory, writes to a **temp** path, loads into a **view**, writes view to Bronze, then removes temp. Raw file is preserved. No permanent fixed file created.

# COMMAND ----------

dbutils.widgets.text(
    "xml_path",
    "/Volumes/dev_automotive/landing/landing_raw/final_geografic.xml",
    "Source XML file (raw, may have empty tags)",
)
dbutils.widgets.text("row_tag", "record", "rowTag (element per row)")
dbutils.widgets.text(
    "bronze_table",
    "dev_automotive.bronze.geografic",
    "Bronze table (catalog.schema.table)",
)

xml_path = dbutils.widgets.get("xml_path").strip()
row_tag = dbutils.widgets.get("row_tag").strip()
bronze_table = dbutils.widgets.get("bronze_table").strip()

# Temp path for fixed XML (deleted after load); no new permanent file
import uuid
temp_dir = xml_path.rsplit("/", 1)[0] + "/temp_xml_bronze_" + str(uuid.uuid4())[:8]

# COMMAND ----------

import re
import xml.etree.ElementTree as ET
from pyspark.sql import functions as F

# 1. Read raw XML as text (FUSE path on driver)
dbfs_xml = xml_path.replace("/Volumes", "/dbfs/Volumes")
with open(dbfs_xml, "r", encoding="utf-8") as f:
    raw_xml = f.read()
print("Raw XML loaded.")

# 2. Repair empty tags in memory: <>value</> -> <index>value</index>
fixed_xml = re.sub(r"<>([^<]*)</>", r"<index>\1</index>", raw_xml)
try:
    ET.fromstring(fixed_xml)
    print("✅ Fixed XML is well-formed.")
except ET.ParseError as e:
    raise Exception(f"❌ Fixed XML still malformed: {e}")

# 3. Write fixed XML to temp path (so Spark can read it)
dbfs_temp_dir = temp_dir.replace("/Volumes", "/dbfs/Volumes")
import os
os.makedirs(dbfs_temp_dir, exist_ok=True)
with open(dbfs_temp_dir + "/fixed.xml", "w", encoding="utf-8") as f:
    f.write(fixed_xml)
print(f"Fixed XML written to temp: {temp_dir}")

# COMMAND ----------

# 4. Load from temp path into DataFrame, then create a view
df = (
    spark.read
    .format("xml")
    .option("rowTag", row_tag)
    .option("charset", "UTF-8")
    .load(temp_dir + "/fixed.xml")
)
df.createOrReplaceTempView("xml_staging")
print("Loaded into view: xml_staging")

# COMMAND ----------

# 5. Add audit columns and write view to Bronze
bronze_df = (
    spark.table("xml_staging")
    .withColumn("_source_file", F.lit(xml_path))
    .withColumn("_ingest_ts", F.current_timestamp())
)
bronze_df.write.mode("overwrite").saveAsTable(bronze_table)
print(f"✅ Written to Bronze: {bronze_table}")

# COMMAND ----------

# 6. Remove temp path (no new file left behind)
dbutils.fs.rm(temp_dir, recurse=True)
print("Temp path removed. Raw XML preserved.")
