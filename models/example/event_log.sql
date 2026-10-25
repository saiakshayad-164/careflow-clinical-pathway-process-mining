{{ config(materialized='table') }}

SELECT
    case_id,
    activity_name,
    event_timestamp,
    resource,
    age_group
FROM {{ ref('stg_hospital_events') }}
WHERE
    case_id IS NOT NULL
    AND activity_name IS NOT NULL
    AND event_timestamp IS NOT NULL
