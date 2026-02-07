from pyspark import pipelines as dp
import pandas as pd
from pyspark.sql.functions import col, pandas_udf, to_utc_timestamp, regexp_extract, regexp_replace
from pyspark.sql.types import DoubleType

# ---------------------------------------------------------------------
# 1. PANDAS UDF: Unit Stripping (Day 4 Requirement)
# ---------------------------------------------------------------------
@pandas_udf(DoubleType())
def clean_units_udf(unit_series: pd.Series) -> pd.Series:
    """
    Standardizes numeric metrics by stripping units and handling decimal commas.
    Processes data in batches via Apache Arrow for high performance.
    """
    return unit_series.str.replace(',', '.', regex=False).str.extract(r'(\d+\.?\d*)')[0].astype(float)

# ---------------------------------------------------------------------
# 2. SILVER MATERIALIZED VIEW (Standardized & Typed)
# ---------------------------------------------------------------------
@dp.table(
    name="catalogs_silver",
    comment="Silver: Reference catalog with UTC dates, split years, and typed metrics.",
    table_properties={"quality": "silver"}
)
@dp.expect_or_drop("valid_unit_format", "clearance RLIKE '.*(мм|см|м)$'")
def catalogs_silver():
    bronze_df = dp.read("catalogs_raw")
    return (
        bronze_df.select(
            "brand", "model", "generation",
            col("complectation").alias("trim_level"),
            clean_units_udf(col("clearance")).alias("clearance_mm"),
            clean_units_udf(col("power")).alias("power_hp"),
            clean_units_udf(col("engine_volume")).alias("engine_volume_l"),
            clean_units_udf(col("trunk_volume")).alias("trunk_volume_l"),
            clean_units_udf(col("acceleration_0_100")).alias("acceleration_sec"),
            clean_units_udf(col("max_speed")).alias("max_speed_kmh"),
            clean_units_udf(col("fuel_consumption")).alias("fuel_consumption_l_100km"),
            regexp_extract(col("production_period"), r"(\d{4})", 1).cast("int").alias("start_year"),
            regexp_extract(col("production_period"), r"-\s*(\d{4})", 1).cast("int").alias("end_year"),
            "gearbox", "drive", "fuel_type", "body_type", 
            col("body_mark").alias("body_code"), 
            col("country").alias("assembly_country"),
            col("seats").alias("seats_count"),
            to_utc_timestamp(col("source_file_modified_at"), "UTC").alias("processed_at_utc"),
            "source_file_name"
        )
    )

# ---------------------------------------------------------------------
# 3. QUARANTINE TABLE (The "Rescue" Logic)
# ---------------------------------------------------------------------
@dp.table(
    name="catalogs_quarantine",
    comment="Rescue: Records with unrecognized units or malformed data for manual audit."
)
def catalogs_quarantine():
    return dp.read("catalogs_raw").filter("clearance NOT RLIKE '.*(мм|см|м)$'")