from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="CareFlow | Pathway Studio",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "event_log_validated.csv"
REQUIRED = {"Case_ID", "Activity_Name", "Timestamp"}

THEMES = {
    "Light": {
        "bg": "#F5F7FB", "panel": "#FFFFFF", "text": "#172033",
        "muted": "#667085", "line": "#E5EAF2", "accent": "#3157D5",
        "soft": "#EAF0FF", "plot": "plotly_white",
    },
    "Dark": {
        "bg": "#101827", "panel": "#182235", "text": "#F1F5FC",
        "muted": "#A8B4C7", "line": "#2A3850", "accent": "#8EA9FF",
        "soft": "#263653", "plot": "plotly_dark",
    },
}


@st.cache_data(show_spinner=False)
def load_data(source: str, uploaded_bytes: bytes | None = None) -> pd.DataFrame:
    if uploaded_bytes is not None:
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


def style_plot(fig, theme):
    fig.update_layout(
        template=theme["plot"],
        paper_bgcolor=theme["panel"],
        plot_bgcolor=theme["panel"],
        font=dict(color=theme["text"], family="Inter, sans-serif"),
        title_font=dict(size=16),
        margin=dict(l=8, r=8, t=48, b=8),
        legend_title_text="",
    )
    return fig


def metric_card(label, value, note, theme):
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    .stApp {background: var(--cf-bg);}
    section[data-testid="stSidebar"] {border-right: 1px solid var(--cf-line);}
    .block-container {padding-top: 1.8rem; padding-bottom: 2.5rem; max-width: 1440px;}
    .hero {padding: 1.35rem 1.5rem; border: 1px solid var(--cf-line);
           border-radius: 18px; background: var(--cf-panel); margin-bottom: 1.1rem;}
    .eyebrow {font-size: .72rem; letter-spacing: .13em; text-transform: uppercase;
              color: var(--cf-accent); font-weight: 750; margin-bottom: .35rem;}
    .hero h1 {font-size: 2rem; line-height: 1.15; margin: 0; color: var(--cf-text);}
    .hero p {color: var(--cf-muted); margin: .45rem 0 0 0; font-size: .95rem;}
    .metric-card {background: var(--cf-panel); border: 1px solid var(--cf-line);
                  border-radius: 15px; padding: 1rem 1.05rem; min-height: 112px;}
    .metric-label {font-size: .78rem; color: var(--cf-muted); font-weight: 650;}
    .metric-value {font-size: 1.75rem; color: var(--cf-text); font-weight: 750;
                   letter-spacing: -.04em; margin: .25rem 0;}
    .metric-note {font-size: .72rem; color: var(--cf-muted);}
    .section-head {font-size: 1.1rem; font-weight: 720; color: var(--cf-text);
                   margin: .4rem 0 .2rem 0;}
    .subtle {color: var(--cf-muted); font-size: .83rem;}
    .journey-chip {display:inline-block; padding:.45rem .72rem; margin:.22rem .18rem .22rem 0;
                   border-radius:9px; background:var(--cf-soft); color:var(--cf-text);
                   border:1px solid var(--cf-line); font-size:.82rem;}
    div[data-testid="stTabs"] button {font-weight:650;}
    div[data-testid="stDataFrame"] {border:1px solid var(--cf-line); border-radius:12px;}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### CAREFLOW")
    st.caption("Clinical pathway intelligence")
    theme_name = st.radio("Appearance", ["Light", "Dark"], horizontal=True, index=0)
    theme = THEMES[theme_name]
    st.divider()
    st.markdown("#### Your dataset")
    uploaded = st.file_uploader("Upload event log", type=["csv"])
    if uploaded is not None:
        data = load_data("uploaded", uploaded.getvalue())
        st.caption("Source: uploaded CSV")
    elif DEFAULT_DATA.exists():
        data = load_data(str(DEFAULT_DATA))
        st.caption("Source: validated project dataset")
    else:
        st.error("Dataset not found. Upload a CSV to continue.")
        st.stop()

    min_date = data["Timestamp"].min().date()
    max_date = data["Timestamp"].max().date()
    st.markdown("#### Explore")
    date_range = st.date_input(
        "Event date range", value=(min_date, max_date),
        min_value=min_date, max_value=max_date,
    )
    activities = sorted(data["Activity_Name"].dropna().unique().tolist())
    selected_activities = st.multiselect("Activities", activities, default=activities)
    resources = sorted(data["Resource"].dropna().astype(str).unique().tolist()) if "Resource" in data else []
    selected_resources = st.multiselect("Resources", resources, default=resources) if resources else []
    st.divider()
    st.caption("Filters affect the event view. Journey order and transition gaps are calculated from the complete date-filtered sequence.")

