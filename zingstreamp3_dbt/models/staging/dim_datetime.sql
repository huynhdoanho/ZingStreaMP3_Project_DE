{{ config(materialized = 'table') }}

WITH date_series AS
(
    SELECT
        generate_series('2023-10-01'::TIMESTAMP, '2024-12-31'::TIMESTAMP, INTERVAL '1 HOUR') AS date
)
SELECT
    EXTRACT(EPOCH FROM date) AS dateKey,
    date,
    EXTRACT(DOW FROM date) AS dayOfWeek,
    EXTRACT(DAY FROM date) AS dayOfMonth,
    EXTRACT(WEEK FROM date) AS weekOfYear,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(YEAR FROM date) AS year,
    CASE WHEN EXTRACT(DOW FROM date) IN (0, 6) THEN True ELSE False END AS weekendFlag
FROM date_series
