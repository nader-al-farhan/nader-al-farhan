# Remediation toolkit — what is ready now

This folder holds everything the project needs that does not depend on an institutional decision. None of it changes the PMU website. Publishing belongs to PMU's web team, after decisions are signed.

| Folder | Content | Used at |
|---|---|---|
| `canonical/` | Admissions Canonical Record seed: 19 records, each with its published values, sources, owner role, decision and status (`build_canonical.py` → `.json` / `.md`) | WS2, gates G1/G2 |
| `decisions/` | D0–D10 signable decision packs: evidence, neutral options, signature record | WS1, gate G1 |
| `content/` | Bilingual component templates bound to canonical fields; D0 request memo (Arabic) | WS3 |
| `legacy/redirect-map.csv` | 15 legacy URLs, each with its risk, replacement, lifecycle action and verification method | WS5, gate G6 |
| `verification/` | `drift_check.py` G3 verifier (live or fixtures), `checks.json`, unit tests (5/5 pass), baseline report, live report 2026-09-27, `dom_probe.js` (G5 DOM baseline) | WS6, gates G3/G7 |
| `closure/gate-tracker.md` | G0–G7 status with evidence | Steering committee |

Run the verifier against the live site from any network that can reach pmu.edu.sa:
```
cd verification && python3 drift_check.py --out report-live
```
Exit code 0 means G3 PASS. Any unreachable page counts as NOT MET.
