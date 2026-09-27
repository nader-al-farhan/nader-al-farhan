# Closure Gate Tracker — PMU Admissions

Status date: 2026-09-27 (live re-verification 19:09–19:20 UTC). A gate is **PASS** only with evidence produced by the independent verifier (Quality / Institutional Effectiveness). A gate that cannot be proven counts as **NOT MET**.

| Gate | Pass criterion | Evidence required | Tooling ready | Current status | Evidence now |
|---|---|---|---|---|---|
| G0 Mandate | Charter approved; sponsor named; one functional owner per data domain | Signed D0; owner list | `decisions/D0.md`, `canonical/admissions-canonical.md` (owner column) | NOT MET | D0 not signed |
| G1 Authoritative rules | D1–D10 signed; Rules Book v1 with effective date | Signed packs; `approved_value` filled | `decisions/*.md`, `canonical/build_canonical.py` | NOT MET | 0/10 signed; 16 of 19 records in conflict |
| G2 Canonical data | 100% of records approved; programme register unified | `admissions-canonical.json` with no null `approved_value` | canonical seed (19 records) | NOT MET | 2/19 have an approved value (tuition label, VAT) |
| G3 Surface conformance | 0 forbidden strings, 0 contradictions, 1 value per rule on all surfaces | `verification/drift_check.py` report on the live site = PASS | verifier + tests (5/5 passing) | NOT MET | **Live run 2026-09-27: 21/21 surfaces fetched, 21 issues — identical to the baseline** (14 forbidden strings, 1 contradiction, 6 value conflicts). `verification/report-live-2026-09-27.md` |
| G4 Journey & routing | 6/6 persona journeys reach the correct channel within 3 clicks; site and portal show the same intake status | Recorded journey tests | persona scripts to be written in WS6 | NOT MET | Live DOM probe: at least 4 endpoints behind the same “Apply” label, plus one “Apply Now” that opens an information page (`evidence/dom-probes-2026-09-27.md`) |
| G5 Quality | WCAG 2.2 AA: 0 critical/serious; 0 http/# links; 100% AR/EN parity for core components | Automated + manual a11y report; parity diff | `verification/dom_probe.js` (Playwright, rendered — used); `verification/static_probe.py` (static cross-check); `verification/dom_probe.mjs` (alternative browser probe) | NOT MET | **Measured baseline 2026-09-27 (21 surfaces, 390 + 1366 px):** `lang` absent on 19/21 · 8 http:// links (4 pages) · 114 `#` links (19 pages) · 79 images without `alt` (21 pages) · heading skips on 16/21 · **passes:** 0 horizontal overflow, 0 over-wide tables. AR/EN parity: 0% on rule pages (F-14). Full WCAG test not yet run. |
| G6 Legacy | Every row of `legacy/redirect-map.csv` in its terminal state and verified | Crawl + search-console export | redirect map (15 rows) | NOT MET | 0/15 terminal |
| G7 Operate | Two consecutive monthly drift runs with 0 unresolved issues; signed handover | Two G3 reports + handover note | verifier can be scheduled | NOT MET | not started |

## Verdict

**FULL PROJECT CLOSURE — NOT MET**

This is the measured baseline. The live re-verification on 2026-09-27 confirmed it: no gate changed state. The verdict can only change to PASS after PMU signs D0–D10, publishes corrected content, and two live drift runs return 0 issues.
