-- Run in the target BigQuery project after creating the dataset.
-- Replace YOUR_GCP_PROJECT and confirm dataset/region before execution.
CREATE SCHEMA IF NOT EXISTS `YOUR_GCP_PROJECT.careflow`;

CREATE TABLE IF NOT EXISTS `YOUR_GCP_PROJECT.careflow.raw_event_log` (
  Case_ID STRING,
  Activity_Name STRING,
  Timestamp STRING,
  Resource STRING,
  Age_Group STRING
);
