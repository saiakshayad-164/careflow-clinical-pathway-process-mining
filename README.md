# CareFlow: Clinical Pathway Process Mining

Infotact Solutions internship project (Data Analytics, Project 3).

## Objective

CareFlow reconstructs patient journeys from event logs, identifies repeated or unusual activity sequences, and highlights long gaps between consecutive recorded events. These measures support operational investigation; they are not clinical diagnoses or proof of queue time.

## Current pipeline

CSV event log → BigQuery raw table → dbt staging and marts → pandas/PM4Py process analysis → interactive Streamlit dashboard

The original project plan names Power BI as the presentation target. The repository currently includes a runnable Streamlit dashboard. A native Power BI `.pbix` still needs to be authored and validated in Power BI Desktop if it is a formal deliverable.

## Event-log schema

| Column | Description |
|---|---|
| `Case_ID` | One patient visit/case |
| `Activity_Name` | Recorded clinical/process activity |
| `Timestamp` | Event timestamp (UTC) |
| `Resource` | Optional resource/group |
| `Age_Group` | Optional demographic band; may be missing |

## Data provenance

The current committed event log was converted from a Sepsis Cases XES event log using `simulator/convert_dataset.py`. It is **not newly generated synthetic data**. The current validated handoff contains 15,183 events across 1,049 cases after removing seven exact duplicate rows from the cleaned file. Review the data license/provenance before external redistribution. Do not claim that all repository data is simulated.

## Repository structure

- `simulator/` conversion and validation scripts
- `data/` event-log CSV files and raw source folder
- `warehouse/` BigQuery table schema and loading instructions
- `dbt_project/` staging model, analytical marts and tests
- `mining/` event-log analytics and PM4Py process discovery
- `dashboard/` interactive dashboard and dependencies
- `docs/` validation and analysis documentation

## Quick start: dashboard

From the repository root:

```bash
python -m pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```


## Deploy the dashboard

Deploy the Streamlit app using [Streamlit Community Cloud](https://share.streamlit.io/deploy?repository=saiakshayad-164/careflow-clinical-pathway-process-mining&branch=Sai-Akshaya-D&mainModule=dashboard%2Fapp.py).

1. Sign in to Streamlit Community Cloud with GitHub and authorize access to this repository.
2. Select repository `saiakshayad-164/careflow-clinical-pathway-process-mining`, branch `Sai-Akshaya-D`, and main file `dashboard/app.py`.
3. Select **Deploy** and wait for the app to finish building.
4. Copy the public app URL provided by Streamlit and add it here as the live dashboard link.

The repository contains the deployment configuration target, but the public app URL is created only after deployment is completed in Streamlit Community Cloud. The dashboard reads the committed `data/event_log_validated.csv` file by default.

## Quick start: process analysis

```bash
python -m pip install -r mining/requirements.txt
python mining/analyze_event_log.py
```

Outputs are written to `docs/generated/`. PM4Py model discovery is attempted when its dependencies are installed.

## BigQuery and dbt

See [warehouse setup](warehouse/README.md) for raw table creation, CSV loading, OAuth authentication and dbt commands. Never commit service-account keys, `.env` files or local `profiles.yml`.

## Team branches

| Contributor | Responsibility | Branch |
|---|---|---|
| Sai Akshaya | Python, event-log preparation and validation | `Sai-Akshaya-D` |
| Adarsh Porwal | BigQuery and dbt | `Adarsh-Porwal` (confirm exact spelling in GitHub) |
| Shivasakthi S | PM4Py and process discovery | `SIVASAKTHI-S` (confirm exact spelling in GitHub) |

## Weekly plan

- Week 1: event data preparation, warehouse and dbt setup
- Week 2: event-log cleaning and process discovery
- Week 3: bottleneck calculations and dashboard
- Week 4: conformance checking against an approved reference model, polish, report and presentation

## Interpretation cautions

- The elapsed time between two recorded events is called an **inter-event gap**. It is not automatically a queue or clinician waiting time.
- A discovered process model describes the observed log; it is not a normative clinical pathway.
- Genuine conformance checking requires a separately approved reference model.
- Missing optional fields such as `Age_Group` should not be treated as missing core event identifiers.
