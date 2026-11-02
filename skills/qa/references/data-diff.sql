-- BigQuery Standard SQL. Dry-run each query first (bq query --dry_run).
-- Replace the placeholders; pass the date with --parameter=ds:DATE:YYYY-MM-DD.
-- dev:  `{{dev_table}}`   prod: `{{prod_table}}`   key: {{key}}

-- 1. Row count by ds for two tables
SELECT 'dev' AS side, ds, COUNT(*) AS row_count
FROM `{{dev_table}}`
WHERE ds = @ds
GROUP BY ds
UNION ALL
SELECT 'prod' AS side, ds, COUNT(*) AS row_count
FROM `{{prod_table}}`
WHERE ds = @ds
GROUP BY ds;

-- 2a. Keys in prod but missing from dev
SELECT {{key}} FROM `{{prod_table}}` WHERE ds = @ds
EXCEPT DISTINCT
SELECT {{key}} FROM `{{dev_table}}` WHERE ds = @ds;

-- 2b. Keys in dev but missing from prod
SELECT {{key}} FROM `{{dev_table}}` WHERE ds = @ds
EXCEPT DISTINCT
SELECT {{key}} FROM `{{prod_table}}` WHERE ds = @ds;

-- 3. NULL rate per column (repeat the pair for each column)
SELECT
  COUNTIF({{column}} IS NULL) AS null_rows,
  COUNT(*) AS total_rows,
  SAFE_DIVIDE(COUNTIF({{column}} IS NULL), COUNT(*)) AS null_rate
FROM `{{dev_table}}`
WHERE ds = @ds;

-- 4. Metric sums, dev against prod
SELECT
  'dev' AS side,
  SUM({{metric}}) AS metric_sum
FROM `{{dev_table}}`
WHERE ds = @ds
UNION ALL
SELECT
  'prod' AS side,
  SUM({{metric}}) AS metric_sum
FROM `{{prod_table}}`
WHERE ds = @ds;
