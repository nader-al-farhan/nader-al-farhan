# Live run status — BLOCKED

Checked: **2026-09-27 18:27 UTC** (audit environment, cloud container).

Tasks 2–5 of the live verification run (G3 live verifier, DOM/mobile probes, full-page screenshots, register and plan updates) were **not executed**. The site is still unreachable from this environment. No live evidence was collected, so no register entry, gate status or plan section was changed.

## Exact result

Access check, as specified:

```
$ curl -sS -o /dev/null -w "%{http_code}" https://pmu.edu.sa/admission/admission
curl: (56) CONNECT tunnel failed, response 403
000
```

Other hosts and schemes tried at the same time:

| URL | Result |
|---|---|
| `https://pmu.edu.sa/admission/admission` | `curl: (56) CONNECT tunnel failed, response 403` |
| `https://pmu.edu.sa/` | `curl: (56) CONNECT tunnel failed, response 403` |
| `https://www.pmu.edu.sa/` | `curl: (56) CONNECT tunnel failed, response 403` |
| `http://pmu.edu.sa/` | HTTP `403` returned by the egress proxy |

What the environment's egress proxy logged for these attempts (`$HTTPS_PROXY/__agentproxy/status`, `recentRelayFailures`):

```
"kind": "connect_rejected",
"detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
"host": "pmu.edu.sa:443"      (also "www.pmu.edu.sa:443")
```

DNS resolves: `pmu.edu.sa` → `2600:1407:e800:15::17cd:594c`, `2600:1407:e800:15::17cd:5944`. The block is at the egress gateway, not at DNS or at PMU's server.

## Fact vs. assumption

- **Fact:** the egress gateway still refuses `pmu.edu.sa:443` and `www.pmu.edu.sa:443` with a 403 on CONNECT. This is the same error recorded in `report-live-attempt.md`.
- **Assumption, not verified:** the allowlist change was made, but this running container still uses the old policy. Network policy changes may apply only to sessions or containers started after the change.

## To unblock

1. Confirm that `pmu.edu.sa` and `*.pmu.edu.sa` are in the environment's allowed domains. The setting is under the cloud environment menu → Edit → Network access. Access levels are described at https://code.claude.com/docs/en/claude-code-on-the-web.
2. Start a **new** session on this branch (`claude/pmu-admissions-audit-jm54d8`) and re-run step 1. Then continue:
   `cd pmu-admissions-audit/remediation/verification && python3 drift_check.py --out report-live-$(date +%F)`

## Effect on gates

No change. G3 and G5 remain **NOT MET** (unmeasured live). Verdict: **FULL PROJECT CLOSURE — NOT MET**.
