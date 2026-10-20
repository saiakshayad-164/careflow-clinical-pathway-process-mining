# Checkpoint 1 — sai_akshaya Handoff

## sai_akshaya: Python & Data Generation

### Completed

- Existing event-log conversion/cleaning reviewed.
- Clean event log validated.
- Missing core identifiers checked.
- Timestamp validity checked.
- Patient event ordering checked.
- Repeated activities and loop-like sequences checked.
- Exact duplicate rows removed from the validated handoff dataset.
- Reusable validation script added.
- Validation report added.

### Handoff file

`data/event_log_validated.csv`

### Core schema

`Case_ID | Activity_Name | Timestamp`

Optional fields retained:

`Resource | Age_Group`

### Result

The validated dataset is ready for the downstream BigQuery/dbt and PM4Py work.

**Important:** PM4Py/process discovery and BigQuery/dbt implementation remain the responsibilities of the other team members.

