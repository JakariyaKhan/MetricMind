-- stg_costs.sql
SELECT
    cost_id,
    order_id,
    material_cost_usd,
    shipping_cost_usd,
    tariff_cost_usd,
    overhead_cost_usd,
    carrier,
    cost_center
FROM raw_costs
