SELECT
    COUNT(*) AS total_cases,
    SUM(total_transitions) AS total_transitions,
    SUM(compliant_transitions) AS compliant_transitions,
    SUM(unexpected_transitions) AS unexpected_transitions,
    SUM(return_visit_transitions) AS return_visit_transitions
FROM `careflow-analytics-production.dbt_adarsh.mart_case_conformance`;
