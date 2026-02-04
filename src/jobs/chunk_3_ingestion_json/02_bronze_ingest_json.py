# Databricks notebook source
# =============================================================
# Bronze Ingestion — catalogs_raw
# Auto Loader, single file, trigger once
# Path   : /Volumes/dev_automotive/landing/landing_raw/
# File   : catalogs.json
# Table  : dev_automotive.bronze.catalogs_raw
# =============================================================

from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col

# -------------------------------------------------------------
# Config
# -------------------------------------------------------------
LANDING_PATH = "/Volumes/dev_automotive/landing/landing_raw/"
TARGET_TABLE = "dev_automotive.bronze.catalogs_raw"

# -------------------------------------------------------------
# Schema — all STRING, matches the JSON exactly
# -------------------------------------------------------------
EXPLICIT_SCHEMA = StructType([
    StructField("loaded_at",                        StringType(), True),
    StructField("source_file",                      StringType(), True),
    StructField("Время разгона 0-100 км/ч, с",     StringType(), True),
    StructField("Клиренс",                          StringType(), True),
    StructField("Кол-во мест",                      StringType(), True),
    StructField("Комплектация",                     StringType(), True),
    StructField("Коробка передач",                  StringType(), True),
    StructField("Максимальная скорость, км/ч",     StringType(), True),
    StructField("Марка",                            StringType(), True),
    StructField("Марка кузова",                     StringType(), True),
    StructField("Модель",                           StringType(), True),
    StructField("Мощность двигателя",              StringType(), True),
    StructField("Объем багажника",                  StringType(), True),
    StructField("Объём двигателя",                  StringType(), True),
    StructField("Период выпуска",                   StringType(), True),
    StructField("Поколение",                        StringType(), True),
    StructField("Привод",                           StringType(), True),
    StructField("Расход топлива",                   StringType(), True),
    StructField("Страна сборки",                    StringType(), True),
    StructField("Тип кузова",                       StringType(), True),
    StructField("Тип топлива",                      StringType(), True),
])

# -------------------------------------------------------------
# Read — Auto Loader
# -------------------------------------------------------------
def read_catalogs_json():
    return (
        spark.readStream
        .format("cloudFiles")
        .schema(EXPLICIT_SCHEMA)
        .option("cloudFiles.format", "json")
        .option("rescuedDataColumn", "_rescued_data")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .load(LANDING_PATH + "catalogs.json")
    )

# -------------------------------------------------------------
# Enrich — add lineage from _metadata
# -------------------------------------------------------------
def add_lineage(df):
    return df.select(
        "*",
        col("_metadata.file_path").alias("source_file_path"),
        col("_metadata.file_name").alias("source_file_name"),
        col("_metadata.file_modification_time").alias("source_file_modified_at"),
    )

# -------------------------------------------------------------
# Write — trigger once, lands in catalogs_raw
# -------------------------------------------------------------
(
    add_lineage(read_catalogs_json())
    .writeStream
    .trigger(availableNow=True)
    .format("delta")
    .option("checkpointLocation", f"/Volumes/dev_automotive/checkpoints/catalogs_raw/")
    .option("mergeSchema", "true")
    .table(TARGET_TABLE)
    .awaitTermination()
)

print("✅ catalogs_raw loaded successfully")