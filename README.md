# CareFlow: Clinical Pathway Process Mining

Infotact Solutions internship project (Data Analytics, Project 3).

## Problem
Hospital emergency room dashboards report an average waiting time, but they
do not show the real sequence of steps each patient follows. CareFlow rebuilds
the actual patient journeys from event logs, finds repeated or unusual paths
(for example, patients sent back to Triage after an X-Ray), and shows where
time is lost.

## Pipeline
Python simulator -> BigQuery (raw table) -> dbt (clean event log)
-> PM4Py (process discovery) -> Power BI dashboard

## Event log format
| Column | Description |
|---|---|
| Case_ID | One patient visit |
| Activity_Name | Hospital step (Registration, Triage, Doctor, X-Ray, Treatment, Discharge) |
| Timestamp | When the step happened (UTC, ISO format) |

Optional extra columns for dashboard filters: Resource, Doctor_ID, Age_Group, Department.

All data in this project is simulated. No real patient information is used.

## Team
| Member | Role | Branch |
|---|---|---|
| Sai Akshaya | Python and data generation (Data Engineer) | Sai-Akshaya-D |
| Adarsh Porwal | BigQuery and dbt (Data Pipeline Engineer) | Adrash-Porwal |
| Shivasakthi S | PM4Py and process discovery (Process Analytics Engineer) | SHIVASAKTHI |

## Repository structure
- `simulator/`   mock data generator and validation script
- `data/`        small sample files only
- `warehouse/`   BigQuery setup and load scripts
- `dbt_project/` dbt models
- `mining/`      PM4Py scripts
- `dashboard/`   Power BI files and notes
- `docs/`        schema, validation report, weekly logs

## Git workflow
1. Work only on your own branch.
2. Commit small, meaningful changes at least once a day.
3. Open a pull request into `main`. The Team Lead reviews and merges.
4. Never commit passwords, keys, `.env` files or `profiles.yml`.

## Weekly plan
- Week 1: generate mock data, load it into BigQuery, set up dbt.
- Week 2: clean the data with dbt, discover the process with PM4Py.
- Week 3: bottleneck calculations and Power BI dashboard.
- Week 4: conformance checking, polish, report and presentation.

## Setup
Instructions will be added as each part is built.
