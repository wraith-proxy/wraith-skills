# Review: daily revenue by country

Checklist: contract matches models, personal data stays out, grain is tested, cost is bounded, plan followed.

## Blocker (fixed)
- `daily_revenue` model first said `group by order_date, country`. In BigQuery `country` there can resolve to the raw nullable column rather than the `coalesce(...)` alias, so null-country orders would form a separate group and the `UNKNOWN` bucket the plan promised would not appear. Fixed with `group by 1, 2`. Add a fixture row with a null country to the grain test when the project first runs against a dev target.

## Suggestions
- `schema.yml` has no test that `amount_refunded <= amount_gross`. The plan's card 4 asks for it; add it as a singular test.
- Plan card 4 also asks for a test that no email column reaches the mart; `schema.yml` has neither that nor the refund test yet.
- `orders_other_currency` is a count, not money. The name is fine; say so in the model description.

## Nits
- `packages.yml` pins a range; commit the lock file once `dbt deps` has run.

## Checked and fine
- `customer_email` appears in staging only; the mart selects no email column.
- Partitioned by `order_date`; no clustering, as the plan said.
- Contract has an owning team and a classification for every property.

## Not checked
No `dbt parse`, `dbt build` or contract validation was run for this example. Run them before relying on any of it.

**Verdict:** approve once the refund test is added.
