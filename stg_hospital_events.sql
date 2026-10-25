
{{ config(materialized='view') }}

SELECT
    CAST(Case_ID AS STRING) AS case_id,
    TRIM(Activity_Name) AS activity_name,
    Timestamp AS event_timestamp,
    Resource AS resource,
    Age_Group AS age_group
FROM `careflow-analytics-production.raw_ehr.clean_event_log`
WHERE
    Case_ID IS NOT NULL
    AND Activity_Name IS NOT NULL
    AND Timestamp IS NOT NULL
