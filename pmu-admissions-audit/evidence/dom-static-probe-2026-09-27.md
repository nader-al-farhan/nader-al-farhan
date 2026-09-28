# DOM probe summary — 2026-09-27 (static HTML)

> **Superseded for layout and rendered text** by the browser-rendered probe [`dom-probes-2026-09-27.md`](dom-probes-2026-09-27.md) (Playwright/Chromium, run in a parallel session the same day). This static run is kept as an independent cross-check; where both measured the same thing, the results agree (see that file). It was renamed from `dom-probes-2026-09-27.*` during the merge.

Raw output: [`dom-static-probe-2026-09-27.json`](dom-static-probe-2026-09-27.json). Tool: [`remediation/verification/static_probe.py`](../remediation/verification/static_probe.py).

**Method and its limits (read first).** The probe reads the HTML each server sends for the 21 pages in `checks.json`. It fetches over plain GET: nothing is clicked, submitted or logged into. It does **not** run JavaScript and does **not** lay out the page. So:
- **Not measured:**
  - horizontal overflow at 390×844 and 1366×768
  - tables wider than the viewport
  - full-page screenshots S30–S35
  - any text that a script injects (the portal is a 3,290-byte JavaScript shell)
- **Why not:** the planned Playwright run could not be done. Chromium reached the site through the audit egress proxy but did not trust the proxy's certificate authority (`net::ERR_CERT_AUTHORITY_INVALID`). Adding that CA to the browser's trust store was refused by the environment's permission policy, and the change was reverted. The browser probe is kept as [`dom_probe.mjs`](../remediation/verification/dom_probe.mjs) for a network where a browser can load pmu.edu.sa normally.

This is a measured baseline of a few checkable properties. **It is not a WCAG audit and makes no compliance claim.**

## Per page

Images column: total images / images without an `alt` attribute. `#` = links whose href is exactly `#`. `http` = distinct `http://` link targets.

| Page key | HTTP | `<html lang>` | `dir` | viewport meta | H1 count | Heading-order skips | Images / no alt | `#` links | `http` links | Tables |
|---|---|---|---|---|---|---|---|---|---|---|
| hub | 200 | **none** | none | yes | 1 | 0 | 6 / 4 | 6 | 0 | 0 |
| ug_home | 200 | **none** | none | yes | 1 | 1 | 7 / 5 | 6 | 0 | 0 |
| freshman | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 0 |
| direct | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 1 | 0 |
| ielts | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 1 | 1 |
| toefl | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 1 |
| sat | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 1 |
| medicine | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 1 |
| medicine_academic | 200 | **none** | none | yes | 1 | 1 | 8 / 4 | 6 | 0 | 0 |
| medical_fees | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 2 |
| other_fees | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 3 |
| payment_policy | 200 | **none** | none | yes | **2** | 1 | 6 / 4 | 6 | 0 | 1 |
| calendar | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 4 |
| international | 200 | **none** | none | yes | **0** | 8 | 6 / 4 | 6 | 0 | 0 |
| cs_eng | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 3 | 2 |
| transfer | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 2 | 0 |
| emgms | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 0 |
| legacy_criteria | 200 | **none** | none | yes | 1 | 2 | 6 / 4 | 6 | 0 | 0 |
| apply | 200 | **none** | none | yes | 1 | 0 | 6 / 4 | 6 | 0 | 4 |
| portal | 200 | en | none | yes | **0** | 0 | 0 / 0 | 0 | 0 | 0 |
| guide_viewer | 200 | **none** | none | yes | **0** | 1 | 6 / 4 | 6 | 0 | 0 |

## Results

**Failures and risks (measured):**
1. **No `lang` attribute** on `<html>` on **20 of 20** pmu.edu.sa pages. The element is served as `<html xmlns="http://www.w3.org/1999/xhtml">` under an XHTML 1.0 Transitional doctype. No `dir` attribute is set either. The portal (`admissions.pmu.edu.sa/welcome`) declares `lang="en"`. A script could set these at runtime; that was not tested.
2. **Images without `alt`:** 81 in total. Every page carries the same 4 header/footer logo images with no `alt` (for example `../web-resources/home/images/logo-name.png` and `logo-PMU-1.png`). `ug_home` has one more.
3. **`href="#"` links:** 6 on every page, 120 in total.
4. **`http://` links** on 4 pages (`direct`, `ielts`, `cs_eng`, `transfer`), pointing to 4 distinct targets:
   - `http://admissions.pmu.edu.sa/`
   - `http://csbd.pmu.edu.sa/Continuing-Education/IELTS-Testing-Centre.aspx`
   - `http://pmu.edu.sa/Admission/Overview-Undergraduate-Placement-Tests.aspx`
   - `http://www.pmu.edu.sa/Admission/Admission_Calendar_FS_RO.aspx`
5. **Heading structure:**
   - 18 of 20 pages skip a heading level (for example h1 → h4 on `medical_fees`: "Undergraduate Fees").
   - `payment_policy` has **2 H1s** ("Tuition Fee Payment", "Tuition and Fee Payment Policy").
   - `international` and `guide_viewer` have **no H1**. `international` goes h2 → h4 eight times.
6. **Apply controls lead to two parallel landing pages:**
   - "Apply to PMU" (in the template on 20 pages) → `/apply.aspx` → `https://pmu.edu.sa/apply`.
   - "Apply Now" on 9 pages → `/Admission/Apply_Now_ADS.aspx` → `https://pmu.edu.sa/admission/apply_now_ads`, a separate page titled "Apply for Admission, Apply Now".
   - The calendar carries **7** Apply controls:
     - 1 → Apply_Now_ADS
     - 2 → `/Apply`
     - 2 ASP.NET postbacks (`javascript:WebForm_DoPostBackWithOptions(…"https://pmu.edu.sa/admission/Apply_Now_ADS"…)`), recorded but not triggered
     - 1 "Apply to PMU"
     - 1 "Applying for Aid"
   - On `medicine_academic`, "Apply Now" leads to the Medicine admission page (`/admission/college_of_medicine_admission.aspx`), not to an application.

**Passes (measured):**
- A viewport meta tag is present on 21 of 21 pages. This is a precondition for mobile rendering, not proof of it.
- Exactly one H1 on 17 of 20 site pages.
- No `http://` links on 16 of 20 site pages.
- Every page returned HTTP 200. None redirected to a login page, so the portal was measured too, though only its shell.
- Every Apply target that was resolved returned 200 after 1–2 redirects. No dead Apply link was found.

## What still needs a browser (Gate G5)
- overflow and table width at 390 and 1366 px
- keyboard and focus order
- contrast
- rendered accessible names
- the portal's rendered text (F-08 "No events are currently published")
- screenshots S30–S35
