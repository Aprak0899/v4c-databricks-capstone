from pyspark import pipelines as dp
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col

# ---------------------------------------------------------------------
# Config & Schema
# ---------------------------------------------------------------------
LANDING_PATH = "/Volumes/dev_automotive/landing/landing_catalog/"

CATALOGS_SCHEMA = StructType([
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

# Russian key → English column name
COLUMN_MAPPING = {
    "Время разгона 0-100 км/ч, с": "acceleration_0_100",
    "Клиренс":                     "clearance",
    "Кол-во мест":                 "seats",
    "Комплектация":                "complectation",
    "Коробка передач":             "gearbox",
    "Максимальная скорость, км/ч": "max_speed",
    "Марка":                       "marka",
    "Марка кузова":                "body_mark",
    "Модель":                      "model",
    "Мощность двигателя":          "power",
    "Объем багажника":             "trunk_volume",
    "Объём двигателя":             "engine_volume",
    "Период выпуска":              "production_period",
    "Поколение":                   "generation",
    "Привод":                      "drive",
    "Расход топлива":              "fuel_consumption",
    "Страна сборки":               "country",
    "Тип кузова":                  "body_type",
    "Тип топлива":                 "fuel_type",
}


# ---------------------------------------------------------------------
# Read — Auto Loader, JSON only
# ---------------------------------------------------------------------
def read_catalogs_json():
    return (
        spark.readStream
        .format("cloudFiles")
        .schema(CATALOGS_SCHEMA)
        .option("cloudFiles.format", "json")
        .option("pathGlobFilter", "catalogs*.json")
        .option("rescuedDataColumn", "_rescued_data")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .load(LANDING_PATH)
    )


# ---------------------------------------------------------------------
# Enrich — lineage from _metadata
# ---------------------------------------------------------------------
def add_lineage(df):
    # Rename Russian → English
    for russian, english in COLUMN_MAPPING.items():
        df = df.withColumnRenamed(russian, english)

    # Add lineage from _metadata
    return df.select(
        "*",
        col("_metadata.file_path").alias("source_file_path"),
        col("_metadata.file_name").alias("source_file_name"),
        col("_metadata.file_modification_time").alias("source_file_modified_at"),
    )


# ---------------------------------------------------------------------
# DLT Table — streaming, appends on every new catalogs*.json file
# ---------------------------------------------------------------------
@dp.table(
    name="catalogs_raw",
    comment="Bronze: dimension table, raw ingest of catalogs JSON. Appends on new file.",
)
def catalogs_raw():
    return add_lineage(read_catalogs_json())