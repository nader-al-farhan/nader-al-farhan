# Field notes (raw) — captured via user's Opera browser (Browser Connector), 2026-09-27
Method: accessibility-tree text extraction (tab-content) + viewport screenshots. Container egress to pmu.edu.sa blocked; all live reads via Opera.

## P01 https://pmu.edu.sa/admission/admission — Admissions Office hub
- Link-list hub only (6 groups: Future Students, International, Graduate, Undergraduate, Placement Tests). No intro text, no deadline/status, no Arabic toggle visible.
- "Contact Us" -> Staff_Profile/Staff_List.aspx?&DEpt=4 (staff directory, not admissions contact page)
- "Apply Now" and International "Apply" -> https://www.pmu.edu.sa/apply
- Typo: "Visting Students"
- Graduate: 11 program links, mixed URL patterns (application_form_*_gdp vs Admissions_Requirements_*_GDP); "MIlBL" typo in URL.
- Footer: "Academic Calendar" -> academic_calendar_2021_2022_ro.aspx ; "2021 © PMU" ; Directory/SiteMap -> "#" (dead); social icon "#" ; two Twitter accounts (PMU_KSA, pmuofficial)
- Footer colleges list: Engineering, CCES, Business, Law (URL law_dept_cshs_udp), Architecture & Design, Sciences & Human Studies, Prep. **No College of Medicine** in footer.
- Screenshot S01.

## P02 https://pmu.edu.sa/admission/undergraduate_programs_admission — UG Admissions home
- GPA *80% or equivalent; Qudrat *60% or equivalent (SAT 1); fee "non-refundable application fee of SAR 950 (incl. VAT) upon submission of documents"
- Lower %: composite "Secondary School 60% / General Aptitude Test 40%" (no Tahseely)
- Day up to 20 credits; Evening 12 max
- "College of Medical Admissions" / "PMU College of Medical curriculum ... 7-year hybrid"
- "Undergraduate Program" para lists colleges: Arch & Design, CCES, Business Admin, Law, Engineering — omits Medicine and Sciences & Human Studies
- Links go to .aspx legacy URLs (Direct-Admissions-from-Secondary-School.aspx etc.)

