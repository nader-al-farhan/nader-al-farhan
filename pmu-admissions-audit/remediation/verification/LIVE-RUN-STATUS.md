# Live run status — BLOCKED (re-checked in a fresh container)

Latest check: **2026-09-27 18:58 UTC** — new session, new container, started after the user reported changing the network policy to allow all domains.
Previous check: 2026-09-27 18:27 UTC (earlier container; details kept below).

## Re-check 2026-09-27 18:58 UTC — result

The site is still unreachable. Tasks 2–5 (G3 live verifier, DOM/mobile probes, full-page screenshots, register and plan updates) were **not executed**. No live evidence was collected; no register entry, gate status or plan section was changed.

```
$ curl -sS -o /dev/null -w "%{http_code}" https://pmu.edu.sa/admission/admission
curl: (56) CONNECT tunnel failed, response 403
000
```

Control tests, to tell a policy-wide block from a host-specific one:

| URL | Result (18:58 UTC) |
|---|---|
| `https://pmu.edu.sa/admission/admission` | `curl: (56) CONNECT tunnel failed, response 403` |
| `https://www.pmu.edu.sa/` | `curl: (56) CONNECT tunnel failed, response 403` |
| `http://pmu.edu.sa/` | HTTP `403` returned by the egress proxy |
| `https://example.com` | `curl: (56) CONNECT tunnel failed, response 403` |
| `https://www.google.com` | `curl: (56) CONNECT tunnel failed, response 403` |
| `https://github.com` | reached (HTTP `400` from GitHub — connection allowed) |
| `https://pypi.org/simple/` | HTTP `200` (package registry, bypasses the gateway) |

Egress proxy log (`$HTTPS_PROXY/__agentproxy/status`, `recentRelayFailures`):

```
{"ts": "2026-09-27T18:57:26.749Z", "kind": "connect_rejected",
 "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)", "host": "pmu.edu.sa:443"}
{"ts": "2026-09-27T18:57:27.053Z", "kind": "connect_rejected",
 "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)", "host": "example.com:443"}
```

DNS resolves (`pmu.edu.sa` → `23.209.94.209`), so the block is at the egress gateway.

### Fact vs. assumption (updated)

- **Fact:** the block is **policy-wide, not specific to PMU**. `example.com` and `www.google.com` are refused the same way; only GitHub and package registries get through. This matches a restricted/"trusted hosts" network level, not "all domains".
- **Fact:** this session started in a fresh container, so the earlier assumption ("the change was made but the old container kept the old policy") is **withdrawn** — a new container still has the restricted policy.
- **Assumption, not verified:** the "allow all domains" change was not saved to the environment this session runs in (e.g. it was made on a different environment, or not saved).

#### To unblock (as recorded at 18:27)

1. Open the cloud environment menu in the session title bar → **Edit** → **Network access**, set it to full/unrestricted access (or add `pmu.edu.sa` and `*.pmu.edu.sa` to allowed domains), and save. Make sure it is the same environment the session uses. Access levels: https://code.claude.com/docs/en/claude-code-on-the-web
2. Start a new session on branch `claude/pmu-admissions-audit-jm54d8`. A quick check that the change took effect: `curl -sS -o /dev/null -w "%{http_code}" https://example.com` must return `200`.

---

## Earlier check — 2026-09-27 18:27 UTC (previous container)

Tasks 2–5 of the live verification run (G3 live verifier, DOM/mobile probes, full-page screenshots, register and plan updates) were **not executed**. The site is still unreachable from this environment. No live evidence was collected, so no register entry, gate status or plan section was changed.

### Exact result

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

### Fact vs. assumption (as recorded at 18:27)

- **Fact:** the egress gateway still refuses `pmu.edu.sa:443` and `www.pmu.edu.sa:443` with a 403 on CONNECT. This is the same error recorded in `report-live-attempt.md`.
- **Assumption, not verified:** the allowlist change was made, but this running container still uses the old policy. Network policy changes may apply only to sessions or containers started after the change.

### To unblock (as recorded at 18:27)

1. Confirm that `pmu.edu.sa` and `*.pmu.edu.sa` are in the environment's allowed domains. The setting is under the cloud environment menu → Edit → Network access. Access levels are described at https://code.claude.com/docs/en/claude-code-on-the-web.
2. Start a **new** session on this branch (`claude/pmu-admissions-audit-jm54d8`) and re-run step 1. Then continue:
   `cd pmu-admissions-audit/remediation/verification && python3 drift_check.py --out report-live-$(date +%F)`

## Effect on gates

No change after either check. G3 and G5 remain **NOT MET** (unmeasured live). Verdict: **FULL PROJECT CLOSURE — NOT MET**.
