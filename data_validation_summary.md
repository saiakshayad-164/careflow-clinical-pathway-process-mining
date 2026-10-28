# CareFlow Data Validation Summary

## Purpose

This document summarizes the validation performed on the CareFlow clinical event log before process-mining analysis.

## Validation Areas

The event log was reviewed for the following data-quality aspects:

- Required event-log fields
- Missing or incomplete values
- Duplicate records
- Timestamp validity and consistency
- Activity and case identifiers
- Overall event-log structure

## Event Log Structure

The standardized event log uses the following core fields:

- `Case_ID` – identifies the patient/process case.
- `Activity_Name` – identifies the clinical activity or event.
- `Timestamp` – records when the activity occurred.
- `Resource` – identifies the associated resource where available.
- `Age_Group` – records the patient's age category where available.

## Process-Mining Preparation

After validation and cleaning, the event log was prepared for process-mining analysis using Python and PM4Py.

The standardized process-mining fields were mapped to:

- `case:concept:name`
- `concept:name`
- `time:timestamp`

## Validation Outcome

The validated event log was used as the basis for subsequent process discovery and process analysis.

The validation step helps ensure that the event data is structured consistently before generating process models and analyzing clinical pathway behavior.

## Related Project Files

- `data/event_log.csv`
- `data/event_log_clean.csv`
- `data/event_log_validated.csv`
- `simulator/validate_event_log.py`
- `docs/data_validation_report.md`
- `docs/checkpoint_1_sai_akshaya.md`