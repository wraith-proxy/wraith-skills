# Ship: daily revenue by country

## Checks to run before merge (not run for this example)
- [ ] Contract validates against the ODCS v3.2.0 JSON Schema.
- [ ] Copy each block in `project/models/*/*.md` into a `.sql` file under `models/`, then `dbt deps && dbt parse` passes.
- [ ] After copying the blocks into `.sql` files under `models/`, `dbt build --target dev --select stg_orders daily_revenue` passes against a dev dataset.
- [ ] Row count and total revenue compared with finance's current spreadsheet for one closed week.

## Changelog line
Add `analytics.daily_revenue`: GBP revenue per day per shipping country, refunds subtracted, personal data excluded.

## PR body
Adds the daily revenue mart for finance. Contract first, then staging, then the mart. Plan review changed two things (refunds, null country); code review caught one grouping bug. Rollout: first build is a full build into `analytics`, no existing table is touched. Rollback: drop `analytics.daily_revenue`.
