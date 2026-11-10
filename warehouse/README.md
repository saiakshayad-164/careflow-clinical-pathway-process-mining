# BigQuery warehouse setup

## 1. Create the raw table

Edit `schema.sql` and replace `YOUR_GCP_PROJECT` with your Google Cloud project ID. Then run it in BigQuery.

## 2. Load the validated CSV

From the repository root, after installing and authenticating the Google Cloud CLI:

```bash
gcloud auth application-default login
bq load --autodetect=false --source_format=CSV --skip_leading_rows=1 YOUR_GCP_PROJECT:careflow.raw_event_log data/event_log_validated.csv Case_ID:STRING,Activity_Name:STRING,Timestamp:STRING,Resource:STRING,Age_Group:STRING
```

If the timestamp column has already been loaded as TIMESTAMP, update the staging model's SAFE_CAST accordingly. Keep credentials, service-account JSON files, and local environment files out of Git.

## 3. Configure dbt

Install dependencies:

```bash
python -m pip install -r dbt_project/requirements.txt
```

Create a local `~/.dbt/profiles.yml` (do not commit it):

```yaml
careflow_bigquery:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: YOUR_GCP_PROJECT
      dataset: careflow_dbt
      threads: 4
      location: US
      priority: interactive
      job_execution_timeout_seconds: 300
      job_retries: 1
```

Run:

```bash
cd dbt_project
dbt debug --vars '{gcp_project: YOUR_GCP_PROJECT, bq_dataset: careflow}'
dbt run --vars '{gcp_project: YOUR_GCP_PROJECT, bq_dataset: careflow}'
dbt test --vars '{gcp_project: YOUR_GCP_PROJECT, bq_dataset: careflow}'
```

Set `location` to the actual BigQuery dataset region. The dbt target dataset is `careflow_dbt`; the source dataset defaults to `careflow`.
