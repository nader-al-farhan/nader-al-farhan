# DOM / mobile probes — 2026-09-27

**Run:** 2026-09-27T19:12:19.445Z · Playwright 1.56.1 / Chromium headless · proxy CA trusted via the NSS store (TLS verification left on).
**Method:** read-only. `page.goto` on each of the 21 surfaces in `remediation/verification/checks.json` "pages", wait for `load` plus 2.5 s (6 s for the portal), then read the DOM. No clicks, no form input, no login. Two viewports: **390×844** (mobile, touch, iPhone UA) and **1366×768** (desktop).
**Raw data:** [`dom-probes-2026-09-27.json`](dom-probes-2026-09-27.json). **Screenshots:** full-page, 390×844, `screenshots/S30`–`S35`.
**Scope limit:** this is a set of automated DOM measurements. It is **not a WCAG audit** and makes no conformance claim. Colour contrast, keyboard operation, focus order, screen-reader output and the Arabic site were not tested.
**Portal:** `admissions.pmu.edu.sa/welcome` loaded without a login redirect, so it was included (landing page only). `pmu.edu.sa/apply` ends on the same portal URL in the browser.
**Viewport consistency:** every measured value below is identical at 390 and 1366, except page width.

## Results at a glance

| Check | Result | Pages |
|---|---|---|
| Page loads (HTTP) | **PASS** — 42/42 loads returned 200 | all 21 |
| Horizontal overflow (`scrollWidth > clientWidth`) | **PASS** — 0 at 390 and 0 at 1366 | 21/21 |
| Tables wider than viewport | **PASS** — 0 | 21/21 |
| `<meta name=viewport>` | **PASS** where checked — `width=device-width, initial-scale=1.0` in the hub source (curl); portal `width=device-width, initial-scale=1` | hub, portal |
| `<html lang>` | **FAIL** — attribute absent on 19 of 21 (`<html xmlns="http://www.w3.org/1999/xhtml">`); portal has `lang="en"` | hub, ug_home, freshman, direct, ielts, toefl, sat, medicine, medicine_academic, medical_fees, other_fees, payment_policy, calendar, international, cs_eng, transfer, emgms, legacy_criteria, guide_viewer |
| `<html dir>` | not set anywhere; computed direction `ltr`, consistent with English content | 21/21 |
| Exactly one visible H1 | **FAIL** on 4: no visible H1 on medicine_academic, international, guide_viewer; two H1s on payment_policy | — |
| Heading-level skips | **FAIL** on 16 of 21 (e.g. h1→h3, h1→h4, portal h1→h5) | ug_home, freshman, direct, ielts, toefl, sat, medicine, medical_fees, other_fees, calendar, cs_eng, transfer, emgms, legacy_criteria, apply, portal |
| `<img>` without `alt` attribute | **FAIL** — 79 images on 21 of 21 pages (4 header/footer logos repeated on every pmu.edu.sa page; plus `admission-banner.png` on ug_home and `admissions-banner.jpg` on the portal) | 21/21 |
| Links with `href="#"` | **FAIL** — 114 links on 19 pages (6 per template page: “Directory”, “SiteMap” and empty-text links) | 19/21 |
| Links with `http://` | **FAIL** — 8 links on 4 pages | cs_eng, direct, ielts, transfer |

## Per-page measurements (390×844; desktop identical except width)

