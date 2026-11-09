# dbt patterns for BigQuery

Placeholders in angle brackets come from the `## wraith` block.

## 1. Raw merge with dedup and lookback

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='cust_id',
    on_schema_change='fail',
    full_refresh=false,
    partition_by={'field': 'updated_ts', 'data_type': 'timestamp'},
    cluster_by=['cust_id']
) }}
select * except (rn) from (
  select *, row_number() over (
    partition by cust_id order by loaded_at desc) as rn
  from {{ source('raw', 'raw_customers') }}
  {% if is_incremental() %}
  where loaded_at > timestamp_sub(
    (select max(loaded_at) from {{ this }}), interval 3 day)
  {% endif %}
) where rn = 1
```

## 2. Staging `ds` snapshot

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='insert_overwrite',
    partition_by={'field': 'ds', 'data_type': 'date'},
    cluster_by=['customer_id'],
    on_schema_change='fail'
) }}
select
  date('{{ var("ds") }}') as ds,
  cust_id as customer_id,
  safe_cast(signup_dt as date) as signup_date
from {{ ref('raw_customers') }}
{% if is_incremental() %}
where date(loaded_at) <= date('{{ var("ds") }}')
{% endif %}
```

Run with `--vars '{ds: <YYYY-MM-DD>}'`. A backfill reruns an earlier `ds`.
Test uniqueness on `(customer_id, ds)`.

## 3. SCD2 full rebuild from snapshots

```sql
{{ config(
    materialized='table',
    partition_by={'field': 'valid_from', 'data_type': 'date'},
    cluster_by=['customer_id']
) }}
with changed as (
  select *, to_json_string(
      (select as struct * except (ds))) as row_hash
  from {{ ref('stg_customers') }}
), marked as (
  select *, lag(row_hash) over (
    partition by customer_id order by ds) as prev_hash
  from changed
), versions as (
  select * from marked
  where prev_hash is null or prev_hash != row_hash
)
select * except (row_hash, prev_hash),
  ds as valid_from,
  lead(ds) over (partition by customer_id order by ds) as valid_to
from versions
```

`valid_to` is NULL for the current version.

## profiles.yml dev target

```yaml
<profile_name>:
  target: <dbt_target_dev>
  outputs:
    <dbt_target_dev>:
      type: bigquery
      method: oauth
      project: <gcp_project_dev>
      dataset: <dev_dataset>
      location: <bigquery_location>
      maximum_bytes_billed: <dev_max_bytes_billed>
      threads: 4
```

No keyfile. Credentials come from `gcloud auth application-default login`.
