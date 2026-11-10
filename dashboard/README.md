# CareFlow Pathway Studio

A focused, interactive dashboard for exploring patient-visit event logs. It is designed around four simple workspaces rather than a crowded wall of charts.

## Run locally

From the repository root:

```bash
python -m pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

The dashboard loads `data/event_log_validated.csv` automatically. You can also upload a CSV containing `Case_ID`, `Activity_Name`, and `Timestamp`.

## What makes this dashboard different

- **Light / Dark appearance switch** in the sidebar
- **Overview:** compact KPIs, activity footprint and transitions worth investigating
- **Pathway fingerprints:** compare common full visit sequences and inspect their step-by-step pattern
- **Loopback watch:** find cases containing repeated activities or a Return ER event
- **Journey explorer:** inspect one visit's ordered activity timeline and elapsed gaps
- **Data health:** review core-field, timestamp and duplicate checks
- **Exports:** download a single case or the currently filtered event rows

## Design principles

- Four tabs keep related analysis together and avoid chart overload.
- Filters live in one sidebar.
- The transition calculations use the complete date-filtered event sequence. Activity/resource filters do not create artificial transitions by skipping events.
- Theme selection changes both the interface and chart template.

## Metric interpretation

Elapsed time between two consecutive recorded events is called an **inter-event gap**. It is not automatically queue time or clinician waiting time, and it does not prove why an interval occurred. Repeated activities and Return ER events are descriptive patterns for investigation, not proof of poor care or avoidable readmission.

The committed dataset is derived from a Sepsis Cases XES event log; it is not newly generated synthetic data.
