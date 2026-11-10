{{ config(materialized='table') }}

WITH sequenced_events AS (

    SELECT
        case_id,
        activity_name AS from_activity,
        event_timestamp AS from_time,

        LEAD(activity_name) OVER (
            PARTITION BY case_id
            ORDER BY event_timestamp
        ) AS to_activity,

        LEAD(event_timestamp) OVER (
            PARTITION BY case_id
            ORDER BY event_timestamp
        ) AS to_time

    FROM {{ ref('event_log') }}

),

actual_transitions AS (

    SELECT *
    FROM sequenced_events
    WHERE to_activity IS NOT NULL

),

classified_transitions AS (

    SELECT
        a.case_id,
        a.from_activity,
        a.to_activity,
        a.from_time,
        a.to_time,

        TIMESTAMP_DIFF(
            a.to_time,
            a.from_time,
            MINUTE
        ) AS transition_minutes,

        CASE
            WHEN a.from_activity LIKE 'Release %'
                 AND a.to_activity = 'Return ER'
                THEN 'RETURN_VISIT_REVIEW'

            WHEN e.from_activity IS NOT NULL
                THEN 'COMPLIANT'

            ELSE 'UNEXPECTED_REVIEW'
        END AS conformance_status

    FROM actual_transitions a

    LEFT JOIN {{ ref('expected_transitions') }} e
        ON a.from_activity = e.from_activity
        AND a.to_activity = e.to_activity

)

SELECT *
FROM classified_transitions