st.markdown(
    f"""
    <style>
    :root {{
      --cf-bg:{theme['bg']}; --cf-panel:{theme['panel']}; --cf-text:{theme['text']};
      --cf-muted:{theme['muted']}; --cf-line:{theme['line']};
      --cf-accent:{theme['accent']}; --cf-soft:{theme['soft']};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

date_data = data[data["Timestamp"].dt.date.between(start_date, end_date)].copy()
filtered = date_data[date_data["Activity_Name"].isin(selected_activities)].copy()
if selected_resources and "Resource" in filtered:
    filtered = filtered[filtered["Resource"].astype(str).isin(selected_resources)]

if filtered.empty or date_data.empty:
    st.warning("No events match the current filters. Widen the date range or select more activities.")
    st.stop()

# Preserve real event adjacency: activity/resource filters must not create fake transitions.
sequence = date_data.sort_values(["Case_ID", "Timestamp", "Activity_Name"]).copy()
sequence["Next_Activity"] = sequence.groupby("Case_ID")["Activity_Name"].shift(-1)
sequence["Next_Timestamp"] = sequence.groupby("Case_ID")["Timestamp"].shift(-1)
sequence["Gap_Minutes"] = (
    sequence["Next_Timestamp"] - sequence["Timestamp"]
).dt.total_seconds() / 60
transitions = sequence.dropna(subset=["Next_Activity", "Gap_Minutes"]).copy()
transitions = transitions[transitions["Gap_Minutes"] >= 0]

case_paths = (
    sequence.groupby("Case_ID")["Activity_Name"]
    .agg(lambda s: " → ".join(s.astype(str)))
    .rename("Pathway")
    .reset_index()
)
variant_counts = case_paths["Pathway"].value_counts().rename_axis("Pathway").reset_index(name="Visits")
variant_counts["Share"] = variant_counts["Visits"] / max(len(case_paths), 1) * 100

case_flags = sequence.groupby("Case_ID").agg(
    event_count=("Activity_Name", "size"),
    unique_activities=("Activity_Name", "nunique"),
    first_event=("Timestamp", "min"),
    last_event=("Timestamp", "max"),
)
repeated = sequence.groupby("Case_ID")["Activity_Name"].apply(lambda s: s.duplicated().any())
case_flags["has_repeat"] = repeated
return_ids = set(sequence.loc[sequence["Activity_Name"].eq("Return ER"), "Case_ID"].astype(str))
case_flags["has_return_er"] = case_flags.index.astype(str).isin(return_ids)
case_flags["duration_hours"] = (
    case_flags["last_event"] - case_flags["first_event"]
).dt.total_seconds() / 3600

case_count = date_data["Case_ID"].nunique()
event_count = len(filtered)
activity_count = filtered["Activity_Name"].nunique()
return_cases = int(case_flags["has_return_er"].sum())
repeat_cases = int(case_flags["has_repeat"].sum())
median_gap = transitions["Gap_Minutes"].median() if not transitions.empty else 0
duplicate_rows = int(data.duplicated().sum())
invalid_timestamp_rows = int(pd.to_datetime(data["Timestamp"], errors="coerce").isna().sum())

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">CARE PATHWAY / INSIGHT WORKSPACE</div>
      <h1>See the journey, not just the numbers.</h1>
      <p>Explore how visits move through recorded activities, where pathways repeat, and which transitions deserve a closer look.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    metric_card("Patient visits", f"{case_count:,}", "Unique cases in date range", theme)
with m2:
    metric_card("Events shown", f"{event_count:,}", "After activity/resource filters", theme)
with m3:
    metric_card("Pathway types", f"{len(variant_counts):,}", "Distinct observed sequences", theme)
with m4:
    metric_card("Repeat visits / loops", f"{repeat_cases:,}", "Cases with a repeated activity", theme)
with m5:
    metric_card("Return ER cases", f"{return_cases:,}", f"{return_cases / case_count * 100:.1f}% of cases" if case_count else "No cases", theme)

st.write("")
overview_tab, pathways_tab, journey_tab, quality_tab = st.tabs(
    ["Overview", "Pathway fingerprints", "Journey explorer", "Data health"]
)

with overview_tab:
    left, right = st.columns([1.05, 1])
    with left:
        st.markdown('<div class="section-head">Activity footprint</div>', unsafe_allow_html=True)
        counts = filtered["Activity_Name"].value_counts().rename_axis("Activity").reset_index(name="Events")
        fig = px.bar(
            counts.sort_values("Events"), x="Events", y="Activity", orientation="h",
            text="Events", color_discrete_sequence=[theme["accent"]],
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(yaxis_title="", xaxis_title="Recorded events", showlegend=False)
        st.plotly_chart(style_plot(fig, theme), use_container_width=True)
    with right:
        st.markdown('<div class="section-head">Transitions to inspect</div>', unsafe_allow_html=True)
        st.caption("Ranked by median elapsed time between consecutive recorded events.")
        if not transitions.empty:
            trans_summary = (
                transitions.groupby(["Activity_Name", "Next_Activity"], as_index=False)
                .agg(
                    Occurrences=("Gap_Minutes", "size"),
                    Median_Gap_Min=("Gap_Minutes", "median"),
                    Mean_Gap_Min=("Gap_Minutes", "mean"),
                )
                .sort_values("Median_Gap_Min", ascending=False)
                .head(8)
            )
            trans_summary["Transition"] = trans_summary["Activity_Name"] + " → " + trans_summary["Next_Activity"]
            fig = px.bar(
                trans_summary.sort_values("Median_Gap_Min"),
                x="Median_Gap_Min", y="Transition", orientation="h",
                color="Occurrences", color_continuous_scale="Blues",
                hover_data=["Mean_Gap_Min"],
            )
            fig.update_layout(yaxis_title="", xaxis_title="Median inter-event gap (minutes)")
            st.plotly_chart(style_plot(fig, theme), use_container_width=True)
        else:
            st.info("No consecutive events are available for this date range.")

    st.markdown('<div class="section-head">A quick pulse</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    p1.metric("Median inter-event gap", f"{median_gap:,.1f} min")
    p2.metric("Cases with repeated activity", f"{repeat_cases:,}")
    p3.metric("Distinct pathway patterns", f"{len(variant_counts):,}")
    st.caption("Inter-event gap is elapsed time between timestamps. It is not automatically queue time, clinician waiting time, or proof of a cause.")

with pathways_tab:
    st.markdown('<div class="section-head">Pathway fingerprints</div>', unsafe_allow_html=True)
    st.caption("Each fingerprint is an observed sequence. Select one to inspect its activity trail and frequency.")
    if not variant_counts.empty:
        top_variants = variant_counts.head(12).copy()
        selected_variant = st.selectbox(
            "Choose a pathway fingerprint",
            top_variants["Pathway"].tolist(),
            format_func=lambda p: f"{int(top_variants.loc[top_variants['Pathway'].eq(p), 'Visits'].iloc[0])} visits · {p[:85]}",
        )
        selected_row = top_variants[top_variants["Pathway"].eq(selected_variant)].iloc[0]
        a, b, c = st.columns(3)
        a.metric("Visits using this path", f"{int(selected_row['Visits']):,}")
        b.metric("Share of visits", f"{selected_row['Share']:.1f}%")
        c.metric("Activities in sequence", f"{len(selected_variant.split(' → '))}")
        st.markdown("**Activity trail**")
        chips = "".join(
            f'<span class="journey-chip">{i + 1}. {activity}</span>'
            for i, activity in enumerate(selected_variant.split(" → "))
        )
        st.markdown(chips, unsafe_allow_html=True)
        st.markdown("**Most common observed patterns**")
        fig = px.bar(
            top_variants.sort_values("Visits"), x="Visits", y="Pathway",
            orientation="h", color_discrete_sequence=[theme["accent"]],
        )
        fig.update_layout(yaxis_title="", xaxis_title="Visits")
        st.plotly_chart(style_plot(fig, theme), use_container_width=True)
    else:
        st.info("No pathway patterns found.")

    st.markdown('<div class="section-head">Loopback watch</div>', unsafe_allow_html=True)
    loop_cases = case_flags[case_flags["has_repeat"] | case_flags["has_return_er"]].copy()
    loop_cases["Case_ID"] = loop_cases.index.astype(str)
    loop_cases["Pattern"] = loop_cases.apply(
        lambda r: "Return ER + repeated activity" if r["has_return_er"] and r["has_repeat"]
        else ("Return ER" if r["has_return_er"] else "Repeated activity"),
        axis=1,
    )
    st.dataframe(
        loop_cases.sort_values(["has_return_er", "event_count"], ascending=False)
        [["Case_ID", "Pattern", "event_count", "unique_activities", "duration_hours"]]
        .rename(columns={"event_count": "Events", "unique_activities": "Unique activities", "duration_hours": "Span (hours)"}),
        use_container_width=True, hide_index=True,
    )

with journey_tab:
    st.markdown('<div class="section-head">One visit, step by step</div>', unsafe_allow_html=True)
    st.caption("Choose a case to reveal its recorded activity sequence and elapsed time between events.")
    case_options = sorted(date_data["Case_ID"].dropna().astype(str).unique().tolist())
    selected_case = st.selectbox("Patient visit / Case ID", case_options, key="journey_case")
    one_case = sequence[sequence["Case_ID"].astype(str).eq(selected_case)].sort_values("Timestamp").copy()
    one_case["Gap from previous (min)"] = one_case["Timestamp"].diff().dt.total_seconds() / 60
    one_case["Step"] = range(1, len(one_case) + 1)
    first, last = one_case["Timestamp"].min(), one_case["Timestamp"].max()
    c1, c2, c3 = st.columns(3)
    c1.metric("Recorded steps", f"{len(one_case)}")
    c2.metric("Unique activities", f"{one_case['Activity_Name'].nunique()}")
    c3.metric("Recorded span", f"{(last - first).total_seconds() / 3600:.1f} hours")
    display = ["Step", "Timestamp", "Activity_Name", "Gap from previous (min)"]
    for optional in ["Resource", "Age_Group"]:
        if optional in one_case.columns:
            display.append(optional)
    st.dataframe(
        one_case[display].rename(columns={"Activity_Name": "Activity"}),
        use_container_width=True, hide_index=True,
    )
    path_text = "  →  ".join(one_case["Activity_Name"].astype(str).tolist())
    st.markdown("**Journey line**")
    st.markdown(" ".join(
        f'<span class="journey-chip">{i + 1}. {a}</span>'
        for i, a in enumerate(one_case["Activity_Name"].astype(str).tolist())
    ), unsafe_allow_html=True)
    st.download_button(
        "Export this visit",
        one_case.to_csv(index=False).encode("utf-8"),
        file_name=f"careflow_case_{selected_case}.csv",
        mime="text/csv",
    )

with quality_tab:
    st.markdown('<div class="section-head">Dataset health check</div>', unsafe_allow_html=True)
    st.caption("A quick technical check of the currently loaded source file.")
    quality = pd.DataFrame([
        {"Check": "Required columns present", "Result": "Pass", "Detail": ", ".join(sorted(REQUIRED))},
        {"Check": "Rows with missing core fields", "Result": "Pass" if not data[list(REQUIRED)].isna().any(axis=1).any() else "Review", "Detail": str(int(data[list(REQUIRED)].isna().any(axis=1).sum()))},
        {"Check": "Invalid timestamps", "Result": "Pass" if invalid_timestamp_rows == 0 else "Review", "Detail": f"{invalid_timestamp_rows:,}"},
        {"Check": "Exact duplicate rows", "Result": "Pass" if duplicate_rows == 0 else "Review", "Detail": f"{duplicate_rows:,}"},
        {"Check": "Optional Age_Group missing", "Result": "Info", "Detail": f"{int(data['Age_Group'].isna().sum()):,}" if "Age_Group" in data else "Column not supplied"},
    ])
    st.dataframe(quality, use_container_width=True, hide_index=True)
    q1, q2, q3 = st.columns(3)
    q1.metric("Loaded rows", f"{len(data):,}")
    q2.metric("Cases", f"{data['Case_ID'].nunique():,}")
    q3.metric("Timestamp range", f"{data['Timestamp'].min().date()} — {data['Timestamp'].max().date()}")
    st.download_button(
        "Download current filtered events",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="careflow_filtered_events.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    f"CareFlow Pathway Studio · {len(data):,} valid events loaded · "
    "Descriptive process analytics only. Review dataset provenance before redistribution."
)
