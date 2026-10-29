"""
CareFlow Week 3 - Transition Time Analysis

Calculates the time taken between consecutive activities
within each patient case.

Input:
    data/event_log_validated.csv

Output:
    docs/transition_time_analysis.csv
"""

from pathlib import Path
import pandas as pd


# Repository root
ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "event_log_validated.csv"
OUTPUT = ROOT / "docs" / "transition_time_analysis.csv"


def main():
    # Load validated event log
    df = pd.read_csv(INPUT, parse_dates=["Timestamp"])

    # Sort events chronologically within each case
    df = df.sort_values(
        ["Case_ID", "Timestamp"],
        kind="stable"
    ).copy()

    # Get the next activity and timestamp for each patient case
    df["Next_Activity"] = df.groupby("Case_ID")["Activity_Name"].shift(-1)
    df["Next_Timestamp"] = df.groupby("Case_ID")["Timestamp"].shift(-1)

    # Calculate transition time in hours
    df["Transition_Hours"] = (
        df["Next_Timestamp"] - df["Timestamp"]
    ).dt.total_seconds() / 3600

    # Keep only rows where a next activity exists
    transitions = df.dropna(
        subset=["Next_Activity", "Next_Timestamp"]
    ).copy()

    # Remove negative transition times if any invalid ordering exists
    transitions = transitions[
        transitions["Transition_Hours"] >= 0
    ]

    # Calculate statistics for each transition
    analysis = (
        transitions
        .groupby(
            ["Activity_Name", "Next_Activity"],
            as_index=False
        )
        .agg(
            Transition_Count=("Transition_Hours", "count"),
            Average_Hours=("Transition_Hours", "mean"),
            Median_Hours=("Transition_Hours", "median"),
            Minimum_Hours=("Transition_Hours", "min"),
            Maximum_Hours=("Transition_Hours", "max"),
        )
    )

    # Round time values for readability
    time_columns = [
        "Average_Hours",
        "Median_Hours",
        "Minimum_Hours",
        "Maximum_Hours",
    ]

    analysis[time_columns] = analysis[time_columns].round(2)

    # Sort by most frequent transitions
    analysis = analysis.sort_values(
        "Transition_Count",
        ascending=False
    )

    # Save result
    analysis.to_csv(OUTPUT, index=False)

    # Display summary
    print("CareFlow Week 3 - Transition Time Analysis")
    print("-------------------------------------------")
    print(f"Input events: {len(df):,}")
    print(f"Transition records: {len(transitions):,}")
    print(f"Unique transitions: {len(analysis):,}")
    print(f"Output written to: {OUTPUT}")

    print("\nTop 10 transitions:")
    print(analysis.head(10).to_string(index=False))


if __name__ == "__main__":
    main()