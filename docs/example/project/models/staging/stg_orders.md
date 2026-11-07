# stg_orders.sql

Save this block as `models/staging/stg_orders.sql` in the dbt project.

```sql
select
    order_id,
    email as customer_email,
    ship_country as country,
    currency,
    cast(gross as numeric) as amount_gross,
    cast(refunded as numeric) as amount_refunded,
    created_ts as ordered_at
from {{ source('raw', 'raw_orders') }}
```
