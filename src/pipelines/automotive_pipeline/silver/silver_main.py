import dlt
from pyspark.sql.functions import col, to_utc_timestamp, expr, when

# 1. Target Table for SCD Type 2
dlt.create_target_table(
    name="main_silver",
    comment="Silver: Incremental Sales with SCD Type 2 history tracking.",
    table_properties={
        "quality": "silver",
        "pipelines.autoOptimize.zOrderCols": "marka, model"
    }
)

# 2. View for Transformation (Day 5 Normalization)
@dlt.view
def main_silver_cleaned():
    """
    Standardizes dates to UTC and cleans metrics before applying SCD 2.
    """
    return dlt.read_stream("main_raw").select(
        "id",
        "marka",
        "model",
        "year",
        "cost",
        "currency",
        when(col("has_license") == 1, "Licensed").otherwise("No License").alias("license_status"),
        "place",
        # Business Rule: Normalize sales date to UTC
        to_utc_timestamp(expr("to_date(date, 'dd.MM.yyyy')"), "UTC").alias("sale_date_utc"),
        "engine",
        "power",
        "gear",
        "probeg",
        "transmission",
        # Business Rule: Normalize audit timestamps to UTC
        to_utc_timestamp(col("source_file_modified_at"), "UTC").alias("file_processed_at_utc")
    )

# 3. Apply Changes (FIXED: sequence_by is a STRING)
dlt.apply_changes(
    target = "main_silver",
    source = "main_silver_cleaned",
    keys = ["id"],
    sequence_by = "file_processed_at_utc", # FIX: Use string, not col()
    stored_as_scd_type = "2",
    except_column_list = ["file_processed_at_utc"]
)