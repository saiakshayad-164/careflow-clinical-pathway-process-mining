{{ config(materialized='table') }}

with case_paths as (
    select
        case_id,
        string_agg(activity_name, ' -> ' order by event_timestamp, activity_name) as observed_pathway,
        count(*) as event_count,
        min(event_timestamp) as first_event_timestamp,
        max(event_timestamp) as last_event_timestamp,
        timestamp_diff(max(event_timestamp), min(event_timestamp), minute) as case_duration_minutes,
        countif(activity_name = 'Return ER') as return_er_events
    from {{ ref('stg_event_log') }}
    group by case_id
)
select
    *,
    return_er_events > 0 as has_return_er
from case_paths
