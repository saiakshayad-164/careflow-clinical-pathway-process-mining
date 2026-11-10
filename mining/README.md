# Process mining and event-log analysis

Run from the repository root:

```bash
python -m pip install -r mining/requirements.txt
python mining/analyze_event_log.py
```

The script writes descriptive outputs under `docs/generated/` and attempts PM4Py Inductive Miner discovery when PM4Py and its dependencies are installed.

Outputs:
- `summary_metrics.json`
- `transition_summary.csv`
- `case_variants.csv`
- `return_er_events.csv`
- `inductive_process_model.png` (when PM4Py discovery succeeds)

The discovered model describes the observed event log; it is not a clinical gold-standard pathway. Conformance checking requires a separately approved reference model and should not be claimed from discovery alone.
