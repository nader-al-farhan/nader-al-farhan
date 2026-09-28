# Link audit — live Admissions Office page (2026-09-28)

Read-only inventory of every link on https://pmu.edu.sa/admission/admission, with the status of each target, observations, the fix needed and screenshots.

| File | What it is |
|---|---|
| `PMU-Admissions-Hub-Link-Audit.html` | Report (Arabic). Self-contained: thumbnails embedded; each opens the full-size screenshot in the repo |
| `LINK-AUDIT-2026-09-28.md` | Same content as Markdown |
| `linkaudit-2026-09-28.json` | Data: every row, observations, severity, finding IDs, blueprint mapping |
| `shots/hub-annotated-{desktop,mobile}.png` | The live page with numbered link badges (red = issue on the link itself) |
| `shots/<ID>.jpg` | Target page, above the fold at 1366 px; known defect text outlined in red |

## Result
- 133 `<a>` elements on the page; 114 unique URLs.
- **107 tested:** 106 ended in 200. No 404s.
- **84 go through at least one redirect.**
- **7 not tested:** social sites, Taleo and the IT help desk are not reachable from this environment.
- **Severity:**
  - 7 links high: C04, C06, C08, C10, C19, C24, F08
  - 24 medium
  - 32 low
  - 7 with no observation
- **Page-level observations:**
  - no `lang` attribute and no Arabic version;
  - redirect chains on 33 of 36 content links;
  - three apply entry points;
  - four `#` links on user-visible menus: RSS, Directory, SiteMap and «Objectives»;
  - duplicated Research Centers menu.

New observations that are **not yet in the findings register**. These are proposals and need the owner's decision before they become F-31 onwards:
- C10's page `<title>` names another programme («Application Form for MSDH»).
- «ADMISSSIONS» is misspelled in the H1 of six graduate pages.
- «Contact Us» leads to a staff list reached through an `http://` hop.
- The footer calendar link points to 2021/22, and that page links to an internal host.
- «Campus Map» does not open a map.
- The footer college list omits Medicine.
- `#` links.

## Method
1. `extract.js`: Chromium lists every `<a>` with its region, group heading and box.
2. `check_links.py`: every unique URL is fetched with `curl -L`, TLS verified. The script records each hop, the final URL, the `<title>`, and the defect strings from `../verification/checks.json`.
3. `shots.js`: screenshots, with numbered badges on the hub.
4. `build_report.py`: builds the report, using `notes.py` for the manual observations and `../blueprint/ia.json` for the target IA.

All page loads go through `curlroute.js`: every request is fetched by curl and handed to Chromium. The browser never connects to the network and its certificate store is not modified. No clicks, no form input, no login.

Re-run:
```
NODE_PATH=$(npm root -g) node extract.js && cp /tmp/hub-links.json links.json
python3 check_links.py links.json ../verification/checks.json
# ids.json (stable link IDs B/C/F/H) is committed; regenerate it only if the page structure changes
NODE_PATH=$(npm root -g) node shots.js && python3 build_report.py
```

## Limits
- The portal (C06/C08) is a JavaScript application and does not render through curl routing, so it has no screenshot here. Earlier evidence (F-08, S30–S35) covers it.
- `http://admissions.pmu.edu.sa` returned 503 three times, with the body «upstream connect error … connection timeout». That text comes from this environment's proxy, so a server fault is **not established**.
- C04 (staff list) was not captured because it shows personal names.
