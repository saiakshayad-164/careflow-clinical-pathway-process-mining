import os
import pandas as pd
import pm4py
from google.cloud import bigquery

# 1. Fetch Cleaned Event Log from BigQuery
client = bigquery.Client(project="careflow-analytics-production")
query = """
    SELECT case_id, activity_name, event_timestamp
    FROM `careflow-analytics-production.dbt_adarsh.event_log`
    ORDER BY case_id, event_timestamp
"""
df = client.query(query).to_dataframe()

# Convert timestamp column
df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

# 2. Format for PM4Py
df = pm4py.format_dataframe(
    df, 
    case_id='case_id', 
    activity_key='activity_name', 
    timestamp_key='event_timestamp'
)

# 3. Week 3 Task: Discover Performance Map (Bottlenecks & Transition Durations)
performance_map = pm4py.discover_performance_dfg(df)

print("--- Week 3 Bottleneck & Transition Summary ---")
print("\nTransition Delays (Performance Analysis):")

# FIXED LOOP: Extracting 'mean' duration from the performance dictionary
for pair, metrics in performance_map[0].items():
    source_node, target_node = pair
    
    # Check if metrics is a dictionary or direct float value
    if isinstance(metrics, dict):
        avg_seconds = metrics.get('mean', 0)
    else:
        avg_seconds = metrics

    avg_minutes = round(avg_seconds / 60, 2)
    print(f"{source_node}  --->  {target_node} | Mean Duration: {avg_minutes} mins")

# 4. Save Performance Process Map Visualization
dfg, start_activities, end_activities = pm4py.discover_dfg(df)
pm4py.save_vis_performance_dfg(
    dfg, 
    start_activities, 
    end_activities, 
    "careflow_performance_bottlenecks.png"
)
print("\nPerformance Bottleneck Map saved as 'careflow_performance_bottlenecks.png'.")