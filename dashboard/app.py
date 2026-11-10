from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="CareFlow | Clinical Pathway Analytics", page_icon="🏥", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "event_log_validated.csv"
REQUIRED = {"Case_ID", "Activity_Name", "Timestamp"}


@st.cache_data(show_spinner=False)
def load_data(source: str, uploaded_bytes: bytes | None = None) -> pd.DataFrame:
    if uploaded_bytes is not None:
        from io import BytesIO
        df = pd.read_csv(BytesIO(uploaded_bytes))
    else:
        df = pd.read_csv(source)
    missing = REQUIRED.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    df["Case_ID"] = df["Case_ID"].astype("string").str.strip()
    df["Activity_Name"] = df["Activity_Name"].astype("string").str.strip()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["Case_ID", "Activity_Name", "Timestamp"])
    return df.sort_values(["Case_ID", "Timestamp", "Activity_Name"]).reset_index(drop=True)


st.title("CareFlow")
st.caption("Clinical pathway process analytics | Event-log exploration and bottleneck monitoring")

with st.sidebar:
    st.header("Data and filters")
    uploaded = st.file_uploader("Upload event-log CSV (optional)", type=["csv"])
    if uploaded is not None:
        raw = uploaded.getvalue()
        data = load_data("uploaded", raw)
        st.caption("Using uploaded CSV")
    elif DEFAULT_DATA.exists():
        data = load_data(str(DEFAULT_DATA))
        st.caption("Using data/event_log_validated.csv")
    else:
        st.error("Validated dataset not found. Place event_log_validated.csv in the repository data/ folder or upload it.")
        st.stop()

    min_date = data["Timestamp"].min().date()
    max_date = data["Timestamp"].max().date()
    date_range = st.date_input("Event date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    activities = sorted(data["Activity_Name"].dropna().unique().tolist())
    selected_activities = st.multiselect("Activities", activities, default=activities)
    resources = sorted(data["Resource"].dropna().astype(str).unique().tolist()) if "Resource" in data else []
    selected_resources = st.multiselect("Resources", resources, default=resources) if resources else []

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = data[
    data["Timestamp"].dt.date.between(start_date, end_date)
    & data["Activity_Name"].isin(selected_activities)
].copy()
if selected_resources and "Resource" in filtered:
    filtered = filtered[filtered["Resource"].astype(str).isin(selected_resources)]

if filtered.empty:
    st.warning("No events match the selected filters.")
    st.stop()

filtered = filtered.sort_values(["Case_ID", "Timestamp", "Activity_Name"])
filtered["Next_Activity"] = filtered.groupby("Case_ID")["Activity_Name"].shift(-1)
filtered["Next_Timestamp"] = filtered.groupby("Case_ID")["Timestamp"].shift(-1)
filtered["Gap_Minutes"] = (filtered["Next_Timestamp"] - filtered["Timestamp"]).dt.total_seconds() / 60
transitions = filtered.dropna(subset=["Next_Activity", "Gap_Minutes"]).copy()
transitions = transitions[transitions["Gap_Minutes"] >= 0]

case_count = filtered["Case_ID"].nunique()
event_count = len(filtered)
activity_count = filtered["Activity_Name"].nunique()
avg_gap = transitions["Gap_Minutes"].mean() if not transitions.empty else 0
median_gap = transitions["Gap_Minutes"].median() if not transitions.empty else 0
return_cases = filtered.loc[filtered["Activity_Name"].eq("Return ER"), "Case_ID"].nunique()
return_rate = return_cases / case_count * 100 if case_count else 0
repeat_events = filtered.groupby("Case_ID")["Activity_Name"].apply(lambda s: s.duplicated().any()).sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Patient visits", f"{case_count:,}")
c2.metric("Events", f"{event_count:,}")
c3.metric("Activities", f"{activity_count:,}")
c4.metric("Mean inter-event gap", f"{avg_gap:,.1f} min")
c5.metric("Return ER cases", f"{return_cases:,}", f"{return_rate:.1f}% of filtered cases")

st.caption("Inter-event gap is the elapsed time between consecutive recorded events within a case. It is not necessarily a staffed queue/wait time.")

left, right = st.columns(2)
with left:
    activity_counts = filtered["Activity_Name"].value_counts().rename_axis("Activity").reset_index(name="Events")
    fig = px.bar(activity_counts.sort_values("Events"), x="Events", y="Activity", orientation="h",
                 title="Event volume by activity", text="Events")
    fig.update_layout(yaxis_title="", xaxis_title="Events")
    st.plotly_chart(fig, use_container_width=True)
with right:
    if not transitions.empty:
        transition_summary = (transitions.groupby(["Activity_Name", "Next_Activity"], as_index=False)
                              .agg(Transitions=("Gap_Minutes", "size"),
                                   Median_Gap_Minutes=("Gap_Minutes", "median"),
                                   Mean_Gap_Minutes=("Gap_Minutes", "mean")))
        transition_summary["Transition"] = transition_summary["Activity_Name"] + " → " + transition_summary["Next_Activity"]
        top_gaps = transition_summary.sort_values("Median_Gap_Minutes", ascending=False).head(12)
        fig = px.bar(top_gaps.sort_values("Median_Gap_Minutes"), x="Median_Gap_Minutes", y="Transition",
                     orientation="h", color="Transitions", title="Transitions with highest median inter-event gap",
                     hover_data=["Transitions", "Mean_Gap_Minutes"])
        fig.update_layout(yaxis_title="", xaxis_title="Median gap (minutes)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough consecutive events to calculate transitions.")

st.subheader("Pathway patterns")
case_paths = (filtered.sort_values(["Case_ID", "Timestamp", "Activity_Name"])
              .groupby("Case_ID")["Activity_Name"].agg(lambda x: " → ".join(x.astype(str)))
              .value_counts().head(10).rename_axis("Observed pathway").reset_index(name="Visits"))
st.dataframe(case_paths, use_container_width=True, hide_index=True)

if not transitions.empty:
    st.subheader("Transition detail")
    detail = (transitions.groupby(["Activity_Name", "Next_Activity"], as_index=False)
              .agg(Transition_Count=("Gap_Minutes", "size"),
                   Mean_Gap_Minutes=("Gap_Minutes", "mean"),
                   Median_Gap_Minutes=("Gap_Minutes", "median"),
                   Maximum_Gap_Minutes=("Gap_Minutes", "max")))
    detail = detail.sort_values("Median_Gap_Minutes", ascending=False)
    st.dataframe(detail, use_container_width=True, hide_index=True)

st.subheader("Case-level drill-down")
case_options = sorted(filtered["Case_ID"].dropna().astype(str).unique().tolist())
selected_case = st.selectbox("Choose a visit ID", case_options)
case_view = filtered[filtered["Case_ID"].astype(str).eq(selected_case)].sort_values("Timestamp")
display_cols = [c for c in ["Timestamp", "Activity_Name", "Resource", "Age_Group"] if c in case_view.columns]
st.dataframe(case_view[display_cols], use_container_width=True, hide_index=True)

st.download_button("Download filtered event log", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="careflow_filtered_event_log.csv", mime="text/csv")
st.caption(f"Loaded {len(data):,} valid events before filters. Dashboard results are descriptive and should be interpreted with the dataset's provenance and limitations.")