| Page | Final URL | lang | dir / computed | scrollW/clientW (390 · 1366) | wide tables | visible H1 | heading skips | img no-alt / total | `#` links | http links |
|---|---|---|---|---|---|---|---|---|---|---|
| hub | `pmu.edu.sa/admission/admission` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | — | 4/6 | 6 | 0 |
| ug_home | `pmu.edu.sa/admission/undergraduate_programs_admission` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("New Applicant:") | 5/7 | 6 | 0 |
| freshman | `www.pmu.edu.sa/admission/freshman_admission` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h4 ("Freshman Admission Requirements") | 4/6 | 6 | 0 |
| direct | `pmu.edu.sa/admission/direct-admissions-from-secondary-school` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("Freshman Admissions") | 4/6 | 6 | 1 |
| ielts | `pmu.edu.sa/admission/ielts-admission` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("(IELTS)") | 4/6 | 6 | 1 |
| toefl | `pmu.edu.sa/admission/toefl-admission` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("TOEFL iBT") | 4/6 | 6 | 0 |
| sat | `pmu.edu.sa/admission/sat-admission` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("Scholastic Aptitude Test (SAT)") | 4/6 | 6 | 0 |
| medicine | `pmu.edu.sa/admission/college_of_medicine_admission` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("Curriculum Structure") | 4/6 | 6 | 0 |
| medicine_academic | `www.pmu.edu.sa/academics/college_of_medicine_udp` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 0 (DOM 1) | — | 4/8 | 6 | 0 |
| medical_fees | `pmu.edu.sa/admission/medical_program_studies_fees_tf_ro` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h4 ("Undergraduate Fees") | 4/6 | 6 | 0 |
| other_fees | `pmu.edu.sa/admission/student_fees_tf_ro` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h4 ("Admission Application Fees- Undergraduate Programs") | 4/6 | 6 | 0 |
| payment_policy | `pmu.edu.sa/admission/payment_method_tf_ro` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 2 (DOM 2) | — | 4/6 | 6 | 0 |
| calendar | `pmu.edu.sa/admission/admission_calendar_fs_ro` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("STAY CONNECTED") | 4/6 | 6 | 0 |
| international | `pmu.edu.sa/admission/international_students` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 0 (DOM 0) | — | 4/6 | 6 | 0 |
| cs_eng | `pmu.edu.sa/admission/admissions_requirements_cs_eng_majors` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("General Requirements:") | 4/6 | 6 | 4 |
| transfer | `pmu.edu.sa/admission/admission-from-other-universities` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("Transfer Admissions") | 4/6 | 6 | 2 |
| emgms | `pmu.edu.sa/admission/admissions_requirements_emgms_gdp` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("Master of Science in Engineering Management Application(EMGMS) Checklist") | 4/6 | 6 | 0 |
| legacy_criteria | `www.pmu.edu.sa/admission/admission_procedures_criteria_fs_ro` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h3 ("Student Categories") | 4/6 | 6 | 0 |
| apply | `admissions.pmu.edu.sa/welcome` | en | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h5 ("Admission Calendar") | 1/1 | 0 | 0 |
| portal | `admissions.pmu.edu.sa/welcome` | en | absent / ltr | 390/390 · 1366/1366 | 0 | 1 (DOM 1) | h1→h5 ("Admission Calendar") | 1/1 | 0 | 0 |
| guide_viewer | `pmu.edu.sa/pdf/viewer?ID=203` | **absent** | absent / ltr | 390/390 · 1366/1366 | 0 | 0 (DOM 0) | — | 4/6 | 6 | 0 |

## `http://` links (verbatim)

| Page | Link text | href |
|---|---|---|
| direct | Submit documents before due date | `http://www.pmu.edu.sa/Admission/Admission_Calendar_FS_RO.aspx` |
| ielts | Apply for IELTS | `http://csbd.pmu.edu.sa/Continuing-Education/IELTS-Testing-Centre.aspx` |
| cs_eng | Complete online application | `http://admissions.pmu.edu.sa/` |
| cs_eng | Submit documents before due date | `http://www.pmu.edu.sa/Admission/Admission_Calendar_FS_RO.aspx` |
| cs_eng | if available | `http://pmu.edu.sa/Admission/Overview-Undergraduate-Placement-Tests.aspx` |
| cs_eng | read more... | `http://pmu.edu.sa/Admission/Overview-Undergraduate-Placement-Tests.aspx` |
| transfer | Complete online application | `http://admissions.pmu.edu.sa/` |
| transfer | Submit documents before due date | `http://www.pmu.edu.sa/Admission/Admission_Calendar_FS_RO.aspx` |

Whether these http:// URLs upgrade to HTTPS could not be tested: the audit environment's egress proxy answers plain-HTTP requests itself with 403, so no claim is made about their server behaviour.

