{{ config(materialized='table') }}

WITH patient_transitions AS (
    SELECT
        case_id,
        activity_name AS from_activity,

        LEAD(activity_name) OVER (
            PARTITION BY case_id
            ORDER BY event_timestamp
        ) AS to_activity,

        TIMESTAMP_DIFF(
            LEAD(event_timestamp) OVER (
                PARTITION BY case_id
                ORDER BY event_timestamp
            ),
            event_timestamp,
            MINUTE
        ) AS transition_minutes

    FROM {{ ref('event_log') }}
),

classified_transitions AS (
    SELECT
        *,
        CASE
            WHEN from_activity LIKE 'Release%'
                 AND to_activity = 'Return ER'
                THEN 'Return Visit'

            WHEN to_activity = 'Return ER'
                THEN 'Return Visit Entry'

            WHEN from_activity LIKE 'Release%'
                THEN 'Discharge Related'

            ELSE 'Other Transition'
        END AS transition_category

    FROM patient_transitions
    WHERE to_activity IS NOT NULL
      AND transition_minutes >= 0
)

SELECT
    from_activity,
    to_activity,
    transition_category,
    COUNT(*) AS transition_count,

    ROUND(AVG(transition_minutes), 2)
        AS avg_transition_minutes,

    APPROX_QUANTILES(
        transition_minutes, 100
    )[OFFSET(50)] AS median_transition_minutes,

    MIN(transition_minutes) AS min_transition_minutes,
    MAX(transition_minutes) AS max_transition_minutes

FROM classified_transitions
GROUP BY
    from_activity,
    to_activity,
    transition_category