## P03 https://www.pmu.edu.sa/admission/freshman_admission — Freshman Admission (newer template, left side-menu)
- Side menu: Freshman / Transfer (#anchors), Apply Now -> Apply_Now_ADS.aspx, Tuition & Fees -> Tuition_Fees_RO.aspx (DIFFERENT fees URL than hub's Fees_TF_RO.aspx), "Web Admission Guide" -> PDF/Viewer.aspx?ID=203
- Req: "completed high school within the last 5 years"; placement test + interview on stated date
- Submit: e-form, original sec. certificate, "Recent Score of the Aptitude Test" (NCTE), ID/Iqama, passport, 2 photos, employer NOC, "A S.R.950 Admission and English Placement Test Fee (Non-refundable)" (no VAT mention; described as admission+placement fee vs P02 "application fee incl. VAT")
- Exemption: "TOEFL score of 513 (CBT 183, iBT 65) or more, or IELTS Band 5.5 (min 5.5 writing)", scores < 2 years old. (CBT retired by ETS ~2006.)
- **Weighted criteria: High school 30% / Aptitude Test 50% / Personal Interview 20%** — CONFLICTS with P02 (Secondary 60% / GAT 40%). No Tahseely in either.
- No minimum GPA/Qudrat thresholds stated here (P02: 80% / 60%).
- Breadcrumb lacks Home.

## P04 https://pmu.edu.sa/admission/direct-admissions-from-secondary-school — Direct Admissions (legacy .aspx redirects to extensionless)
- Breadcrumb ends "> Freshman" though page is "Direct Admissions" (label drift). Side menu "Contact Info" -> Admission_Contact_GDP.aspx (GRADUATE contact page) from an UNDERGRADUATE page.
- Criteria: GPA *80%, Qudrat *60% (SAT 1), **IELTS Academic 6.0 overall / 5.5 writing** ("or equivalent TOEFL iBT" — no number given here)
- Lower %: Secondary 60% / GAT 40% (same as P02, conflicts with P03 30/50/20)
- Docs: photos, sec cert copy, Qudrat copy, Saudi ID, Family ID card (female, if available), passport, employer NOC. (P03 asks ORIGINAL certificate + Iqama for non-Saudis; P04 asks COPY and Saudi ID only → no non-Saudi path)
- Fee "non-refundable application fee of SAR 950 (incl. VAT)"
- Process: interview appointment; decision via Admissions Office (no timeline/SLA)
- "Submit documents before due date" link uses http:// (non-HTTPS)
- CONFLICT vs P03: IELTS 5.5 (P03 exemption) vs 6.0 (P04 direct entry). Both claim to be freshman/direct-entry routes.

## P05 https://pmu.edu.sa/admission/overview-undergraduate-placement-tests — Placement Tests overview
- Thin: one paragraph; "Read more about the current technology used..." — "Read more" is plain text (not a link); names Aptis, IELTS, TOEFL. No SAT/Duolingo/other tests; no fee; no dates for placement test sessions.

## P06 https://pmu.edu.sa/admission/ielts-admission — IELTS
- Table: LEVEL / Overall / Writing: Core 6.0/5.5; Advanced 5.0/4.5; Intermediate 4.5/4.0; Beginner 4.0/3.5; Pre-Beginner N/A. Validity: 2 years to commencement date of applied semester.
- "Core" is unexplained jargon (= direct entry to degree?). Bypass/placement text.
- "Apply for IELTS" -> http://csbd.pmu.edu.sa/Continuing-Education/IELTS-Testing-Centre.aspx (http, separate subdomain)
- CONFIRMS CONFLICT: P03 exemption at IELTS 5.5 (writing 5.5) vs P04/P06 6.0 (writing 5.5).
- Validity rule wording differs: P03 "less than two years old" vs P06 "two years from test date to commencement of applied semester".

## P07 https://pmu.edu.sa/admission/toefl-admission — TOEFL
- Table (0–120 scale only): Core 83 / Writing 19; Advanced 63/15; Intermediate 54/13; Beginner 42/11; Pre-Beginner N/A. Validity 2 yrs to semester start.
- "(online or home edition is not accepted)"; score sent from ETS; "PMU DI code: 6993"
- No 1–6 band equivalents (ETS scale changed 21 Jan 2026 — see X01).
- CONFLICT: P03 exemption TOEFL iBT 65 (and PBT 513, CBT 183) vs P07 Core iBT 83 / W19. ~18-point gap on the same "bypass Prep" decision.

## P08 https://pmu.edu.sa/admission/aptis-placement-test — Aptis
- Levels listed (Pre Beginner, Beginner, Intermediate, Advanced) with NO score thresholds (IELTS/TOEFL pages give thresholds; Aptis does not) → applicant cannot self-assess.
- Test ~4 hours. Aptis cannot place into Core: "If a candidate feels eligible for direct entry into the Core Program, he/she will be required to take the IELTS" (TOEFL not mentioned as alternative here, though TOEFL page offers Core route).
- Candidate guide PDF: Attachments/Admission/PDF/Appendix 3.3 (Aptis Candidate Guide).pdf — "August 2017" edition (per search title).
- Links out to britishcouncil.org Aptis pages (6 URLs printed as raw link text – poor UX/accessibility).

## P09 https://pmu.edu.sa/admission/college_of_medicine_admission — College of Medicine
- Mostly curriculum description (Years 1–6); "College of Medical" (grammar) ; "Population Health (to be developed in launch phase)" x2 — launch-phase text still live.
- Admission Criteria paragraph contains generic explanatory/boilerplate prose: "the process typically involves understanding the weighting and criteria that the medical college uses to evaluate applicants. Here’s how each factor can contribute to the overall acceptance percentage:" — reads as unedited draft text, not policy.
- Formula: Total weighted score 60% + Interview 40%; *"20% high school + 40% Qudrat + 40% Tahseely were 86 is the minimum acceptable score" (typo "were"→"where").
- Document list embeds thresholds: HS "(95%)"; Qudrat "(80)"; "Standard Achievement Admission Test score report (SAAT – Tahseely) (80) or equivalent (SAT 1) 1300" — Tahseely equivalence given as SAT 1 (=SAT Reasoning, i.e., Qudrat equivalent), and same "SAT 1" listed for Qudrat → internally inconsistent; search-engine snippet of same page previously read "(SAT 2)" → content has been edited without clear control.
- "Complete online application" -> https://www.uap.sa/ (external platform; DIFFERENT channel from all other UG pages which use pmu.edu.sa/apply)
- Fee: "non-refundable application fee of SAR 1000 (incl. VAT)" (vs SAR 950 elsewhere) — medicine-specific fee not reflected on fees pages (to verify).
- NO English-language requirement stated for Medicine.
- No deadlines, seats, tuition for MBBS/MD, or accreditation status stated on this page.
- Page is 2 pages long in a11y tree (very long curriculum content before admission criteria → criteria buried at bottom).

## P10 https://pmu.edu.sa/admission/fees_tf_ro — Undergraduate Fees index (Registration Office section)
- Index of 4 generations live side-by-side: "Medical Program Fees", "Fall Semester 2026/2027", "Fall Semester 2025/2026", "Continuing Students 2024–2025". No "current" label; applicant must infer which applies.
- Fees sit under "Registration Office" breadcrumb, while hub/sidebars link to TWO different entry URLs (Fees_TF_RO.aspx vs Tuition_Fees_RO.aspx).

## P11 https://pmu.edu.sa/admission/fees_tf_ro_2026_2027 — UG Fees 2026/2027 (admitted/readmitted from Fall 2026/27)
- Prep: SAR 30,000 / semester
- CAD, CCES, COE: SAR 32,500 / semester flat for 12–18 credits; >18 at SAR 2,708.3 per credit hour
- COBA, Law: SAR 30,000 / semester flat (12–18); >18 at SAR 2,500.00
- Part-time (≤11 hrs): 2,708.3 / 2,500.00 per credit hour
- VAT: Non-Saudi 15% on tuition and fees; Saudi 15% on fees only (no VAT on tuition)
- No Medicine row (separate page); no College of Sciences & Human Studies row.
- "2,708.3" = unrounded (32,500/12) — presentation issue.

## P12 https://pmu.edu.sa/admission/medical_program_studies_fees_tf_ro — Medical Program Fees (Fall 2026/27)
- **Medical Application Fee: SAR 1,150 (VAT inclusive)** — CONFLICT with P09 "SAR 1000 (incl. VAT)". Screenshot S12 shows 1,150 directly.
- Medical Seat Reservation Fee (part of tuition): SAR 20,000, non-refundable
- Medical Preparatory Program Tuition: SAR 75,000 / year
- Medical Program Tuition: SAR 90,000 / year
- VAT: non-Saudi 15% on tuition and all fees; Saudi 15% on fees only
- Admission page (P09) mentions neither the SAR 20,000 non-refundable seat reservation nor a "Medical Preparatory Program" year — applicant making a SAR 20k commitment cannot see it on the admission page.

## P13 https://pmu.edu.sa/admission/student_fees_tf_ro — Other Fees
- UG application fee: "Non-refundable SAR 950" (includes VAT 15%); Graduate application fee: same SAR 950.
- Medical application fee (SAR 1,150 per P12 / SAR 1,000 per P09) NOT listed here → third surface without medicine.
- **APTIS Exam Fees: SAR 575** listed as optional fee — CONFLICT with P03 "S.R.950 Admission and English Placement Test Fee" (implies placement test included in 950). Applicant cannot tell if Aptis costs extra.
- Late registration SAR 750; late payment SAR 750/installment; returned cheque SAR 2,300; transcript SAR 115; grade appeal SAR 575 (refunded as credit if approved); bus Khobar 5,522 / Dammam 6,003 per semester; daycare monthly 2,300.
- No effective date on this page.

## P14 https://pmu.edu.sa/admission/admission_calendar_fs_ro — Admissions Calendar (viewed 2026-09-27)
- Shows ONLY Fall 2026-2027 (UG + Grad). Classes began 2026-08-30 → on audit date the only calendar published is for an intake already started; no Spring 2027 / Fall 2027 status, no "applications closed/open" banner.
- UG table: "For Saudi Students: Apply online through Qabool platform: https://www.uap.sa/" (2026-05-03); "For non Saudi Students: Apply online through Study in Saudi platform: https://studyinsaudi.sa/ar" (Closed); EPT & interviews start 2026-05-17; last day Freshman/Re-admit apply online 2026-06-24; end of placement/retake 2026-07-05; last day submit IELTS/TOEFL 2026-07-20; last day Transfer docs in person 2026-07-20; first day of classes 2026-08-30; admission results via Qabool July 19–21 2026; orientation TBA.
- Grad table: apply 2026-05-03; interviews 2026-05-17; last day apply 2026-07-16; docs 2026-07-19; end interviews 2026-07-23; results 2026-08-02; classes 2026-08-30.
- Two "Apply Now" buttons → https://pmu.edu.sa/Apply sitting directly beside the instruction that Saudi students must apply via Qabool (uap.sa) → **route conflict on the same page** (screenshot S14).
- Sequencing: results announced Jul 19–21 while IELTS/TOEFL + transfer-document deadline is Jul 20 (results overlap deadlines). Table rows not chronological (classes listed before results).
- Resolves X05 partially: PMU itself states Saudi UG applicants apply via Qabool/uap.sa → the Medicine page link is consistent with the calendar, but INCONSISTENT with P02/P03/P04/hub which route to pmu.edu.sa/apply or Apply_Now_ADS.aspx.

## P15 https://pmu.edu.sa/apply → 302 to https://admissions.pmu.edu.sa/welcome — Applicant portal landing (public view; no login, no interaction)
- "Admission Calendar — No events are currently published. Please check back later." → portal says nothing published while website calendar (P14) publishes Fall 2026-27 dates → **site/portal mismatch**.
- Banner image (Arabic) advertises graduate-studies admission for "الفصل الدراسي الثاني 2026/2025" — year order reversed and refers to a past semester → stale campaign asset (screenshot S15).
- "Student Login" and "New Student? Register!" active — no guidance that Saudi UG applicants must use Qabool (per P14) or non-Saudis Study in Saudi.
- Footer "2022 ©"; "(visit Degrees & Programs webpage)" is plain text, not a link; "Contact Admissions" links back to hub which itself has no contact details.
- English-only landing (no Arabic toggle observed in a11y tree).

## P16 https://pmu.edu.sa/admission/apply_now_ads (legacy Apply_Now_ADS.aspx) — renders same portal landing content as P15 (No events published; Register). So at least 3 distinct "apply" entry points exist: pmu.edu.sa/apply → portal; Apply_Now_ADS → portal content; uap.sa (Qabool) and studyinsaudi.sa per calendar/medicine page.

## P17 https://pmu.edu.sa/admission/admission-from-other-universities — Transfer
- Eligibility: prior institution MoE-recognized; regular (not online/distance); cumulative GPA 2.0/4.0; not dismissed; last course ≤5 years old; meet current PMU criteria; link to Transfer-Student-Admission-and-Credit-Transfer-Policy.aspx.
- Apply link: http://admissions.pmu.edu.sa/ (non-HTTPS; 4th variant of apply link). No mention of Qabool although P14 says Saudi UG apply via Qabool.
- Docs incl. original sealed transcript (English) + all syllabi (English). Fee SAR 950 incl. VAT. Direct entry IELTS 6.0/5.5 "or equivalent TOEFL iBT with acceptable scores" (no number).
- Process: Aptis + interview; credit transfer review "minimum 5 weeks" after acceptance.
- Grammar: "In order to be consider".

## P18 https://pmu.edu.sa/admission/international_students — International Students without Saudi Residence
- "As an international student, you'll begin the application process just like all other applicants. The application process can be completed entirely online." Apply → pmu.edu.sa/apply. **CONFLICT with P14** (non-Saudis apply via Study in Saudi platform; status "Closed").
- Criteria: HS 80%; "Acceptable SAT I" (no threshold); IELTS 6.0/5.5; online interview.
- Lower-% composite: Non-Engineering: Secondary 60% / SAT I 40%. **CS & Engineering: Secondary 40% / SAT I 30% / SAT II 30%** — SAT II (Subject Tests) discontinued 2021 (X06) → requirement impossible to satisfy.
- Docs: certificate certified by Saudi Cultural Mission and Saudi Embassy; "Copy of National ID"; passport. No Iqama/visa-specific documents; visa support mentioned.
- Breadcrumb "International Students' Office" → International_Students_Office.aspx (another page).
- Accordion headings (Transfer, Visitor, Graduate, Tuition, Housing...) are click-only headings (role=heading with click action) — keyboard/semantics risk.

## P19 https://pmu.edu.sa/admission/admissions_requirements_cs_eng_majors — CS & Engineering Majors requirements
- Page title says CS & Engineering but applies also to **Architecture** (listed: Architecture, CS, CE, SE, ME, EE, CivE).
- General: HS ≥80 (60%) + Qudrat ≥60 (40%). Major-specific: **HS ≥85 (40%) + Qudrat ≥65 (30%) + Tahseely ≥65 (30%)**.
- "*Students with lower marks may apply, however, the minimum weighted total, defined by the Admissions Office, should be met." → the decisive cut-off is not published.
- Tahseely equivalent: "SAT 1 (1200)" — vs Medicine page "SAT 1 1300" (P09) and International "SAT II 30%" (P18). Three different equivalence statements for the same Tahseely component.
- SAT Math ≥400 may waive Prep math courses ("wave" typo) → link to sat-admission.
- Apply link http://admissions.pmu.edu.sa (http); several http:// links.
- Step IV/V duplicated/confusing ("if available ... or ... For direct entry ...").
- Freshman page (P03) omits Tahseely entirely and gives 30/50/20 formula; UG home/direct (P02/P04) 60/40; International CS/Eng 40/30/30 with SAT II; Medicine 20/40/40 then 60/40 with interview → **five distinct published weighting schemes**.

## P20 https://www.pmu.edu.sa/admission/admission_procedures_criteria_fs_ro — Admission Procedures & Criteria (NOT in hub navigation; reachable, indexed by search)
- Legacy-generation criteria page still public. Categories incl. "Two Year College Graduates", "Part Time Students".
- Fresh students: fee SR 950 (non refundable; no VAT mention); GPA ≥80% — "**Students with a lower GPA, 70% as a minimum, can apply but acceptance depends on the interview results**" (a 70% floor appears nowhere else); GAT ≥60%; "Successful Interview and **PMU Standard Battery Test**" (test not mentioned elsewhere; current placement is Aptis).
- Transfer: GPA 2.0; "**TOEFL or IELTS of 550** or PMU Math and English Placement Test" — IELTS has no 550 score (band 0–9); 550 is a retired TOEFL PBT figure → factually wrong for IELTS and conflicts with P06/P07/P17.
- Links "PMU PLACEMENT TEST – SAMPLE" PDF/Viewer.aspx?ID=202.
- Breadcrumb lacks Home; side menu shows only "Future Students".
- Screenshot S20 (page identity + headings).

## P21 https://www.pmu.edu.sa/academics/admission_registration_dp — "Admission & Registration" (Diploma Program, Deanship of Business Development & Community Service)
- Title "Admission & Registration" (same label as admissions) but content = Arabic, undated announcement that PMU "intends to offer" (نيتها لطرح) diploma programs with a social charity fund; eligibility incl. Saudi nationality, HS ≤5 years, guardian income < SAR 8,000/month.
- Undated, "intention" wording → likely legacy campaign still public under an admissions-like title; appears in search for "القبول والتسجيل". Publishes named individual staff phone/email (personal contacts rather than role mailboxes). [Names deliberately not reproduced in audit outputs.]
- Only Arabic-language admissions-type content found in the crawl → illustrates parity gap (Arabic content exists for a legacy diploma, not for the main admissions rules).

## P22 https://www.pmu.edu.sa/ — Homepage (viewport only)
- Header shows search, main nav, SIGN IN; **no Arabic/English language switch visible** in the header (S22). Same header on every admissions page crawled (P01–P20): no language switch in any a11y tree.
- Tiles: "UNDERGRADUATE PROGRAMS", "GRADUATE PROGRAMS", "APPLY TO PMU"; chat widget "May I Help You!".
- Arabic parity conclusion (bounded): no Arabic equivalents of the admissions rule pages were found via navigation or search (search for Arabic admissions terms returned only Arabic news items and a legacy MOHE PDF). Not asserted that no Arabic site exists anywhere; asserted that the applicant-facing admissions rules are published in English only on the surfaces reviewed.