## Every “Apply / قدّم” control and its actual href

The label pattern was `/apply|قدّم|قدم/i` on `a`, `button` and `input` elements. No Arabic “قدّم” label was found on these 21 English surfaces. “(hidden)” = present in the DOM but not rendered (collapsed menu or accordion).

| href (as written in the page) | Where (page: text) |
|---|---|
| `https://www.pmu.edu.sa/apply` | hub: “Apply Now”<br>hub: “Apply” |
| `https://pmu.edu.sa/apply` | ug_home: “Apply Now”<br>international (hidden): “Apply” |
| `../Admission/Apply_Now_ADS.aspx` | freshman: “Apply Now”<br>direct: “Apply Now”<br>ielts: “Apply Now”<br>toefl: “Apply Now”<br>sat: “Apply Now”<br>medicine: “Apply Now”<br>calendar: “Apply Now”<br>cs_eng: “Apply Now”<br>transfer: “Apply Now” |
| `#menu11` | direct (hidden): “Applying for Aid”<br>ielts (hidden): “Applying for Aid”<br>toefl (hidden): “Applying for Aid”<br>sat (hidden): “Applying for Aid”<br>medicine (hidden): “Applying for Aid”<br>calendar (hidden): “Applying for Aid”<br>cs_eng (hidden): “Applying for Aid”<br>transfer (hidden): “Applying for Aid” |
| `http://csbd.pmu.edu.sa/Continuing-Education/IELTS-Testing-Centre.aspx` | ielts: “Apply for IELTS” |
| `../admission/college_of_medicine_admission.aspx` | medicine_academic: “Apply Now” |
| `https://pmu.edu.sa/Apply` | calendar: “Apply Now”<br>calendar: “Apply Now” |
| `javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("ctl00$ContentPlaceHolder_ContentArea$ctl03", "", false, "", "https://pmu.edu.sa/admission/Apply_Now_ADS", false, true))` | calendar (hidden): “Apply Now” |
| `javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("ctl00$ContentPlaceHolder_ContentArea$ctl09", "", false, "", "https://pmu.edu.sa/admission/Apply_Now_ADS", false, true))` | calendar (hidden): “Apply Now” |
| `../Admission/Application_Form_EMBA_GDP.aspx` | emgms (hidden): “Apply for EMBA” |
| `../Admission/Application_Form_MBA_GDP.aspx` | emgms (hidden): “Apply for MBA” |
| `../Admission/Application_Form_MSEHD_GDP.aspx` | emgms (hidden): “Apply for MSHD” |
| `../Admission/Application_Form_MSME_GDP.aspx` | emgms (hidden): “Apply for MSME” |

Resolved with GET (no form submission), {date}:
- `https://pmu.edu.sa/Apply` → 301 → `https://pmu.edu.sa/apply` (200; renders the portal landing `admissions.pmu.edu.sa/welcome` in the browser).
- `../Admission/Apply_Now_ADS.aspx` and the hidden postback targets → `/admission/apply_now_ads` (200, title “Apply for Admission, Apply Now”).
- `../admission/college_of_medicine_admission.aspx` (label “Apply Now” on the Medicine academic page) → the Medicine **admission information page**, not an application channel.
- `http://admissions.pmu.edu.sa/` (label “Complete online application”) — plain http, not testable here (see above).

**Reading:** the same “Apply” intent points to at least **four different endpoints** (`www.pmu.edu.sa/apply`, `pmu.edu.sa/apply`, `/admission/apply_now_ads`, `http://admissions.pmu.edu.sa/`), plus one “Apply Now” that leads to an information page. This is evidence for F-02 and Gate G4.

## Rendered-text capture for the G3 verifier

The portal is an Angular single-page app: its static HTML is a 3 KB shell. Its rendered text (390×844) is saved in `remediation/verification/rendered-2026-09-27/portal.txt` and fed to `drift_check.py --rendered`. It still reads, verbatim: “Admission Calendar … No events are currently published. Please check back later.” and “2022 © PMU”.
