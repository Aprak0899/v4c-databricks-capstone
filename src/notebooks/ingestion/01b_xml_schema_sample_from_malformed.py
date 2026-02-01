# Databricks notebook source
# MAGIC %md
# MAGIC ## Schema sample from malformed XML (bounded read + regex fix)
# MAGIC Reads a bounded line sample, applies regex fix for empty tags, wraps and parses, then creates a temp view for schema discovery. Use when the XML has `<>value</>` and you want to infer structure without fixing the whole file.

# COMMAND ----------

# ----------------------------
# Inputs
# ----------------------------

dbutils.widgets.text(
    "xml_path",
    "/Volumes/dev_automotive/landing/landing_raw/final_geografic.xml",
    "XML file path (volume)",
)
dbutils.widgets.text("row_tag", "record", "XML rowTag (element per row)")

xml_path = dbutils.widgets.get("xml_path").strip()
row_tag = dbutils.widgets.get("row_tag").strip()

SAMPLE_LINES = 5000
MAX_ROWS = 50

# COMMAND ----------

# ----------------------------
# Read bounded sample
# ----------------------------

sample_lines = (
    spark.read.text(xml_path)
    .limit(SAMPLE_LINES)
    .select("value")
    .toPandas()["value"]
    .tolist()
)

assert sample_lines, "❌ Unable to read sample from XML"

raw_sample = "\n".join(sample_lines)
print(f"✅ Loaded {len(sample_lines)} lines for schema sampling")

# COMMAND ----------

# ----------------------------
# Regex fix
# ----------------------------

import re

fixed_sample = re.sub(r"<>([^<]*)</>", r"<index>\1</index>", raw_sample)

# Remove XML declaration (so we can wrap in a single root)
fixed_sample = re.sub(r"<\?xml[^>]*\?>", "", fixed_sample, flags=re.IGNORECASE)

# Remove dangling partial tag at end (sample may cut mid-tag)
fixed_sample = re.sub(r"<[^>]*$", "", fixed_sample)

print("✅ Regex fix + cleanup applied")

# COMMAND ----------

# ----------------------------
# Wrap & parse
# ----------------------------

wrapped_xml = f"<__schema_sample__>{fixed_sample}</__schema_sample__>"

import xml.etree.ElementTree as ET

try:
    root = ET.fromstring(wrapped_xml)
    print("✅ Sample XML parsed successfully")
except ET.ParseError as e:
    raise Exception(f"❌ Sample XML still malformed: {e}")

# Helpful diagnostics
candidate_tags = {elem.tag for elem in root.iter()}
print(f"Candidate tags found in sample: {candidate_tags}")

# COMMAND ----------

# ----------------------------
# Extract rows
# ----------------------------

rows = []
for elem in root.findall(f".//{row_tag}")[:MAX_ROWS]:
    rows.append({child.tag: (child.text or "") for child in elem})

assert rows, f"❌ No rows extracted for row_tag='{row_tag}'"

print(f"✅ Extracted {len(rows)} rows for schema discovery")

# COMMAND ----------

# ----------------------------
# Create TEMP VIEW
# ----------------------------

sample_df = spark.createDataFrame(rows)
sample_df.createOrReplaceTempView("vw_xml_schema_sample")

print("✅ TEMP VIEW created: vw_xml_schema_sample")

sample_df.printSchema()
sample_df.show(10, truncate=False)
