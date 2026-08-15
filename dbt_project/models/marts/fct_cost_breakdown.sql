-- fct_cost_breakdown.sql
-- Materialized as gold mart table
SELECT
    c.cost_id,
    c.order_id,
    o.geography_id,
    DATE(o.order_timestamp) AS cost_date,
    'Q' || ((CAST(SUBSTR(o.order_timestamp, 6, 2) AS INTEGER) - 1) / 3 + 1) AS quarter,
    SUBSTR(o.order_timestamp, 1, 4) AS year,
    c.material_cost_usd,
    c.shipping_cost_usd,
    c.tariff_cost_usd,
    c.overhead_cost_usd,
    (c.material_cost_usd + c.shipping_cost_usd + c.tariff_cost_usd + c.overhead_cost_usd) AS total_cost_usd,
    c.carrier,
    c.cost_center
FROM stg_costs c
INNER JOIN stg_orders o ON c.order_id = o.order_id
