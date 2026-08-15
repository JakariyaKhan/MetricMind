"""
MetricMind - dbt Transformation Engine
Executes SQL transformation DAG from raw tables -> staging views -> gold dimensional marts.
Provides verified, tested Lakehouse tables for the Semantic Layer.
"""

import os
import sqlite3

def run_transformations(db_path: str = "metricmind_lakehouse.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("[*] Running dbt Staging Transformations...")
    # Staging views
    cursor.executescript("""
    DROP VIEW IF EXISTS stg_orders;
    CREATE VIEW stg_orders AS
    SELECT
        order_id,
        customer_id,
        geography_id,
        order_timestamp,
        product_category,
        gross_revenue_usd,
        discount_amount_usd,
        net_revenue_usd,
        units_sold,
        status
    FROM raw_orders
    WHERE status = 'COMPLETED';

    DROP VIEW IF EXISTS stg_costs;
    CREATE VIEW stg_costs AS
    SELECT
        cost_id,
        order_id,
        material_cost_usd,
        shipping_cost_usd,
        tariff_cost_usd,
        overhead_cost_usd,
        carrier,
        cost_center
    FROM raw_costs;

    DROP VIEW IF EXISTS stg_geography;
    CREATE VIEW stg_geography AS
    SELECT
        geography_id,
        region,
        country,
        country_code,
        currency
    FROM raw_geography;

    DROP VIEW IF EXISTS stg_customers;
    CREATE VIEW stg_customers AS
    SELECT
        customer_id,
        customer_name,
        segment,
        tier,
        signup_date,
        is_active
    FROM raw_customers;
    """)

    print("[*] Materializing Gold Analytical Marts...")
    cursor.executescript("""
    DROP TABLE IF EXISTS dim_geography;
    CREATE TABLE dim_geography AS
    SELECT
        geography_id,
        region,
        country,
        country_code,
        currency
    FROM stg_geography;

    DROP TABLE IF EXISTS dim_customers;
    CREATE TABLE dim_customers AS
    SELECT
        customer_id,
        customer_name,
        segment,
        tier,
        signup_date,
        is_active
    FROM stg_customers;

    DROP TABLE IF EXISTS fct_orders;
    CREATE TABLE fct_orders AS
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
    LEFT JOIN stg_costs c ON o.order_id = c.order_id;

    DROP TABLE IF EXISTS fct_cost_breakdown;
    CREATE TABLE fct_cost_breakdown AS
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
    INNER JOIN stg_orders o ON c.order_id = o.order_id;

    -- Create optimal analytical indexes
    CREATE INDEX IF NOT EXISTS idx_fct_orders_geo ON fct_orders(geography_id);
    CREATE INDEX IF NOT EXISTS idx_fct_orders_date ON fct_orders(order_date);
    CREATE INDEX IF NOT EXISTS idx_fct_costs_geo ON fct_cost_breakdown(geography_id);
    """)

    conn.commit()
    
    # Audit row counts
    cursor.execute("SELECT COUNT(*) FROM fct_orders")
    order_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fct_cost_breakdown")
    cost_count = cursor.fetchone()[0]
    conn.close()

    print(f"[+] dbt Transformation Pipeline Complete! fct_orders: {order_count} rows, fct_cost_breakdown: {cost_count} rows.")

if __name__ == "__main__":
    run_transformations("metricmind_lakehouse.db")
