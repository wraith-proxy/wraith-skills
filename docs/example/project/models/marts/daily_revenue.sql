{{ config(
    partition_by={'field': 'order_date', 'data_type': 'date'}
) }}

select
    date(ordered_at) as order_date,
    coalesce(country, 'UNKNOWN') as country,
    sum(case when currency = 'GBP' then amount_gross - amount_refunded else 0 end) as revenue_gbp,
    countif(currency != 'GBP') as orders_other_currency
from {{ ref('stg_orders') }}
group by 1, 2
