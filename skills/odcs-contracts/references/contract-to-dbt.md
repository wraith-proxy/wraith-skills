# Contract to dbt

How each part of an ODCS contract maps to dbt models and tests on BigQuery.
Generated models are never hand-edited; change the contract and regenerate.
Model conventions are in wraith:dbt-bigquery.

## Schema object to raw model

One raw model per schema object, named from `physicalName`.

- Materialization: `incremental`, strategy `merge`, `unique_key` set to the
  properties with `primaryKey: true`.
- Select columns by `physicalName` from the source. A column the contract
  lists but the source lacks fails generation (rule 8); never default it.
- Deduplicate on the key with `row_number()` over the key, ordered by the
  source's change timestamp descending, keeping row number 1.
- Read new rows with a lookback window, for example the last 3 days before
  the high-water mark. A strict greater-than high-water mark skips late
  rows; the merge makes the overlap safe.

```sql
select * except (rn) from (
  select *, row_number() over (
    partition by cust_id order by updated_ts desc) as rn
  from {{ source('raw', 'raw_customers') }}
  {% if is_incremental() %}
  where updated_ts > timestamp_sub(
    (select max(updated_ts) from {{ this }}), interval 3 day)
  {% endif %}
) where rn = 1
```

## Raw to staging model

One staging model per object, a daily snapshot.

- Materialization: `incremental`, strategy `insert_overwrite`, partitioned
  by `ds` (the snapshot date), so a rerun replaces that day only.
- Rename `physicalName` to the contract `name`.
- Cast to the property's `physicalType` with `safe_cast` only where the
  contract says the raw type differs; otherwise a bad value should fail.

## Quality to tests

| Contract | dbt |
|---|---|
| `metric: nullValues`, `mustBe: 0` | `not_null` |
| `required: true` | `not_null` |
| `primaryKey: true` | `unique` (combined key: `unique_combination_of_columns`) |
| `metric: rowCount` with a bound | a row-count test with `min_value` |
| `severity: warn` | test `severity: warn` |

A quality rule with no dbt equivalent becomes a singular test under
`tests/`, named after the rule.

## SLAs to source freshness

`slaProperties` entry with `property: freshness` maps to the source's
`freshness` block: `warn_after` and `error_after` take the `value` and
`unit` (`h` is `hour`). `element` names the `loaded_at_field`. The entry's
`description` says what happens on breach; put it in the source `meta`.

## Classification to encryption

Each property with a sensitive `classification` (for example `pii`) is
encrypted or masked in the staging model, and access to it follows the
class. Which step and which key are decided in wraith:bigquery. Properties
labelled `public` or `internal` pass through unchanged.

## Drift check

CI regenerates the models from the contract and diffs them against disk. Any
difference fails the build (rule 10).
