# Power BI dashboard build guide

A native `.pbix` must be created and saved in Power BI Desktop; this repository includes the model outputs and starter DAX measures, not a binary Power BI report.

## Connect data

Recommended: connect Power BI to the BigQuery dbt outputs:
- `stg_event_log`
- `fct_case_pathways`
- `fct_transition_waits`

For a local prototype before BigQuery is configured, import `data/event_log_validated.csv`. Use the dbt outputs for the final report when available.

## Relationships

The case table `fct_case_pathways` is one row per `case_id`. Relate it to `stg_event_log` on `case_id` (one-to-many). `fct_transition_waits` is aggregated by activity pair; it is not a case-level table, so do not create an artificial case relationship to it.

## Suggested report pages

### 1. Overview
- Cards: Total Events, Patient Visits, Distinct Activities, Return ER Visits, Return ER Visit Rate
- Bar chart: event count by activity
- Slicers: event date, activity, resource, age group (where populated)

### 2. Bottlenecks
- Bar chart: mean inter-event gap by activity transition
- Table: activity, next activity, transition count, mean gap, median gap, maximum gap
- Sort by median or mean gap and show transition counts to avoid overemphasizing rare transitions

### 3. Pathways
- Table: observed pathway, visit count, share
- Bar chart: top observed variants
- Card: cases with repeated activities

### 4. Case drill-down
- Table filtered by case_id, ordered by event_timestamp
- Show activity, timestamp, resource and age group

Import starter measures from `PowerBI_measures.dax`.

## Interpretation and design notes

The elapsed time between two recorded events is an **inter-event gap**, not automatically a queue wait or clinician delay. Include transition counts alongside time metrics. Filter to a minimum transition count when highlighting potential bottlenecks. Avoid clinical claims or causal explanations based only on timestamps.

A discovered process model is descriptive. Conformance checking should only be presented after the team agrees on an independent reference process model and its allowed alternatives.
