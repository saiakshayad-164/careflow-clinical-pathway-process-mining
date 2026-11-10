# Week 4 – Conformance Checking

## Objective
Compare actual patient event transitions with a proposed analytical reference journey using dbt and BigQuery.

## dbt Models
- `expected_transitions.sql`: Defines the proposed expected activity transitions.
- `conformance_check.sql`: Compares actual consecutive transitions against expected transitions.
- `mart_case_conformance.sql`: Summarizes conformance results for each patient case.

## Conformance Categories
- **COMPLIANT:** Transition exists in the expected transition list.
- **UNEXPECTED_REVIEW:** Transition is not present in the expected list and requires further review.
- **RETURN_VISIT_REVIEW:** Discharge followed by a Return ER event, classified separately.

## Validation Results
- Total cases: 1,049
- Total transitions: 14,134
- Compliant transitions: 9,485
- Unexpected transitions for review: 4,356
- Return visit transitions: 293

## Important Note
The expected journey is an analytical reference drafted using the simulated dataset. It is not an officially approved clinical protocol. Unexpected transitions are review flags and do not automatically indicate clinical errors.
