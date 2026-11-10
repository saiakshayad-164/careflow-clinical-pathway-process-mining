# CareFlow — Clinical Pathway Process Mining

## Project Overview

CareFlow is a healthcare operations analytics project that uses timestamped hospital event logs to help analyze patient journeys and identify potential operational bottlenecks.

The project workflow includes:
- **Data generation:** Simulated hospital event logs created by the data-generation team.
- **Data warehouse:** Google BigQuery.
- **Data transformation:** dbt.
- **Process discovery:** PM4Py/Python, handled by a separate teammate.
- **Dashboard and reporting:** Power BI/BI tools, according to the team plan.

## My Contribution: BigQuery and dbt

My responsibility is the data warehouse and event-log engineering part of CareFlow.

### 1. BigQuery Data Pipeline

The simulated hospital event data was loaded into BigQuery.

- Source table: `careflow-analytics-production.raw_ehr.simulated_hospital_events`
- Cleaned table: `careflow-analytics-production.raw_ehr.clean_event_log`

The cleaning step standardizes column types, trims activity names, and excludes records missing a case ID, activity name, or timestamp.

### 2. dbt Models

**Staging model:** `stg_hospital_events`

- Standardizes column names.
- Exposes the case ID, activity, event timestamp, resource, and age group.
- Filters records with missing required fields.

**Normalized Event Log:** `event_log`

- Uses the staging model as its input through dbt's `ref()` function.
- Selects the fields required for downstream process mining.
- Materializes the final output as a BigQuery table.

### 3. Final Event Log Schema

| Column | Purpose |
|---|---|
| `case_id` | Identifies a patient case |
| `activity_name` | Records the hospital activity |
| `event_timestamp` | Records when the activity occurred |
| `resource` | Identifies the associated resource |
| `age_group` | Provides patient age-group information |

### 4. Validation Results

The final BigQuery Event Log was validated with these results:

- Total events: 15,183
- Distinct cases: 1,049
- Missing case IDs: 0
- Missing activities: 0
- Missing timestamps: 0
- dbt model build and configured not-null tests: PASS

These results describe the current simulated dataset and should be rechecked if the source data changes.

### 5. BigQuery Output

The final table is:

`careflow-analytics-production.dbt_adarsh.event_log`

The table is intended for use by the process-mining teammate as the input to PM4Py.

Events should be ordered by `case_id` and `event_timestamp` during downstream processing. A SQL table does not guarantee persistent row order by itself.

## BigQuery and dbt Data Engineering

### Overview
The BigQuery and dbt component of CareFlow is responsible for preparing, cleaning, transforming, and validating simulated hospital event log data for process mining analysis.

### Data Warehouse
- Cloud Platform: Google BigQuery
- GCP Project: `careflow-analytics-production`
- Raw Dataset: `raw_ehr`
- Transformed Dataset: `dbt_adarsh`
- Source Table: `simulated_hospital_events`

### Data Preparation
The raw hospital event log contains 15,183 records across 1,049 unique patient cases. The cleaning process standardizes case identifiers, trims activity names, and filters records with missing essential fields.

### dbt Models
1. `stg_hospital_events.sql` – Standardizes source columns and prepares staging data.
2. `event_log.sql` – Creates the structured patient event log.
3. `mart_transition_times.sql` – Calculates consecutive activity transition counts and duration metrics.

### Transition Analysis
The transition analysis includes:
- Transition frequency between consecutive activities.
- Average transition duration in minutes.
- Median transition duration.
- Minimum and maximum transition duration.
- Classification of return visits and discharge-related transitions.

### Data Quality Validation
The pipeline uses dbt tests and BigQuery SQL validation queries to check required fields and transition metrics.

Verified event log:
- Total events: 15,183
- Unique patient cases: 1,049
- Missing case IDs: 0
- Missing activities: 0
- Missing timestamps: 0

### Team Contribution
The BigQuery and dbt work covers data ingestion, cleaning, transformation, transition analysis, and data quality validation. The resulting structured datasets support the team's process mining and Power BI analysis.

### Important Note
Transition durations represent differences between consecutive recorded event timestamps. Large gaps, repeated activities, and return visits require contextual investigation before being interpreted as confirmed hospital waiting-time bottlenecks.

### 6. Team Handoff

The BigQuery/dbt contribution provides a cleaned and normalized Event Log for downstream process discovery.

PM4Py process discovery, Python implementation, and dashboard development are handled separately by the respective teammates.

**Access note:** Access to the GitHub repository does not automatically grant access to the BigQuery project or dataset. Appropriate Google Cloud permissions are required to query the output table.

### Security

Do not commit service-account JSON keys, passwords, tokens, private credentials, or other secrets to GitHub.
