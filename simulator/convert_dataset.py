"""Convert the downloaded XES event log into the team's flat CSV format.

Run from the repo root:  python simulator/convert_dataset.py
Reads any .xes / .xes.gz file in data/raw/ (no need to extract it).
Writes data/event_log.csv with: Case_ID, Activity_Name, Timestamp,
Resource, Age_Group
"""
import glob
import sys

import pandas as pd
import pm4py

files = glob.glob("data/raw/*.xes*")
if not files:
    sys.exit("No .xes or .xes.gz file found in data/raw/")
src = files[0]
print("Reading:", src)

df = pm4py.read_xes(src)
df = pd.DataFrame(df)
print("Columns found:", df.columns.tolist())

out = pd.DataFrame({
    "Case_ID": df["case:concept:name"],
    "Activity_Name": df["concept:name"],
    "Timestamp": pd.to_datetime(df["time:timestamp"], utc=True),
})
out["Resource"] = df["org:group"] if "org:group" in df else None
if "Age" in df:
    out["Age_Group"] = pd.cut(pd.to_numeric(df["Age"], errors="coerce"),
                              [0, 17, 35, 60, 120],
                              labels=["0-17", "18-35", "36-60", "60+"])

out = out.sort_values(["Case_ID", "Timestamp"])
out.to_csv("data/event_log.csv", index=False)

print("Rows:", len(out), "| Cases:", out["Case_ID"].nunique())
print("Date range:", out["Timestamp"].min(), "to", out["Timestamp"].max())
print("\nActivities:")
print(out["Activity_Name"].value_counts())
