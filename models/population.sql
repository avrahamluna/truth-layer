-- population.sql
-- The single population definition, reused by the entire report.
-- Rule: one population, one method, whole report. (see docs/COUNTING_RULES.md)
--
-- Trusted population = customers verified in BOTH the payments source AND the
-- app source (the intersection). Deltas are logged, not hidden.

WITH paid_customers AS (
    -- app source: at least one paid order
    SELECT DISTINCT customer_id
    FROM orders
    WHERE status = 'paid'
),

charged_customers AS (
    -- payments source: at least one succeeded charge
    SELECT DISTINCT customer_id
    FROM charges
    WHERE status = 'succeeded'
),

trusted_population AS (
    -- intersection: verified in both sources
    SELECT customer_id
    FROM paid_customers
    INTERSECT
    SELECT customer_id
    FROM charged_customers
)

SELECT customer_id
FROM trusted_population;
