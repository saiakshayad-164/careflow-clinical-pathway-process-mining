# CareFlow Weeks 3–4 completion and handover status

## Implemented on branch Sai-Akshaya-D

- Validated event log committed at `data/event_log_validated.csv`.
- Reproducible event-log descriptive analysis and optional PM4Py Inductive Miner discovery: `mining/analyze_event_log.py`.
- Transition summary, case variants, Return ER event export and KPI JSON are generated under `docs/generated/` when the script is run locally.
- Interactive Streamlit dashboard: `dashboard/app.py`.
- Dashboard dependencies and run instructions: `dashboard/requirements.txt`, `dashboard/README.md`.
- BigQuery raw table DDL and loading instructions: `warehouse/schema.sql`, `warehouse/README.md`.
- dbt source, staging model, case pathway mart, transition mart and schema tests: `dbt_project/`.
- Power BI starter measures and report layout guide: `dashboard/PowerBI_measures.dax`, `docs/powerbi_dashboard_guide.md`.

## Required execution/validation before declaring the whole project complete

1. Run the process analysis locally and inspect the PM4Py model output.
2. Create the BigQuery dataset, load the CSV, and run `dbt debug`, `dbt run`, and `dbt test` using the team's actual GCP project and region.
3. Validate the dbt mart results against the local pandas summaries.
4. Build and save the native Power BI `.pbix` in Power BI Desktop if required by the internship deliverable.
5. Obtain the team's approved reference pathway/model before performing and reporting conformance checking. Do not treat the discovered model as its own conformance reference.
6. Review dataset license/provenance and confirm with the team lead whether the current XES-derived Sepsis Cases log satisfies the requirement for simulated data.

## Important limitations

- The current data is converted from a Sepsis Cases XES event log; it is not a newly generated synthetic hospital dataset.
- BigQuery/dbt cannot be executed against the team's cloud project without authorized project access and credentials.
- A Streamlit app is a runnable interactive dashboard, but it is not a native Power BI `.pbix` report.
- Inter-event gaps are descriptive elapsed times between recorded events and do not prove queue time, staffing delay, or clinical causality.
- Conformance checking is intentionally not fabricated: it needs an independently approved reference model.
