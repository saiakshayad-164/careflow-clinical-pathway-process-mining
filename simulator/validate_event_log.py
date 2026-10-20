"""Validate the CareFlow event log for the Member 1 checkpoint.

Run from the repository root:
    python simulator/validate_event_log.py

Input:
    data/event_log_clean.csv

Output:
    data/event_log_validated.csv
    docs/data_validation_report.md
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "event_log_clean.csv"
OUTPUT = ROOT / "data" / "event_log_validated.csv"

REQUIRED = ["Case_ID", "Activity_Name", "Timestamp"]


def validate_event_log(df):
    errors = []

    missing_columns = [c for c in REQUIRED if c not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")
        return errors

    if df["Case_ID"].isna().any():
        errors.append("Missing Case_ID values found.")

    if df["Activity_Name"].isna().any():
        errors.append("Missing Activity_Name values found.")

    timestamps = pd.to_datetime(df["Timestamp"], errors="coerce", utc=True)
    if timestamps.isna().any():
        errors.append("Invalid or missing timestamps found.")

    check = df.copy()
    check["Timestamp"] = timestamps
    check = check.sort_values(
        ["Case_ID", "Timestamp", "Activity_Name"], kind="stable"
    )

    differences = check.groupby("Case_ID")["Timestamp"].diff()
    if (differences < pd.Timedelta(0)).any():
        errors.append("Negative timestamp ordering found within a case.")

    return errors


def main():
    df = pd.read_csv(INPUT)
    errors = validate_event_log(df)

    duplicate_count = int(df.duplicated().sum())
    validated = df.drop_duplicates().copy()
    validated["Timestamp"] = pd.to_datetime(
        validated["Timestamp"], errors="coerce", utc=True
    )
    validated = validated.sort_values(
        ["Case_ID", "Timestamp", "Activity_Name"], kind="stable"
    )

    validated.to_csv(OUTPUT, index=False)

    print(f"Input rows: {len(df):,}")
    print(f"Exact duplicates removed: {duplicate_count:,}")
    print(f"Validated rows: {len(validated):,}")
    print(f"Cases: {validated['Case_ID'].nunique():,}")
    print(f"Activities: {validated['Activity_Name'].nunique():,}")

    if errors:
        print("\nVALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("\nVALIDATION PASSED")
    print(f"Validated file written to: {OUTPUT}")


if __name__ == "__main__":
    main()
