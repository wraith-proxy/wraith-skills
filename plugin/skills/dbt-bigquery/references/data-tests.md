# Tests for SQL, dbt and generators

## dbt generic tests from contract quality rules

Generate the schema tests from the ODCS quality rules instead of writing them twice.

- `not_null` on every required column.
- `unique` on the key; on `ds` snapshots scope it to `(key, ds)`, since the same key repeats on every day.
- `relationships` to the parent model for every foreign key.
- `accepted_values` for every enumerated column.

## dbt unit tests for non-trivial SQL

Write a unit test when a model has window functions, CASE ladders or incremental predicates. Give the inputs as `given` rows and the independent, hand-worked answer as `expect` rows.

```yaml
unit_tests:
  - name: latest_status_wins
    model: dim_order
    given:
      - input: ref('stg_order_events')
        rows:
          - {order_id: 1, status: placed, event_ts: "2026-01-01 10:00:00"}
          - {order_id: 1, status: shipped, event_ts: "2026-01-02 09:00:00"}
    expect:
      rows:
        - {order_id: 1, status: shipped}
```

## Golden-file tests for generators

Compare generator output with a checked-in golden file. Regenerate only behind an environment flag such as `UPDATE_GOLDEN=1`, then review the diff like any other change. CI never updates goldens; a CI diff is a failure.

## Backtests for predictive models

Hold out whole periods (not random rows) so the model never sees the future. Report the error per period together with its mechanism: what drives it, such as a holiday, a new product or a data gap.

## Rules

- Mock only at system boundaries (BigQuery client, HTTP, clock); never mock your own code.
- Tests must survive a refactor: test behaviour, not implementation.
