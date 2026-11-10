import pandas as pd
import pm4py
from google.cloud import bigquery

try:
    print("Connecting to BigQuery and fetching event logs...")
    
    client = bigquery.Client()
    query = """
        SELECT case_id, activity_name, event_timestamp
        FROM `careflow-analytics-production.dbt_adarsh.event_log`
    """
    
    df = client.query(query).to_dataframe()
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

    log = pm4py.format_dataframe(
        df, 
        case_id='case_id', 
        activity_key='activity_name', 
        timestamp_key='event_timestamp'
    )

    print(f"Successfully loaded {len(df)} events from BigQuery.")

    # Target Process Model (Petri Net)
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)

    # Token-Based Replay Conformance
    tbr_results = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
    print("\n--- Token-based Replay Results ---")
    print(f"Total Traces Evaluated: {len(tbr_results)}")
    
    # Alignments Calculation
    alignments = pm4py.conformance_diagnostics_alignments(log, net, initial_marking, final_marking)
    print("\n--- Alignments Conformance Sample ---")
    print(f"First Trace Alignment: {alignments[0] if alignments else 'N/A'}")

except Exception as e:
    print(f"Error running conformance check with BigQuery: {e}")