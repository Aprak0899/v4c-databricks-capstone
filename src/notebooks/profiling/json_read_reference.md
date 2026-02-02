Inspect json
--
List 'path'
--pick one path from above and paste it below
-- View JSON files as text
SELECT *
FROM text.`/Volumes/dbacademy_ecommerce/v01/raw/events-kafka`
LIMIT 5;

--
-- 3. Run the cell below to see how to use read_files() to read the JSON data. Notice the following:
--   - The JSON file is cleanly read into a tabular format with 6 columns.
--   - The key and value columns are base64-encoded and returned as STRING data type.
--   - There are no rows in the _rescued_data column.

--
-- View JSON file in tabular form (read_files with format => json)
SELECT *
FROM read_files(
    "/Volumes/dbacademy_ecommerce/v01/raw/events-kafka",
    format => "json"
)
LIMIT 10;

--
-- B2. Using CTAS and read_files() with JSON
-- Ingesting JSON files using read_files() is as straightforward as reading CSV files.

--
-- Create the bronze raw from JSON (CTAS + read_files)
-- Drop the table if it exists for demonstration purposes
DROP TABLE IF EXISTS kafka_events_bronze_raw;

-- Create the Delta table
CREATE TABLE kafka_events_bronze_raw AS
SELECT *
FROM read_files(
    "/Volumes/dbacademy_ecommerce/v01/raw/events-kafka",
    format => "json"
);

-- Display the table
SELECT *
FROM kafka_events_bronze_raw
LIMIT 10;

--
-- B3. Decoding base64 Strings for the Bronze Table
--
-- Decode the Base64 string as binary
SELECT
    key AS encoded_key,
    unbase64(key) AS decoded_key,
    value AS encoded_value,
    unbase64(value) AS decoded_value
FROM kafka_events_bronze_raw
LIMIT 5;

--
-- Create the bronze_decoded table
CREATE OR REPLACE TABLE kafka_events_bronze_decoded AS
SELECT
    cast(unbase64(key) AS STRING) AS decoded_key,
    offset,
    partition,
    timestamp,
    topic,
    cast(unbase64(value) AS STRING) AS decoded_value
FROM kafka_events_bronze_raw;

-- View the new table
SELECT *
FROM kafka_events_bronze_decoded
LIMIT 5;

--
-- C. Working with JSON Formatted Strings in a Table
-- C1. Flattening JSON String Columns
--
-- BENEFITS
--   Simple   - Easy to implement and store JSON as plain text.
--   Flexible - Can hold any JSON structure without schema constraints.
--
-- CONSIDERATIONS
--   Performance     - STRING columns are slower when querying and processing complex data.
--   No Schema      - The lack of a defined schema for STRING columns can lead to data integrity issues.
--   Complex to Query - Requires additional code to parse and retrieve data, which can be complex.

--
-- Query a JSON string and extract values
SELECT
    decoded_value,
    decoded_value:device,
    decoded_value:traffic_source,
    decoded_value:geo,           -- Contains another JSON formatted string
    decoded_value:items         -- Contains a nested-array of JSON formatted strings
FROM kafka_events_bronze_decoded
LIMIT 5;

--
-- 2. We can then begin to parse out the necessary JSON formatted string values to create another bronze table to flatten the JSON formatted string column for downstream processing.

--
-- Create bronze table with flattened JSON string columns
CREATE OR REPLACE TABLE kafka_events_bronze_string_flattened AS
SELECT
    decoded_key,
    offset,
    partition,
    timestamp,
    topic,
    decoded_value:device,
    decoded_value:traffic_source,
    decoded_value:geo,   -- Contains another JSON formatted string
    decoded_value:items  -- Contains a nested-array of JSON formatted strings
FROM kafka_events_bronze_decoded;

-- Display the table
SELECT *
FROM kafka_events_bronze_string_flattened;

--
-- Benefits and Considerations of STRUCT Columns
--
-- Benefits
--   Schema Enforcement - STRUCT columns define and enforce a schema, helping maintain data integrity.
--   Improved Performance - STRUCTs are generally more efficient for querying and processing than plain strings.
--
-- Considerations
--   Schema Enforcement - Because the schema is enforced, issues can arise if the JSON structure changes over time.
--   Reduced Flexibility - The data must consistently match the defined schema, leaving less room for structural variation.
--
-- C2.1 Converting a JSON STRING to a STRUCT Column
-- To convert a JSON-formatted STRING column to a STRUCT column, derive the schema of the JSON-formatted string and then parse each row into a STRUCT type.
-- Two steps: 1. Get the STRUCT type of the JSON formatted string. 2. Apply the STRUCT to the JSON formatted string column.
--
-- Step 1: Determine the schema of the JSON formatted string
SELECT schema_of_json('{"device":"Linux","ecommerce":{"purchase_revenue_in_usd":1075.5,"total_item_quantity":1,"unique_items":1},"event_name":"finalize","event_previous_timestamp":1593879231210816,"event_timestamp":1593879335779563,"geo":{"city":"Houston","state":"TX"},"items":[{"coupon":"NEWBED10","item_id":"M_STAN_K","item_name":"Standard King Mattress","item_revenue_in_usd":1075.5,"price_in_usd":1195.0,"quantity":1}],"traffic_source":"email","user_first_touch_timestamp":1593454417513109,"user_id":"UA000000106116176"}')
AS schema;

--
-- Step 2: Create table with STRUCT type (from_json)
CREATE OR REPLACE TABLE kafka_events_bronze_struct AS
SELECT
    * EXCEPT (decoded_value),
    from_json(
        decoded_value,
        'STRUCT<device: STRING, ecommerce: STRUCT<purchase_revenue_in_usd: DOUBLE, total_item_quantity: BIGINT, unique_items: BIGINT>, event_name: STRING, event_previous_timestamp: BIGINT, event_timestamp: BIGINT, geo: STRUCT<city: STRING, state: STRING>, items: ARRAY<STRUCT<coupon: STRING, item_id: STRING, item_name: STRING, item_revenue_in_usd: DOUBLE, price_in_usd: DOUBLE, quantity: BIGINT>>, traffic_source: STRING, user_first_touch_timestamp: BIGINT, user_id: STRING>'
    ) AS value
FROM kafka_events_bronze_decoded;

-- View the new table
SELECT *
FROM kafka_events_bronze_struct
LIMIT 5;

--
-- Obtain values from a STRUCT column
SELECT
    decoded_key,
    value.device AS device,                    -- Field
    value.geo.city AS city,                    -- Nested-field from geo field
    value.items AS items,
    array_size(items) AS number_elements_in_array  -- Count the number of elements in the array column items
FROM kafka_events_bronze_struct
ORDER BY number_elements_in_array DESC;

--
-- 2. If the array is NULL no rows are produced. To return a single row with NULLs for the array or map values use the explode_outer() function.

--
-- Explore the array to one row per element (explode)
CREATE OR REPLACE TABLE bronze_explode_array AS
SELECT
    decoded_key,
    array_size(value.items) AS number_elements_in_array,
    explode(value.items) AS item_in_array,
    value.items
FROM kafka_events_bronze_struct
ORDER BY number_elements_in_array DESC;

-- Display table
SELECT * FROM bronze_explode_array;
