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

### 📊 1. Process Analytics & Conformance Setup (PM4Py)
* Developed and executed Python analytics scripts (`run_process_mining.py` & `conformance_checking.py`) utilizing **PM4Py** to evaluate patient treatment flow.
* Analyzed event logs to identify critical operational bottlenecks across patient care pathways, specifically focusing on high-volume clinical stages like `Leucocytes`, `CRP`, and `ER Registration`.

### 📈 2. Executive BI Dashboard Development (Google Looker Studio)
* Successfully integrated Google Looker Studio directly with the production dataset on **BigQuery** (`careflow-analytics-production.dbt_adarsh.event_log`).
* Configured core visual elements and dynamic features:
  * **KPI Scorecards:** Total unique patient volume (`case_id` - Count Distinct) and total clinical events (`Record Count`).
  * **Volume Bar Chart:** Visualized high-frequency activity stages (`activity_name`) to highlight operational delay areas.
  * **Time Series Timeline:** Monitored overall patient volume and treatment trends over time (`event_timestamp`).
  * **Interactive Controls:** Integrated dynamic Date Range selectors and Activity Dropdown filters for customizable executive reporting.
* **Live Dashboard URL:** [CareFlow Executive Performance Dashboard](https://datastudio.google.com/reporting/a7fe8627-e495-4cfe-8761-fcd4595ea37f)

### 🌿 3. Documentation & Branch Synchronization
* Maintained clean Markdown documentation in `README.md` summarizing weekly deliverables, process mining insights, and dashboard links.
* Synchronized all codebase updates, scripts, and project assets to the remote Git repository under the dedicated working branch `SIVASAKTHI-S`.
###  4. Conformance Checking & ROI Dashboard Polish
**BigQuery Conformance Integration**
* Developed `conformance_checking.py` script with direct Google BigQuery querying to bypass local CSV file dependencies.
* Formatted raw event logs into PM4Py DataFrames and discovered target Petri Net process models using Inductive Mining.
## 📂 Codebase & Folder Structure

```text
careflow/
│
├── python/
│   ├── run_process_mining.py     # Main PM4Py discovery & graph rendering engine
│   ├── bottleneck_analyzer.py    # Transition time calculation script
│   └── requirements.txt          # Python dependencies (pm4py, pandas, google-cloud-bigquery)
│
└── CONTRIBUTIONS_PM4PY.md        # Individual contribution documentation