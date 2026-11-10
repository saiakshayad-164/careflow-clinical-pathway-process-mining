# 🔍 CareFlow: Process Mining & Executive BI Dashboard (Weeks 1 - 4)

> **Role:** Process Mining & Python Analytics Developer  
> **Working Branch:** `SIVASAKTHI-S`  
> **Module Focus:** BigQuery ingestion, PM4Py process discovery, conformance checking, bottleneck analytics, dynamic Looker Studio BI reporting, and executive ROI tracking.

---

## 📌 Technical Summary & Key Responsibilities

As part of the **CareFlow** clinical pathway project, I engineered the **Process Analytics Engine** and **Executive BI Dashboard** responsible for translating raw patient event streams into actionable visual flow models, process conformance metrics, and interactive executive insights across Weeks 1 to 4.

---

## 📅 Weekly Milestones & Deliverables

### 🔹 Week 1: Ingestion & Environment Setup
- Set up local Python virtual environment (`venv`) and managed package dependencies (`pandas`, `pm4py`, `google-cloud-bigquery`, `db-dtypes`).
- Established direct database connection to **Google BigQuery** dataset (`careflow-analytics-production.dbt_adarsh.event_log`).
- Formatted raw event streams (`case_id`, `activity_name`, `event_timestamp`) into strict `PM4Py` event log structures.

### 🔹 Week 2: Process Mining & Algorithm Execution
- Developed and executed `run_process_mining.py` leveraging **PM4Py** algorithms (**Inductive Miner** and **Heuristics Miner**).
- Rendered visual **Directed Graphs** and **Petri Nets** to map the *"As-Is"* hospital process.
- Identified non-linear clinical loop-backs (e.g., *Triage → X-Ray → Triage* due to missing paperwork).

### 🔹 Week 3: Bottleneck Analysis & BI Dashboard
- Engineered custom transition time logic (`bottleneck_analyzer.py`) to quantify operational delays between sequential clinical nodes.
- Integrated **Google Looker Studio** directly with BigQuery production tables.
- Built initial baseline charts: Time Series Timeline (`event_timestamp`), Record Count metrics, and Volume Bar Charts (`activity_name`).

### 🔹 Week 4: Conformance Checking & Dashboard Polish
- **Conformance Checking Engine:** Developed `conformance_checking.py` with direct BigQuery integration to bypass local CSV dependencies and measure alignment with clinical guidelines.
- **Dynamic Looker Studio Enhancements:**
  - Added multi-level **Dropdown Filters** for `age_group` (patient cohort) and `resource` (Doctor / Staff ID).
  - Configured **Dynamic Hierarchy Drill-down** on the volume bar chart (`activity_name` → `resource`).
- **Executive ROI Scorecards:** Integrated business impact metrics:
  - *Wait Time Reduction:* **Average Triage Wait Time Reduced by 20 mins**
  - *ROI Savings:* **Estimated Annual Cost Savings: ₹15-20 Lakhs per 1,000 cases**

---

## 🔗 Live Public Dashboard Link
- **CareFlow Executive Performance Dashboard:** [View Live Dashboard](https://datastudio.google.com/reporting/a7fe8627-e495-4cfe-8761-fcd4595ea37f)  
- **Direct Link:** `https://datastudio.google.com/reporting/a7fe8627-e495-4cfe-8761-fcd4595ea37f`

---

## 📂 Codebase & Folder Structure

```text
careflow/
│
├── python/
│   ├── run_process_mining.py     # PM4Py discovery & graph rendering engine
│   ├── conformance_checking.py   # BigQuery-integrated conformance checking script
│   ├── bottleneck_analyzer.py    # Clinical transition time calculation script
│   └── requirements.txt          # Python dependencies (pm4py, pandas, google-cloud-bigquery, db-dtypes)
│
├── README.md                     # Main project documentation & weekly deliverables
└── CONTRIBUTIONS_PM4PY.md        # Individual process mining developer contribution details