{{ config(materialized='table') }}

SELECT *
FROM UNNEST([

    -- Registration and triage
    STRUCT('ER Registration' AS from_activity, 'ER Triage' AS to_activity),
    STRUCT('ER Triage', 'ER Sepsis Triage'),

    -- Sepsis triage to laboratory investigations
    STRUCT('ER Sepsis Triage', 'CRP'),
    STRUCT('ER Sepsis Triage', 'Leucocytes'),
    STRUCT('ER Sepsis Triage', 'LacticAcid'),

    -- Flexible laboratory test sequences
    STRUCT('CRP', 'Leucocytes'),
    STRUCT('CRP', 'LacticAcid'),
    STRUCT('Leucocytes', 'CRP'),
    STRUCT('Leucocytes', 'LacticAcid'),
    STRUCT('LacticAcid', 'CRP'),
    STRUCT('LacticAcid', 'Leucocytes'),

    -- Laboratory investigations to treatment
    STRUCT('CRP', 'IV Liquid'),
    STRUCT('CRP', 'IV Antibiotics'),
    STRUCT('Leucocytes', 'IV Liquid'),
    STRUCT('Leucocytes', 'IV Antibiotics'),
    STRUCT('LacticAcid', 'IV Liquid'),
    STRUCT('LacticAcid', 'IV Antibiotics'),

    -- Treatment sequence
    STRUCT('IV Liquid', 'IV Antibiotics'),
    STRUCT('IV Antibiotics', 'Admission NC'),

    -- Admission to discharge
    STRUCT('Admission NC', 'Release A'),
    STRUCT('Admission NC', 'Release B'),
    STRUCT('Admission NC', 'Release C'),
    STRUCT('Admission NC', 'Release D'),
    STRUCT('Admission NC', 'Release E')

])
