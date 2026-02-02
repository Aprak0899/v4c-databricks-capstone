-- =============================================================================
-- Bronze Ingestion - Simple & Clean
-- Path  : /Volumes/dev_automotive/landing/landing_raw/
-- Files : 1_photo.csv, 1_text.csv
-- Tables: dev_automotive.bronze.photo_raw, dev_automotive.bronze.text_raw
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Step 1: Create Bronze tables (schema enforced + audit columns)
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dev_automotive.bronze.photo_raw (
  photo_seq_id INT,
  photo_url STRING,
  id DOUBLE,
  load_dt TIMESTAMP,
  source STRING,
  _rescued_data STRING              -- Absorbs new columns if CSV schema changes
) USING DELTA;

CREATE TABLE IF NOT EXISTS dev_automotive.bronze.text_raw (
  id DOUBLE,
  `text` STRING,
  load_dt TIMESTAMP,
  source STRING,
  _rescued_data STRING              -- Absorbs new columns if CSV schema changes
) USING DELTA;


-- -----------------------------------------------------------------------------
-- Step 2: Load data (COPY INTO - idempotent by default)
-- -----------------------------------------------------------------------------

-- Load photo
COPY INTO dev_automotive.bronze.photo_raw
FROM (
  SELECT
    _c0 AS photo_seq_id,
    photo_url,
    id,
    current_timestamp() AS load_dt,
    _metadata.file_path AS source,
    _rescued_data
  FROM 'file:/Volumes/dev_automotive/landing/landing_raw/1_photo.csv'
)
FILEFORMAT = CSV
FORMAT_OPTIONS (
  'header' = 'true',
  'rescuedDataColumn' = '_rescued_data'
);

-- Load text
COPY INTO dev_automotive.bronze.text_raw
FROM (
  SELECT
    id,
    `text`,
    current_timestamp() AS load_dt,
    _metadata.file_path AS source,
    _rescued_data
  FROM 'file:/Volumes/dev_automotive/landing/landing_raw/1_text.csv'
)
FILEFORMAT = CSV
FORMAT_OPTIONS (
  'header' = 'true',
  'rescuedDataColumn' = '_rescued_data'
);


-- -----------------------------------------------------------------------------
-- Step 3: Quick view (optional - just to see what loaded)
-- -----------------------------------------------------------------------------

SELECT * FROM dev_automotive.bronze.photo_raw LIMIT 5;
SELECT * FROM dev_automotive.bronze.text_raw LIMIT 5;


-- -----------------------------------------------------------------------------
-- Future: Load multiple files with pattern matching
-- -----------------------------------------------------------------------------
-- FROM 'file:/Volumes/dev_automotive/landing/landing_raw/*_photo.csv'
-- FROM 'file:/Volumes/dev_automotive/landing/landing_raw/*_text.csv'
