-- ========================================================================
-- MetricMind - Snowflake / Lakehouse DDL Specification
-- Schema: ANALYTICS.RAW and ANALYTICS.GOLD
-- ========================================================================

-- RAW INGESTION SCHEMAS (BRONZE)
CREATE SCHEMA IF NOT EXISTS ANALYTICS.RAW;

CREATE TABLE IF NOT EXISTS ANALYTICS.RAW.RAW_GEOGRAPHY (
    geography_id INT PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code VARCHAR(10) NOT NULL,
    currency VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS ANALYTICS.RAW.RAW_CUSTOMERS (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    tier VARCHAR(50) NOT NULL,
    signup_date DATE NOT NULL,
    is_active INT NOT NULL
);

CREATE TABLE IF NOT EXISTS ANALYTICS.RAW.RAW_ORDERS (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    geography_id INT NOT NULL,
    order_timestamp TIMESTAMP NOT NULL,
    product_category VARCHAR(100) NOT NULL,
    gross_revenue_usd NUMERIC(14, 2) NOT NULL,
    discount_amount_usd NUMERIC(14, 2) NOT NULL,
    net_revenue_usd NUMERIC(14, 2) NOT NULL,
    units_sold INT NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS ANALYTICS.RAW.RAW_COSTS (
    cost_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    material_cost_usd NUMERIC(14, 2) NOT NULL,
    shipping_cost_usd NUMERIC(14, 2) NOT NULL,
    tariff_cost_usd NUMERIC(14, 2) NOT NULL,
    overhead_cost_usd NUMERIC(14, 2) NOT NULL,
    carrier VARCHAR(100) NOT NULL,
    cost_center VARCHAR(100) NOT NULL
);
