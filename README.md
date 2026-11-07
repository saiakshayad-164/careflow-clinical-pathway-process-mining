# 🔍 Process Mining & PM4Py Analytics (My Contribution)

> **Role:** Process Mining & Python Analytics Developer  
> **Module Focus:** Event log ingestion, algorithmic process discovery using `PM4Py`, bottleneck calculations, and patient flow visualization.

---

## 📌 Technical Summary & Key Responsibilities

As part of the **CareFlow** clinical pathway project, I engineered the **Process Analytics Engine** responsible for translating chronological patient event streams into actionable visual flow models.

### 1. Ingestion & Event Log Normalization
* Connected Python runtime to **Google BigQuery** using `google-cloud-bigquery` to fetch cleaned and transformed data logs (`Case_ID`, `Activity_Name`, `Timestamp`).
* Formatted dynamic relational DataFrames into strict `PM4Py` event log structures adhering to standard process mining semantics.

### 2. Process Discovery & Spaghetti Diagram Generation
* Applied **Heuristics Miner** and **Inductive Miner** algorithms via `PM4Py` to discover the actual *"As-Is"* hospital process.
* Rendered dynamic **Directed Graphs** and **Petri Nets** to highlight non-linear patient flows and uncover hidden loop-backs (e.g., *Triage → X-Ray → Triage* due to missing paperwork).

### 3. Dwell Time & Bottleneck Analytics
* Engineered custom logic to compute average transition durations between sequential clinical nodes (e.g., time elapsed between *Triage completion* and *Doctor consultation*).
* Quantified operational delays to isolate high-friction activities impacting total Emergency Room (ER) wait times.

---

## 📂 Codebase & Folder Structure


## 📊 Week 3: Process Analytics & Executive BI Dashboard Integration

### 🎯 Key Deliverables & Contributions
- **PM4Py Bottleneck Analytics:** Analyzed CareFlow healthcare event logs to identify critical operational bottlenecks across patient treatment pathways (e.g., high-volume clinical stages like `Leucocytes`, `CRP`, and `ER Triage`).
- **Google Looker Studio Integration:** Built and configured a live native Business Intelligence (BI) Executive Dashboard connected to BigQuery (`careflow-analytics-production.dbt_adarsh.event_log`).
- **Executive Metrics & Visualizations:**
  - **KPI Scorecards:** Total unique patient volume (`case_id` - Count Distinct) and total clinical events (`Record Count`).
  - **Volume Bar Chart:** Visualized high-frequency activity stages (`activity_name`) to isolate operational bottlenecks.
  - **Time Series Timeline:** Tracked overall patient flow and clinical event trends over time (`event_timestamp`).
  - **Interactive Controls:** Integrated dynamic Date Range selectors and Activity Dropdown filters for interactive executive reporting.

---

### 🔗 Live Interactive Dashboard
- **Looker Studio Dashboard Link:** [CareFlow Executive Performance Dashboard](https://datastudio.google.com/reporting/a7fe8627-e495-4cfe-8761-fcd4595ea37f)

---
```text
careflow/
│
├── python/
│   ├── run_process_mining.py     # Main PM4Py discovery & graph rendering engine
│   ├── bottleneck_analyzer.py    # Transition time calculation script
│   └── requirements.txt          # Python dependencies (pm4py, pandas, google-cloud-bigquery)
│
└── CONTRIBUTIONS_PM4PY.md        # Individual contribution documentation