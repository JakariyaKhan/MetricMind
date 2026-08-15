-- fct_orders.sql
-- Materialized as gold mart table
SELECT
    o.order_id,
    o.customer_id,
    o.geography_id,
    o.order_timestamp,
    DATE(o.order_timestamp) AS order_date,
    'Q' || ((CAST(SUBSTR(o.order_timestamp, 6, 2) AS INTEGER) - 1) / 3 + 1) AS quarter,
    SUBSTR(o.order_timestamp, 1, 4) AS year,
    o.product_category,
    o.gross_revenue_usd,
    o.discount_amount_usd,
    o.net_revenue_usd,
    o.units_sold,
    (c.material_cost_usd + c.shipping_cost_usd + c.tariff_cost_usd + c.overhead_cost_usd) AS total_cost_usd,
    (o.net_revenue_usd - (c.material_cost_usd + c.shipping_cost_usd + c.tariff_cost_usd + c.overhead_cost_usd)) AS gross_margin_usd,
    CASE 
        WHEN o.net_revenue_usd > 0 
        THEN ROUND(((o.net_revenue_usd - (c.material_cost_usd + c.shipping_cost_usd + c.tariff_cost_usd + c.overhead_cost_usd)) / o.net_revenue_usd) * 100.0, 2)
        ELSE 0.0 
    END AS gross_margin_pct
FROM stg_orders o
LEFT JOIN stg_costs c ON o.order_id = c.order_id
