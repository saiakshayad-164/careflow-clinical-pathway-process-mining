{{ config(materialized='table') }}

with sequenced as (
    select
        case_id,
        activity_name,
        event_timestamp,
        lead(activity_name) over (
            partition by case_id order by event_timestamp, activity_name
        ) as next_activity,
        lead(event_timestamp) over (
            partition by case_id order by event_timestamp, activity_name
        ) as next_timestamp
    from {{ ref('stg_event_log') }}
)
select
    activity_name,
    next_activity,
    count(*) as transition_count,
    avg(timestamp_diff(next_timestamp, event_timestamp, second)) / 60.0 as mean_gap_minutes,
    approx_quantiles(timestamp_diff(next_timestamp, event_timestamp, second) / 60.0, 100)[offset(50)] as median_gap_minutes,
    max(timestamp_diff(next_timestamp, event_timestamp, second)) / 60.0 as max_gap_minutes
from sequenced
where next_activity is not null
  and next_timestamp >= event_timestamp
group by activity_name, next_activity
