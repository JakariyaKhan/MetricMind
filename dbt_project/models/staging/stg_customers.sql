-- stg_customers.sql
SELECT
    customer_id,
    customer_name,
    segment,
    tier,
    signup_date,
    is_active
FROM raw_customers
