import pandas as pd
from google.cloud import bigquery

def analyze_bottlenecks():
    print("🚀 Fetching event logs from BigQuery for Bottleneck Analysis...")
    client = bigquery.Client()
    
    query = """
        SELECT 
            case_id, 
            activity_name, 
            event_timestamp,
            resource,
            age_group
        FROM `careflow-analytics-production.dbt_adarsh.event_log`
        ORDER BY case_id, event_timestamp ASC
    """
    
    df = client.query(query).to_dataframe()
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
    
    df['prev_activity'] = df.groupby('case_id')['activity_name'].shift(1)
    df['prev_timestamp'] = df.groupby('case_id')['event_timestamp'].shift(1)
    df['transition_duration_mins'] = (df['event_timestamp'] - df['prev_timestamp']).dt.total_seconds() / 60.0

    transitions = df.dropna(subset=['prev_activity'])
    bottleneck_summary = transitions.groupby(['prev_activity', 'activity_name'])['transition_duration_mins'].agg(['count', 'mean', 'max']).reset_index()
    bottleneck_summary = bottleneck_summary.sort_values(by='mean', ascending=False)

    print("\n" + "="*60)
    print("⏳ CLINICAL PATHWAY BOTTLENECK ANALYSIS SUMMARY")
    print("="*60)
    for index, row in bottleneck_summary.head(5).iterrows():
        print(f"Transition: {row['prev_activity']} ➔ {row['activity_name']}")
        print(f"  - Total Cases : {row['count']}")
        print(f"  - Avg Delay   : {row['mean']:.1f} minutes")
        print(f"  - Max Delay   : {row['max']:.1f} minutes")
        print("-" * 60)

if __name__ == "__main__":
    analyze_bottlenecks()