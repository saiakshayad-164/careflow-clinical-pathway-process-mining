
-- =====================================================
-- CareFlow Project
-- Transition Metrics Validation
-- BigQuery and dbt Data Quality Checks
-- =====================================================

-- Check transition counts by category
SELECT
    transition_category,
    COUNT(*) AS total_transition_types,
    SUM(transition_count) AS total_transitions,
    ROUND(AVG(avg_transition_minutes), 2)
        AS average_transition_minutes,
    MIN(min_transition_minutes)
        AS minimum_transition_minutes,
    MAX(max_transition_minutes)
        AS maximum_transition_minutes
FROM
    `careflow-analytics-production.dbt_adarsh.mart_transition_times`
GROUP BY
    transition_category
ORDER BY
    total_transitions DESC;

-- Validate overall transition count
SELECT
    COUNT(*) AS total_transition_types,
    SUM(transition_count) AS total_transitions,
    COUNTIF(transition_category = 'Return Visit')
        AS return_visit_transition_types,
    COUNTIF(transition_category = 'Discharge Related')
        AS discharge_transition_types
FROM
    `careflow-analytics-production.dbt_adarsh.mart_transition_times`;

