-- dim_dates.sql
WITH date_spine AS (
    SELECT DISTINCT DATE(order_timestamp) AS date_day
    FROM stg_orders
)
SELECT
    date_day,
    SUBSTR(date_day, 1, 4) AS year,
    'Q' || ((CAST(SUBSTR(date_day, 6, 2) AS INTEGER) - 1) / 3 + 1) AS quarter,
    SUBSTR(date_day, 6, 2) AS month,
    SUBSTR(date_day, 9, 2) AS day
FROM date_spine
ORDER BY date_day
