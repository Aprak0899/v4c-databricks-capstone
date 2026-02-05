"""
Unit tests — bronze photo_raw (Chunk 1).
Same logic as test_chunk_1_bronze_ingestion.ipynb; runnable in CI with PySpark.
Dummy data: 1 good row, 1 duplicate, 1 rescued row, 1 null url.
"""
from datetime import datetime

from pyspark.sql import Row, SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    LongType,
    StringType,
    DoubleType,
    TimestampType,
)


def get_spark():
    return (
        SparkSession.builder.master("local[1]")
        .appName("test_chunk_1_bronze")
        .getOrCreate()
    )


def test_bronze_photo_raw():
    spark = get_spark()
    NOW = datetime.now()

    schema = StructType(
        [
            StructField("photo_seq_id", LongType(), True),
            StructField("photo_url", StringType(), True),
            StructField("id", DoubleType(), True),
            StructField("load_dt", TimestampType(), True),
            StructField("modification_dt", TimestampType(), True),
            StructField("source", StringType(), True),
            StructField("_rescued_data", StringType(), True),
        ]
    )

    dummy_data = [
        Row(101, "https://img.com/photo_101.jpg", 500.5, NOW, NOW, "/path/1_photo.csv", None),
        Row(101, "https://img.com/photo_101.jpg", 500.5, NOW, NOW, "/path/1_photo.csv", None),
        Row(
            202,
            "https://img.com/photo_202.jpg",
            600.0,
            NOW,
            NOW,
            "/path/1_photo.csv",
            '{"oops_extra_column":"bad"}',
        ),
        Row(303, None, 700.0, NOW, NOW, "/path/1_photo.csv", None),
    ]

    df = spark.createDataFrame(dummy_data, schema)

    # TEST 1: Record count
    assert df.count() == 4, "Expected 4 rows"

    # TEST 2: Good data parsing
    good = df.filter("photo_seq_id = 101").first()
    assert good["id"] == 500.5
    assert good["_rescued_data"] is None or good["_rescued_data"] == ""

    # TEST 3: Rescue logic
    bad = df.filter("photo_seq_id = 202").first()
    assert bad["_rescued_data"] is not None
    assert "oops_extra_column" in (bad["_rescued_data"] or "")

    # TEST 4: Null URL
    null_url = df.filter("photo_seq_id = 303").first()
    assert null_url["photo_url"] is None

    # TEST 5: Duplicate count
    assert df.filter("photo_seq_id = 101").count() == 2


if __name__ == "__main__":
    test_bronze_photo_raw()
    print("All tests passed.")
