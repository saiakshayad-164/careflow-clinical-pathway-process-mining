from google.cloud import bigquery
from google.auth import default
import pandas as pd
import pm4py

# 1. BigQuery Client Setup
credentials, project_id = default()
client = bigquery.Client(credentials=credentials, project=project_id)

# 2. Query event log data with actual sample columns
query = """
    SELECT 
        Case_ID,
        Activity_Name,
        Timestamp,
        Resource,
        Age_Group
    FROM 
        `your-gcp-project-id.careflow_raw.raw_ehr_logs`
    ORDER BY 
        Case_ID, Timestamp ASC
"""

print("Fetching event logs from BigQuery...")
df = client.query(query).to_dataframe()

# 3. Format DataFrame for PM4Py
df_formatted = pm4py.format_dataframe(
    df, 
    case_id_key='Case_ID', 
    activity_key='Activity_Name', 
    timestamp_key='Timestamp'
)

# 4. Discover Process Tree
print("Discovering process model...")
process_tree = pm4py.discover_process_tree_inductive(df_formatted)

# 5. Save Process Map
net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)
pm4py.save_vis_petri_net(net, initial_marking, final_marking, file_path="careflow_process_map.png")

print("Success! Process map saved as 'careflow_process_map.png'.")