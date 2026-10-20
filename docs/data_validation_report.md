# CareFlow — sai_akshaya Data Validation Report

## Purpose

This report validates the cleaned CareFlow event log before the first project checkpoint.

sai_akshaya is responsible for Python/data generation and data-quality support. The team plan requires validation of Case_IDs, activities, timestamps, patient sequences, missing/invalid records, and unusual paths.

## Dataset

- Source: `data/event_log_clean.csv`
- Validated output: `data/event_log_validated.csv`
- Rows before exact-duplicate removal: 15,190
- Exact duplicate rows removed: 7
- Rows in validated event log: 15,183
- Unique patient cases: 1,049
- Unique activities: 16
- Timestamp range: 2013-11-07 07:18:29+00:00 to 2015-06-05 10:25:11+00:00

## Core validation

| Check | Result | Status |
|---|---:|---|
| Missing Case_ID | 0 | PASS |
| Missing Activity_Name | 0 | PASS |
| Invalid/missing Timestamp | 0 | PASS |
| Empty Case_ID | 0 | PASS |
| Empty Activity_Name | 0 | PASS |
| Negative timestamp ordering within a case | 0 | PASS |
| Exact duplicate event rows remaining | 0 | PASS |
| Cases with only one event | 0 | PASS |

## Sequence checks

- Cases containing repeated activities: **742**
- Cases containing consecutive repeated activities: **311**
- Equal timestamps between consecutive events: **4,434**

Repeated activities are **not automatically errors** in process mining. They can represent real repeated tests or loop-backs. Equal timestamps are also possible for events recorded together; the validation therefore allows non-decreasing timestamps rather than requiring every event to have a strictly later timestamp.

## Dataset observations

The event log contains the following major activity types:

- Leucocytes: 3,370
- CRP: 3,255
- LacticAcid: 1,463
- Admission NC: 1,180
- ER Triage: 1,052
- ER Registration: 1,049
- ER Sepsis Triage: 1,048
- IV Antibiotics: 822
- IV Liquid: 752
- Release A: 671
- Return ER: 294
- Admission IC: 117
- Release B: 56
- Release C: 24
- Release D: 24
- Release E: 6

The data contains many repeated patient activities, which is useful for CareFlow because the project is intended to identify variations and loop-backs in patient journeys.

## Most common complete patient journeys

1. ER Registration -> ER Triage -> ER Sepsis Triage -> CRP -> Leucocytes — 46 case(s)
2. ER Registration -> ER Triage -> ER Sepsis Triage -> CRP -> LacticAcid -> Leucocytes -> IV Liquid -> IV Antibiotics — 41 case(s)
3. ER Registration -> ER Triage -> ER Sepsis Triage — 35 case(s)
4. ER Registration -> ER Triage -> ER Sepsis Triage -> CRP -> LacticAcid -> Leucocytes — 21 case(s)
5. ER Registration -> ER Triage -> ER Sepsis Triage -> CRP -> LacticAcid -> Leucocytes -> IV Liquid -> IV Antibiotics -> Admission NC -> CRP -> Leucocytes -> Release A — 18 case(s)
6. ER Registration -> ER Triage -> ER Sepsis Triage -> CRP -> LacticAcid -> Leucocytes -> IV Liquid -> IV Antibiotics -> Admission NC -> CRP -> Leucocytes -> CRP -> Leucocytes -> Release A — 11 case(s)
7. ER Registration -> ER Triage -> ER Sepsis Triage -> CRP -> LacticAcid -> Leucocytes -> IV Liquid -> IV Antibiotics -> Admission NC -> Release A — 11 case(s)
8. ER Registration -> ER Triage -> CRP -> LacticAcid -> Leucocytes -> ER Sepsis Triage -> IV Liquid -> IV Antibiotics — 10 case(s)
9. ER Registration -> ER Triage -> ER Sepsis Triage -> IV Liquid -> IV Antibiotics -> CRP -> LacticAcid -> Leucocytes — 10 case(s)
10. ER Registration -> ER Triage -> ER Sepsis Triage -> CRP -> LacticAcid -> Leucocytes -> IV Liquid -> IV Antibiotics -> Admission NC -> CRP -> Leucocytes -> Release A -> Return ER — 9 case(s)

## Important data-quality note

The original cleaned file contained 7 exact duplicate rows. These have been removed from `event_log_validated.csv`.

The original cleaned file also contains many equal-timestamp event pairs. These were **not removed**, because equal timestamps do not necessarily mean invalid events. The validated file preserves those events and only requires chronological order to be non-decreasing.

`Age_Group` has many missing values. It is an optional dashboard/filter field and is not required for the core PM4Py event-log schema. The required process-mining fields are `Case_ID`, `Activity_Name`, and `Timestamp`.

## Checkpoint conclusion

The validated event log is ready for handoff to the next pipeline stages:

**Python/data validation → BigQuery/dbt → PM4Py**

The core event-log requirements are satisfied:

1. Every event has a Case_ID.
2. Every event has an Activity_Name.
3. Every event has a valid timestamp.
4. Events can be ordered chronologically within each case.
5. Repeated activities are present for process-variation analysis.
6. Exact duplicate records have been removed from the validated handoff file.

## Files produced by sai_akshaya

- `data/event_log_clean.csv` — existing cleaned dataset
- `data/event_log_validated.csv` — validated handoff dataset
- `simulator/validate_event_log.py` — reusable validation script
- `docs/data_validation_report.md` — validation evidence/report

