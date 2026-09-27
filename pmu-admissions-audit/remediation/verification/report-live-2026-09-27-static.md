> Static-only live run from a parallel session (no JavaScript): 20 issues, because the portal text (F-08) is injected by JavaScript and was not visible to it. **Superseded** by `report-live-2026-09-27.md` (static fetch + rendered portal text): 21 issues.

# Gate G3 — Surface conformance: **NOT MET**

Pages checked: 21 · unreachable: 0 · issues: 20

| Type | Finding | Page(s) | Detail |
|---|---|---|---|
| forbidden | F-04 | freshman | still contains: 'CBT 183' |
| forbidden | F-05 | international | still contains: 'SAT II' |
| forbidden | F-21 | emgms | still contains: 'CESL' |
| forbidden | F-12 | legacy_criteria | still contains: 'IELTS of 550' |
| forbidden | F-12 | legacy_criteria | still contains: 'Standard Battery Test' |
| forbidden | F-07 | medicine | still contains: 'the process typically involves' |
| forbidden | F-07 | medicine | still contains: 'to be developed in launch phase' |
| forbidden | F-17 | medicine | still contains: 'College of Medical' |
| forbidden | F-17 | hub | still contains: 'Visting' |
| forbidden | F-12 | hub | still contains: 'academic_calendar_2021_2022' |
| forbidden | F-24 | guide_viewer | still contains: 'Web-Admission-Guide-v2-2_20-12-18' |
| forbidden | F-16 | transfer | still contains: 'http://admissions.pmu.edu.sa' |
| forbidden | F-16 | cs_eng | still contains: 'http://admissions.pmu.edu.sa' |
| contradiction | F-22 | payment_policy | contains both 'All tuition payments are non-refundable' and 'Deduction Percentage' |
| conflict | F-04 | freshman,direct,ielts,transfer,international,apply | english_ug_direct.ielts_overall: ['5.5', '6.0'] |
| conflict | F-04 | freshman,toefl,apply | english_ug_direct.toefl_ibt: ['65', '83'] |
| conflict | F-03 | medicine,medical_fees | application_fee.medicine: ['1000', '1150'] |
| conflict | F-05 | sat,cs_eng,medicine | tahseely_rule.sat_score: ['1200', '1300'] |
| conflict | F-23 | medicine,medicine_academic | tuition_medicine.duration_years: ['6', '7'] |
| conflict | F-01 | ug_home,freshman,direct | composite_formula.hs_weight_general: ['30', '60'] |

## Consistency groups

| Rule | Values by page | Expected | OK |
|---|---|---|---|
| english_ug_direct.ielts_overall | {"freshman": ["5.5"], "direct": ["6.0"], "ielts": ["6.0"], "transfer": ["6.0"], "international": ["6.0"], "apply": ["6.0"]} | (pending decision) | NO |
| english_ug_direct.toefl_ibt | {"freshman": ["65"], "toefl": ["83"], "apply": ["83"]} | (pending decision) | NO |
| application_fee.medicine | {"medicine": ["1000"], "medical_fees": ["1150"]} | (pending decision) | NO |
| tahseely_rule.sat_score | {"sat": ["1200"], "cs_eng": ["1200"], "medicine": ["1300"]} | (pending decision) | NO |
| tuition_medicine.duration_years | {"medicine": ["7"], "medicine_academic": ["6"]} | (pending decision) | NO |
| composite_formula.hs_weight_general | {"ug_home": ["60"], "freshman": ["30"], "direct": ["60"]} | (pending decision) | NO |
