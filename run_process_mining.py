import os
import pm4py
from google.cloud import bigquery
from google.auth import default

# 1. Initialize BigQuery Client
credentials, project_id = default()
client = bigquery.Client(credentials=credentials, project=project_id)

# 2. Query Cleaned Event Logs from dbt Model
query = """
    SELECT 
        case_id,
        activity_name,
        event_timestamp,
        resource,
        age_group
    FROM 
        `careflow-analytics-production.dbt_adarsh.event_log`
    ORDER BY 
        case_id, event_timestamp ASC
"""

print("Fetching event logs from BigQuery...")
df = client.query(query).to_dataframe()

# 3. Format DataFrame for PM4Py
df_formatted = pm4py.format_dataframe(
    df,
    case_id='case_id',
    activity_key='activity_name',
    timestamp_key='event_timestamp'
)

# 4. Discover Process Tree & Petri Net
print("Discovering process model...")
process_tree = pm4py.discover_process_tree_inductive(df_formatted)
net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

# 5. Save Process Map
pm4py.save_vis_petri_net(net, initial_marking, final_marking, file_path="careflow_process_map.png")
print("Success! Process map saved as 'careflow_process_map.png'.")

# 6. Trace Variant Analysis
print("\n--- Trace Variant Analysis ---")
variants = pm4py.get_variants(df_formatted)
for variant, count in list(variants.items())[:5]:  # Top 5 variants
    print(f"Path: {variant} | Occurrences: {count}")