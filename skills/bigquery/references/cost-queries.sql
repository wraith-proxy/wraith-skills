-- Substitute <bigquery_location> (from the wraith block) in each region
-- qualifier before running. Dry-run first, then cap with
-- --maximum_bytes_billed.

-- Top 20 queries by bytes billed in the last 30 days.
SELECT
  query_info.query_hashes.normalized_literals AS query_hash,
  COUNT(*) AS runs,
  SUM(total_bytes_billed) AS bytes_billed
FROM `region-<bigquery_location>.INFORMATION_SCHEMA.JOBS`
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_type = 'QUERY'
  AND statement_type != 'SCRIPT'
GROUP BY query_hash
ORDER BY bytes_billed DESC
LIMIT 20;

-- Bytes billed per user per day over the last 30 days.
SELECT
  user_email,
  DATE(creation_time) AS day,
  SUM(total_bytes_billed) AS bytes_billed
FROM `region-<bigquery_location>.INFORMATION_SCHEMA.JOBS`
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_type = 'QUERY'
GROUP BY user_email, day
ORDER BY day DESC, bytes_billed DESC;

-- Slot milliseconds per query hash over the last 30 days.
SELECT
  query_info.query_hashes.normalized_literals AS query_hash,
  COUNT(*) AS runs,
  SUM(total_slot_ms) AS slot_ms
FROM `region-<bigquery_location>.INFORMATION_SCHEMA.JOBS`
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_type = 'QUERY'
GROUP BY query_hash
ORDER BY slot_ms DESC
LIMIT 20;

-- Tables not referenced by any query in the last 90 days.
WITH used AS (
  SELECT DISTINCT
    rt.project_id, rt.dataset_id, rt.table_id
  FROM `region-<bigquery_location>.INFORMATION_SCHEMA.JOBS`,
    UNNEST(referenced_tables) AS rt
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
)
SELECT t.table_catalog, t.table_schema, t.table_name
FROM `region-<bigquery_location>.INFORMATION_SCHEMA.TABLES` AS t
LEFT JOIN used AS u
  ON u.project_id = t.table_catalog
  AND u.dataset_id = t.table_schema
  AND u.table_id = t.table_name
WHERE t.table_type = 'BASE TABLE'
  AND u.table_id IS NULL;
