
# CareFlow - Data Dictionary

## 1. Project Overview

CareFlow uses simulated hospital event log data to study
patient activity sequences and transition durations.

Google BigQuery is used for data storage and dbt is used
for data cleaning, transformation, and validation.

## 2. Source Data

| Property | Details |
|---|---|
| GCP Project | careflow-analytics-production |
| Raw Dataset | raw_ehr |
| Source Table | simulated_hospital_events |
| Transformed Dataset | dbt_adarsh |
| Total Source Events | 15,183 |
| Unique Patient Cases | 1,049 |

## 3. Source Table Columns

| Column | Description |
|---|---|
| Case_ID | Unique patient case identifier |
| Activity_Name | Name of the recorded hospital activity |
| Timestamp | Date and time of the event |
| Resource | Resource associated with the event |
| Age_Group | Age group associated with the patient |

## 4. Transformed Event Log

The event_log model provides a structured representation
of the patient activity records.

| Column | Description |
|---|---|
| case_id | Patient case identifier |
| activity_name | Standardized activity name |
| event_timestamp | Timestamp of the activity |
| resource | Associated resource |
| age_group | Patient age group |

## 5. Transition Metrics

The mart_transition_times model calculates the time
difference between consecutive activities for each case.

| Metric | Description |
|---|---|
| from_activity | Previous recorded activity |
| to_activity | Next recorded activity |
| transition_count | Number of observed transitions |
| avg_transition_minutes | Average time gap |
| median_transition_minutes | Median time gap |
| min_transition_minutes | Minimum time gap |
| max_transition_minutes | Maximum time gap |
| transition_category | Analytical transition classification |

## 6. Data Quality Checks

The required event log fields were validated.

- Total events: 15,183
- Unique cases: 1,049
- Missing case IDs: 0
- Missing activity names: 0
- Missing timestamps: 0

## 7. Analytical Considerations

Transition durations are calculated using consecutive
event timestamps within the same patient case.

Release-to-Return ER transitions are classified separately
because they may represent gaps between separate visits.

Large transition durations should not automatically be
treated as hospital waiting-time bottlenecks.

Repeated activities and zero-minute gaps should also be
considered during interpretation.

## 8. Project Scope

The BigQuery and dbt component is responsible for:

- Raw event data preparation
- Data cleaning and standardization
- Event log transformation
- Transition duration analysis
- Data quality validation
- Preparing structured data for downstream analysis
