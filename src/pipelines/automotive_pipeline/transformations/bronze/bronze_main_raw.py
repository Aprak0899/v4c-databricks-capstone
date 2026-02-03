from pyspark import pipelines as dp
from pyspark.sql.types import StructType, StructField, DoubleType, StringType, IntegerType
from pyspark.sql.functions import col

# ---------------------------------------------------------------------
# Config & Schema
# ---------------------------------------------------------------------
LANDING_PATH    = "/Volumes/dev_automotive/landing/landing_raw/"


EXPLICIT_SCHEMA = StructType([
    StructField("cost",           DoubleType(),  True),
    StructField("currency",       StringType(),  True),
    StructField("marka",          StringType(),  True),
    StructField("model",          StringType(),  True),
    StructField("year",           IntegerType(), True),
    StructField("has_license",    IntegerType(), True),
    StructField("place",          StringType(),  True),
    StructField("date",           StringType(),  True),
    StructField("id",             IntegerType(), True),
    StructField("engine",         StringType(),  True),
    StructField("power",          IntegerType(), True),
    StructField("gear",           StringType(),  True),
    StructField("probeg",         IntegerType(), True),
    StructField("sWheel",         StringType(),  True),
    StructField("complectation",  StringType(),  True),
    StructField("transmission",   StringType(),  True),
    StructField("R",              IntegerType(), True),
    StructField("G",              IntegerType(), True),
    StructField("B",              IntegerType(), True),
])

# ---------------------------------------------------------------------
# Read — Auto Loader only, no business logic
# ---------------------------------------------------------------------
def read_bronze_csv():
    return (
        spark.readStream
        .format("cloudFiles")
        .schema(EXPLICIT_SCHEMA)
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("sep", ",")
        .option("rescuedDataColumn", "_rescued_data")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .option("readerCaseSensitive", "false")
        .load(LANDING_PATH)
    )

# ---------------------------------------------------------------------
# Enrich — add lineage columns only
# _rescued_data & _corrupt_record already in * from reader options
# ---------------------------------------------------------------------
def add_lineage(df):
    return df.select(
        "*",
        col("_metadata.file_path").alias("source_file_path"),
        col("_metadata.file_name").alias("source_file_name"),
        col("_metadata.file_modification_time").alias("source_file_modified_at"),
    )

# ---------------------------------------------------------------------
# Lakeflow Table — returning df is the write
# ---------------------------------------------------------------------
@dp.table(
    name="main_raw",
    comment="Bronze: raw streaming ingest of automotive CSV. No transforms, no dedup.",
)
def main_raw():
    return add_lineage(read_bronze_csv())