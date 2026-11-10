# CareFlow Dashboard

This repository includes a runnable Streamlit dashboard for interactive exploration of the validated event log. The original project brief names Power BI as the intended presentation tool; this Streamlit app is a working dashboard implementation/prototype, not a native Power BI `.pbix` file.

## Run locally

From the repository root:

```bash
python -m pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

The dashboard automatically loads `data/event_log_validated.csv`. You can also upload a CSV containing `Case_ID`, `Activity_Name`, and `Timestamp`.

## Dashboard features

- Visit, event, activity and Return ER KPIs
- Event counts by activity
- Transitions ranked by median inter-event gap
- Most common observed pathways
- Transition-level mean, median and maximum gaps
- Case-level event drill-down
- Date, activity and resource filters
- Filtered CSV export

## Metric definition and limitations

The dashboard computes elapsed time between consecutive recorded events within each case. It calls this **inter-event gap**, not a confirmed queue or clinician waiting time. Event timestamps alone do not establish why a delay occurred. Use the metric to identify transitions for operational investigation, not to make clinical or staffing conclusions without validation.

The committed dataset is derived from historical sepsis-care pathway event records. Do not describe it as newly generated synthetic data unless the source is replaced with generated data and provenance is updated.
