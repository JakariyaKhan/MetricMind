-- stg_orders.sql
SELECT
    order_id,
    customer_id,
    geography_id,
    CAST(order_timestamp AS TIMESTAMP) AS order_timestamp,
    product_category,
    gross_revenue_usd,
    discount_amount_usd,
    net_revenue_usd,
    units_sold,
    status
FROM raw_orders
WHERE status = 'COMPLETED'
