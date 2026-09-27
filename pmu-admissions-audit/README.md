# PMU Admissions — Independent Audit & Executive Project Plan

Evidence verified on **2026-09-27** across 72 live resources (phase 1 in Opera, phases 2–3 via a remote renderer), starting from https://pmu.edu.sa/admission/admission.

- **Main deliverable:** [`PMU-Admissions-Executive-Plan.html`](PMU-Admissions-Executive-Plan.html). Single file, Arabic with English terms, print-ready, screenshots embedded.
- Findings register: [`registers/findings-register.md`](registers/findings-register.md) — 28 findings: 4 Critical, 10 High, 10 Medium, 3 Low, 1 Enhancement, plus a self-correction log and verified passes.
- Crawl coverage: [`registers/crawl-coverage.md`](registers/crawl-coverage.md)
- Data-point matrix: [`registers/data-point-matrix.md`](registers/data-point-matrix.md)
- External verification: [`evidence/external-verification.md`](evidence/external-verification.md)
- Field notes (verbatim page text): [`evidence/field-notes.md`](evidence/field-notes.md)
- Screenshots: [`evidence/screenshots/`](evidence/screenshots/)
- Page source (image placeholders): `src/plan.src.html`

Current project verdict: **FULL PROJECT CLOSURE — NOT MET** (baseline, before the project starts).

**Live re-verification (2026-09-27, audit container):**
- **G3 verifier:** NOT MET on 21/21 reachable pages, with 20 issues. No finding was resolved or overturned. See [`remediation/verification/report-live-2026-09-27.md`](remediation/verification/report-live-2026-09-27.md).
- **Static DOM baseline:** see [`evidence/dom-probes-2026-09-27.md`](evidence/dom-probes-2026-09-27.md).
- **Not done:** the rendered browser checks and the full-page screenshots S30–S35, because the in-container browser does not trust the egress proxy CA. See [`remediation/verification/LIVE-RUN-STATUS.md`](remediation/verification/LIVE-RUN-STATUS.md).
- **Rebuilding the plan:** `python3 src/build_plan.py`.

- **Remediation toolkit (ready to use):** [`remediation/`](remediation/README.md). Contains the canonical record seed, decision packs D0–D10, bilingual components, the legacy redirect map, the G3 verifier with tests, and the closure gate tracker.
