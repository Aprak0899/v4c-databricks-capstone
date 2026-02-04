# Databricks notebook source
# MAGIC %md
# MAGIC # JSON reference code (semi-structured)
# MAGIC SQL + PySpark examples: dot notation, get_json_object, array index, explode, schema on read. Use with `json read` in this folder.
# MAGIC Each section shows SQL and PySpark where both apply.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Load JSON (Spark DataFrame API)
# MAGIC Replace path with your Volume or DBFS path.

# COMMAND ----------

# Load JSON data into a DataFrame
json_df = spark.read.json("/path/to/json/file")
# With schema on read (faster, type-safe):
# from pyspark.sql.types import StructType, StructField, StringType, LongType
# schema = StructType([StructField("id", LongType()), StructField("name", StringType()), ...])
# json_df = spark.read.schema(schema).json("/path/to/json/file")

json_df.printSchema()
json_df.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Extract top-level columns (dot notation)
# MAGIC SQL: use `.` on a STRUCT/JSON column. PySpark: use `F.col("col.field")` or `selectExpr`.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW customer_info AS
# MAGIC SELECT '{"name": "John", "age": 30, "city": "New York"}' AS raw_data;
# MAGIC
# MAGIC SELECT raw_data.name AS customer_name, raw_data.city AS customer_city FROM customer_info;

# COMMAND ----------

# PySpark equivalent: dot notation on STRUCT column
from pyspark.sql import functions as F

customer_df = spark.sql("SELECT '{\"name\": \"John\", \"age\": 30, \"city\": \"New York\"}' AS raw_data")
# Parse JSON string to STRUCT then select fields
from pyspark.sql.types import StructType, StructField, StringType, LongType
schema = StructType([StructField("name", StringType()), StructField("age", LongType()), StructField("city", StringType())])
customer_df = customer_df.withColumn("raw_data", F.from_json(F.col("raw_data"), schema))
customer_df.select(F.col("raw_data.name").alias("customer_name"), F.col("raw_data.city").alias("customer_city")).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Extract nested fields (dot notation)
# MAGIC Navigate nested objects: SQL `column.nested1.nested2.field`; PySpark `F.col("col.a.b.c")`.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW employee_data AS
# MAGIC SELECT '{"employee":{"name":"Alice","department":{"name":"Engineering","location":"San Francisco"}}}' AS raw_data;
# MAGIC SELECT raw_data.employee.department.name AS department_name, raw_data.employee.department.location AS department_location FROM employee_data;

# COMMAND ----------

# PySpark equivalent: nested access (get_json_object for string column, or dot notation if from_json used)
employee_df = spark.table("employee_data")
employee_df.select(
    F.get_json_object(F.col("raw_data"), "$.employee.department.name").alias("department_name"),
    F.get_json_object(F.col("raw_data"), "$.employee.department.location").alias("department_location"),
).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Extract from array (index)
# MAGIC SQL: `column.array[0].field`. PySpark: `F.col("column")[0]` or `F.col("column").getItem(0)`.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW product_data AS
# MAGIC SELECT '{"products":[{"id":1,"name":"Laptop"},{"id":2,"name":"Smartphone"}]}' AS raw_data;
# MAGIC SELECT raw_data.products[0].name AS first_product_name FROM product_data;

# COMMAND ----------

# PySpark equivalent: first element of array (raw_data is string; use get_json_object or parse first)
product_df = spark.table("product_data")
product_df.select(
    F.get_json_object(F.col("raw_data"), "$.products[0].name").alias("first_product_name")
).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. get_json_object(json_string, path)
# MAGIC Extract value by JSON path. PySpark: `F.get_json_object(F.col("raw_data"), "$.path")`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT get_json_object(raw_data, '$.name') AS name, get_json_object(raw_data, '$.employee.department.name') AS dept_name
# MAGIC FROM (SELECT '{"name":"John","employee":{"department":{"name":"Sales"}}}' AS raw_data);

# COMMAND ----------

# PySpark equivalent
path_df = spark.sql("SELECT '{\"name\":\"John\",\"employee\":{\"department\":{\"name\":\"Sales\"}}}' AS raw_data")
path_df.select(
    F.get_json_object(F.col("raw_data"), "$.name").alias("name"),
    F.get_json_object(F.col("raw_data"), "$.employee.department.name").alias("dept_name"),
).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. PySpark: Nested data + explode / explode_outer
# MAGIC Create DataFrame from list of dicts; explode array to one row per element; filter and aggregate. Use `explode_outer` if array can be NULL.

# COMMAND ----------

from pyspark.sql.functions import explode, sum

# Sample JSON-like data
json_data = [
    {"id": 1, "name": "Alice", "orders": [{"product": "Laptop", "price": 1200}]},
    {"id": 2, "name": "Bob", "orders": [{"product": "Headphones", "price": 100}, {"product": "Keyboard", "price": 50}]},
]

df = spark.createDataFrame(json_data)

# Top-level fields
df.select("id", "name").show()

# Nested (array) columns
df.select("id", "orders.product", "orders.price").show()

# Explode array: one row per order (use explode_outer("orders") if orders can be NULL)
df_exploded = df.withColumn("order", explode("orders"))
df_exploded.select("id", "order.product", "order.price").show()

# Filter and aggregate
df_filtered = df_exploded.filter(df_exploded["order.product"] == "Laptop")
df_filtered.groupBy("id").agg(sum("order.price").alias("total_spent")).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. PySpark: from_json / to_json
# MAGIC Parse JSON string column to STRUCT; serialize row to JSON string.

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType

# Parse a string column containing JSON into a STRUCT
# schema = StructType([StructField("device", StringType()), StructField("geo", StructType([...]))])
# df = df.withColumn("value_struct", from_json(F.col("decoded_value"), schema))

# Serialize a STRUCT (or row) to JSON string
# df.withColumn("json_string", to_json(F.struct("col1", "col2")))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Write DataFrame to JSON (PySpark)
# MAGIC After processing, write back to JSON or Delta.

# COMMAND ----------

# PySpark
# json_df.write.mode("overwrite").json("/path/to/output/json_file")
# Delta (recommended): json_df.write.format("delta").mode("append").saveAsTable("catalog.schema.bronze_table")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Run SQL on a DataFrame (temp view)
# MAGIC Register DataFrame as a view and query with SQL.

# COMMAND ----------

# PySpark
# json_df.createOrReplaceTempView("json_data")
# spark.sql("SELECT * FROM json_data WHERE ...").show()
