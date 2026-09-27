# Live run status — PARTIAL (text and static DOM done; rendered browser checks blocked)

## Timeline (2026-09-27, UTC)

| Time | Event |
|---|---|
| 18:27 | First attempt. `curl: (56) CONNECT tunnel failed, response 403` for `pmu.edu.sa:443` and `www.pmu.edu.sa:443`. The egress proxy logged `"gateway answered 403 to CONNECT (policy denial or upstream failure)"`. Nothing was run. |
| 18:58 | A separate session in a fresh container re-checked: still 403 on CONNECT for `pmu.edu.sa`, and also for `example.com` and `www.google.com`, so the block was policy-wide at that time. That session withdrew the assumption that "only the old container kept the old policy" (commit `c2de3eb`; full record in git history). |
| 19:07 | After the allowlist was updated: `https://pmu.edu.sa/admission/admission` returned **200**. `www.pmu.edu.sa` and `admissions.pmu.edu.sa` still returned 403 on CONNECT. |
| ~19:10 | All three hosts returned 200 on three consecutive attempts, so the policy had propagated. |

## Done

- **G3 live verifier:** `report-live-2026-09-27.md` / `.json`. 21/21 pages reachable. Verdict **NOT MET**, 20 issues. Compared with `report-baseline-2026-09-27.md`, no issue was resolved by PMU.
  - A verifier false negative on F-24 was found and fixed. The link was in a single-quoted `src`. A test was added, and 4/4 tests pass.
  - F-08 (portal) is JavaScript-rendered, so it cannot be re-verified by a static fetch.
- **Static DOM probe:** `static_probe.py` → `../../evidence/dom-probes-2026-09-27.json` / `.md`.

## Blocked: rendered browser checks

Not done: horizontal overflow and table width at 390×844 / 1366×768, JavaScript-injected text (portal), and full-page screenshots S30–S35.

- **Fact:** headless Chromium (Playwright 1.56.1, `/opt/pw-browsers`) reached the site through the audit egress proxy and failed on every page with `net::ERR_CERT_AUTHORITY_INVALID`. The browser's NSS trust store did not contain the proxy's interception CA.
- **Fact:** adding that CA to the browser's trust store was refused by the environment's permission policy (classified as a TLS/auth weakening). The change was reverted, and the NSS store is back to empty. No other workaround was attempted, and TLS verification was never disabled.
- **To unblock (either one):**
  1. Run `NODE_PATH=$(npm root -g) node dom_probe.mjs ../../evidence/dom-probes-<date>-rendered.json ../../evidence/screenshots` from a machine with a normal internet connection.
  2. Have the environment owner explicitly allow the browser to trust the environment's egress CA.

## Effect on gates

- G3: **NOT MET**, now measured live.
- G5: **NOT MET**. There is a static baseline; the rendered checks are still pending.
- Verdict: **FULL PROJECT CLOSURE — NOT MET**.
