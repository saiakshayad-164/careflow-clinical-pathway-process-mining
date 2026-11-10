{{ config(materialized='view') }}

with source_events as (
    select
        cast(Case_ID as string) as case_id,
        trim(cast(Activity_Name as string)) as activity_name,
        safe_cast(Timestamp as timestamp) as event_timestamp,
        cast(Resource as string) as resource,
        cast(Age_Group as string) as age_group
    from {{ source('careflow_raw', 'raw_event_log') }}
),
valid_events as (
    select *
    from source_events
    where case_id is not null
      and case_id != ''
      and activity_name is not null
      and activity_name != ''
      and event_timestamp is not null
),
deduplicated as (
    select *,
        row_number() over (
            partition by case_id, activity_name, event_timestamp, resource, age_group
            order by event_timestamp
        ) as duplicate_rank
    from valid_events
)
select
    case_id,
    activity_name,
    event_timestamp,
    resource,
    age_group
from deduplicated
where duplicate_rank = 1
