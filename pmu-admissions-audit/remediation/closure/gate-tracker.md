# Closure Gate Tracker — PMU Admissions

Status date: 2026-09-27 (updated after the live run). A gate is **PASS** only with evidence produced by the independent verifier (Quality / Institutional Effectiveness). A gate that cannot be proven counts as **NOT MET**.

| Gate | Pass criterion | Evidence required | Tooling ready | Current status | Evidence now |
|---|---|---|---|---|---|
| G0 Mandate | Charter approved; sponsor named; one functional owner per data domain | Signed D0; owner list | `decisions/D0.md`, `canonical/admissions-canonical.md` (owner column) | NOT MET | D0 not signed |
| G1 Authoritative rules | D1–D10 signed; Rules Book v1 with effective date | Signed packs; `approved_value` filled | `decisions/*.md`, `canonical/build_canonical.py` | NOT MET | 0/10 signed; 16 of 19 records in conflict |
| G2 Canonical data | 100% of records approved; programme register unified | `admissions-canonical.json` with no null `approved_value` | canonical seed (19 records) | NOT MET | 2/19 have an approved value (tuition label, VAT) |
| G3 Surface conformance | 0 forbidden strings, 0 contradictions, 1 value per rule on all surfaces | `verification/drift_check.py` report on the live site = PASS | verifier + tests (4/4 passing) | NOT MET | **Live run 2026-09-27: NOT MET**, 21/21 pages reachable, 20 issues (`verification/report-live-2026-09-27.md`). No baseline issue was resolved. F-08 (portal) could not be re-verified without a browser. |
| G4 Journey & routing | 6/6 persona journeys reach the correct channel within 3 clicks; site and portal show the same intake status | Recorded journey tests | persona scripts to be written in WS6 | NOT MET | 5 divergent apply entry points. Live 2026-09-27: every Apply control resolves to one of two parallel landing pages (`/apply`, `/admission/apply_now_ads`), and the calendar carries 7 Apply controls. |
| G5 Quality | WCAG 2.2 AA: 0 critical/serious; 0 http/# links; 100% AR/EN parity for core components | Automated + manual a11y report; parity diff | `verification/static_probe.py` (run); `verification/dom_probe.mjs` (needs a browser that can load the site) | NOT MET | **Static baseline measured 2026-09-27** (`../evidence/dom-probes-2026-09-27.md`): no `<html lang>` on 20/20 pages; 81 images without alt; 120 `#` links; `http://` links on 4 pages; heading skips on 18/20 pages. Passes: viewport meta 21/21, one H1 on 17/20. Layout, overflow and rendered checks are not measured (no trusted browser). |
| G6 Legacy | Every row of `legacy/redirect-map.csv` in its terminal state and verified | Crawl + search-console export | redirect map (15 rows) | NOT MET | 0/15 terminal |
| G7 Operate | Two consecutive monthly drift runs with 0 unresolved issues; signed handover | Two G3 reports + handover note | verifier can be scheduled | NOT MET | not started |

## Verdict

**FULL PROJECT CLOSURE — NOT MET**

This is the measured baseline. The verdict can only change to PASS after PMU signs D0–D10, publishes corrected content, and two live drift runs return 0 issues.
