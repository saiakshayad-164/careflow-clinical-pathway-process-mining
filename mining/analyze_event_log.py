"""CareFlow process analytics from the validated event log.

Run from repository root:
    python -m pip install -r mining/requirements.txt
    python mining/analyze_event_log.py

Outputs are written to docs/generated/. PM4Py discovery is attempted when
PM4Py is installed; descriptive event-log analyses work with pandas alone.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "event_log_validated.csv"
OUT = ROOT / "docs" / "generated"
REQUIRED = {"Case_ID", "Activity_Name", "Timestamp"}


def load_log() -> pd.DataFrame:
    if not INPUT.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT}")
    df = pd.read_csv(INPUT)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["Case_ID"] = df["Case_ID"].astype("string").str.strip()
    df["Activity_Name"] = df["Activity_Name"].astype("string").str.strip()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["Case_ID", "Activity_Name", "Timestamp"])
    df = df.sort_values(["Case_ID", "Timestamp", "Activity_Name"]).reset_index(drop=True)
    return df


def analyze(df: pd.DataFrame) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    grouped = df.groupby("Case_ID", sort=False)
    ordered = df.copy()
    ordered["Next_Activity"] = grouped["Activity_Name"].shift(-1)
    ordered["Next_Timestamp"] = grouped["Timestamp"].shift(-1)
    ordered["Gap_Minutes"] = (
        ordered["Next_Timestamp"] - ordered["Timestamp"]
    ).dt.total_seconds() / 60
    transitions = ordered.dropna(subset=["Next_Activity", "Gap_Minutes"]).copy()
    transitions = transitions[transitions["Gap_Minutes"] >= 0]

    transition_summary = (
        transitions.groupby(["Activity_Name", "Next_Activity"], as_index=False)
        .agg(
            Transition_Count=("Gap_Minutes", "size"),
            Mean_Gap_Minutes=("Gap_Minutes", "mean"),
            Median_Gap_Minutes=("Gap_Minutes", "median"),
            P90_Gap_Minutes=("Gap_Minutes", lambda s: s.quantile(0.90)),
            Maximum_Gap_Minutes=("Gap_Minutes", "max"),
        )
        .sort_values(["Median_Gap_Minutes", "Transition_Count"], ascending=[False, False])
    )
    transition_summary.to_csv(OUT / "transition_summary.csv", index=False)

    variants = (
        df.groupby("Case_ID")["Activity_Name"]
        .agg(lambda s: " -> ".join(s.astype(str)))
        .value_counts()
        .rename_axis("Variant")
        .reset_index(name="Case_Count")
    )
    variants["Share_Percent"] = variants["Case_Count"] / df["Case_ID"].nunique() * 100
    variants.to_csv(OUT / "case_variants.csv", index=False)

    repeated = grouped["Activity_Name"].apply(lambda s: s.duplicated().any())
    consecutive = grouped["Activity_Name"].apply(lambda s: s.eq(s.shift()).any())
    return_cases = set(df.loc[df["Activity_Name"].eq("Return ER"), "Case_ID"].astype(str))
    case_ids = set(df["Case_ID"].astype(str))
    activity_counts = df["Activity_Name"].value_counts().to_dict()

    summary = {
        "events": int(len(df)),
        "cases": int(df["Case_ID"].nunique()),
        "activities": int(df["Activity_Name"].nunique()),
        "timestamp_start_utc": df["Timestamp"].min().isoformat(),
        "timestamp_end_utc": df["Timestamp"].max().isoformat(),
        "cases_with_repeated_activity": int(repeated.sum()),
        "cases_with_consecutive_repeat": int(consecutive.sum()),
        "cases_with_return_er": int(len(return_cases)),
        "return_er_case_rate_percent": round(len(return_cases) / len(case_ids) * 100, 2) if case_ids else 0,
        "activity_event_counts": activity_counts,
        "mean_inter_event_gap_minutes": round(float(transitions["Gap_Minutes"].mean()), 2) if len(transitions) else None,
        "median_inter_event_gap_minutes": round(float(transitions["Gap_Minutes"].median()), 2) if len(transitions) else None,
        "metric_note": "Inter-event gap is elapsed time between recorded events; it is not necessarily queue or clinician waiting time.",
    }
    (OUT / "summary_metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Return ER sequence detail, retaining the previous activity and elapsed time.
    return_rows = ordered[ordered["Activity_Name"].eq("Return ER")].copy()
    return_rows[["Case_ID", "Timestamp", "Next_Activity", "Gap_Minutes"]].to_csv(
        OUT / "return_er_events.csv", index=False
    )

    pm4py_result = "PM4Py not installed; descriptive analysis completed."
    try:
        import pm4py
        from pm4py.objects.conversion.log import converter as log_converter
        from pm4py.algo.discovery.inductive import algorithm as inductive_miner
        from pm4py.visualization.petri_net import visualizer as pn_visualizer

        pm_df = df.rename(columns={
            "Case_ID": "case:concept:name",
            "Activity_Name": "concept:name",
            "Timestamp": "time:timestamp",
        })
        event_log = log_converter.apply(pm_df, variant=log_converter.Variants.TO_EVENT_LOG)
        net, initial_marking, final_marking = inductive_miner.apply(event_log)
        gviz = pn_visualizer.apply(net, initial_marking, final_marking)
        pn_visualizer.save(gviz, str(OUT / "inductive_process_model.png"))
        pm4py_result = f"PM4Py Inductive Miner completed for {len(event_log)} cases."
    except ImportError:
        pass
    except Exception as exc:
        pm4py_result = f"PM4Py discovery could not complete: {type(exc).__name__}: {exc}"

    summary["pm4py_status"] = pm4py_result
    (OUT / "summary_metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"\nGenerated reports: {OUT}")


if __name__ == "__main__":
    analyze(load_log())
