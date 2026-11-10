
-- CareFlow: Transition Metrics Validation
-- Purpose: Validate transition counts by category
-- Dataset: dbt_adarsh

WITH category_summary AS (
    SELECT
        transition_category,
        COUNT(*) AS total_transition_types,
        SUM(transition_count) AS total_transitions
    FROM
        `careflow-analytics-production.dbt_adarsh.mart_transition_times`
    GROUP BY
        transition_category
)

SELECT
    transition_category,
    total_transition_types,
    total_transitions
FROM category_summary

UNION ALL

SELECT
    'TOTAL' AS transition_category,
    SUM(total_transition_types),
    SUM(total_transitions)
FROM category_summary

ORDER BY
    CASE
        WHEN transition_category = 'TOTAL' THEN 1
        ELSE 0
    END,
    transition_category;
