# CareFlow dbt project

This project transforms the BigQuery raw event table into a deduplicated staging view and two analytical marts.

- `stg_event_log`: casts and filters required fields, removes exact duplicate event rows.
- `fct_transition_waits`: groups consecutive activity transitions and calculates inter-event gap metrics.
- `fct_case_pathways`: produces one row per visit with observed pathway, duration and Return ER flag.
- `schema.yml`: basic not-null and uniqueness tests.

See [../warehouse/README.md](../warehouse/README.md) for BigQuery loading, OAuth setup and dbt commands. Do not commit `profiles.yml` or credentials.
