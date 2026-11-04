# Design: daily revenue by country

## Consumer and question
Finance reads one chart: revenue per day per country. They need yesterday's figure by 08:00 UTC.

## Grain
One row per `order_date` and `country`.

## Source
`raw.orders`, owned by the storefront team. One row per order. Loaded hourly.

## Decisions
1. Revenue is `amount_gross` minus `amount_refunded`, summed in the order's currency. Currency conversion is out of scope; the mart is GBP-only and filters to `currency = 'GBP'`. Other currencies are counted in a separate column so nothing disappears silently.
2. `customer_email` is personal data. It is classified `pii` in the contract and never leaves staging.
3. Freshness SLA: 24 hours on `order_date`. On breach the owning team is told.

## Cost and blast radius
Table is small and partitioned by `order_date`. A full rebuild scans the orders table once. No production writes outside the `analytics` dataset.

## Not doing
Currency conversion, customer-level reporting, backfill before 2024-01-01.
