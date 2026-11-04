# Plan: daily revenue by country

## Cards
1. **Contract** (sonnet): `project/contracts/orders.odcs.yaml` for `raw.orders`. Done when it validates against the ODCS v3.2.0 schema.
2. **Staging** (sonnet): `stg_orders`, renames from `physicalName`, casts types. Done when `dbt parse` passes and the not-null and unique tests on `order_id` exist.
3. **Mart** (sonnet): `daily_revenue`, grain `order_date` x `country`, partitioned by `order_date`. Done when the unique-combination test on the grain exists.
4. **Tests** (sonnet): refund never exceeds gross; no email column in the mart. Done when each test is written to fail on a bad fixture.

## Data review
Run with `wraith:plan-data-review` before card 1.

- **Changed:** the first draft summed `amount_gross` only. The review pointed out refunds exist in the source, so revenue would be overstated. Plan now subtracts `amount_refunded` and tests it.
- **Changed:** the first draft grouped on `country` as stored, and `country` is nullable. Plan now maps null to `'UNKNOWN'` so rows are not dropped from the totals.
- **Kept:** partition by `order_date`; no clustering until a query needs it.
