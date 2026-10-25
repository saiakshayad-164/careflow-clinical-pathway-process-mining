-- CareFlow: Final Event Log validation

SELECT
    COUNT(*) AS total_events,
    COUNT(DISTINCT case_id) AS total_cases,
    COUNTIF(case_id IS NULL) AS missing_case_ids,
    COUNTIF(activity_name IS NULL) AS missing_activities,
    COUNTIF(event_timestamp IS NULL) AS missing_timestamps
FROM `careflow-analytics-production.dbt_adarsh.event_log`;
