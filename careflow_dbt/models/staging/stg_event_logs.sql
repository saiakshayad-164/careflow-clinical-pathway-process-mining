WITH source AS (
    SELECT * FROM {{ source('careflow_raw', 'raw_ehr_logs') }}
)
SELECT
    CAST(Case_ID AS STRING) AS Case_ID,
    CAST(Activity_Name AS STRING) AS Activity_Name,
    CAST(Timestamp AS TIMESTAMP) AS Timestamp,
    CAST(Resource AS STRING) AS Resource,
    CAST(Age_Group AS STRING) AS Age_Group
FROM source