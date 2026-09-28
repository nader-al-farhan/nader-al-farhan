# Content audit — the 36 links on the live Admissions Office page (2026-09-28)

**Scope:** what each target page *says* — data, rules, numbers, dates, and their accuracy, consistency and completeness. Technical issues (redirects, `lang`, alt text) are out of scope; they are covered in `../` (link audit).

| File | What it is |
|---|---|
| `PMU-Admissions-Content-Audit.html` | Report (Arabic). One card per link, with its purpose, key data and observations. Each observation shows the verbatim quote and a highlighted evidence screenshot (click the screenshot for full size). Also contains the cross-page matrix and the mapping of the 36 links onto the 17 proposed pages. |
| `CONTENT-AUDIT-2026-09-28.md` | The same content as Markdown |
| `content-audit-2026-09-28.json` | The same content as data |
| `report_en/PMU-Admissions-Content-Audit-EN.pdf` / `.docx` | **English formal report** (A4, 66 pages): cover, document control, contents, executive summary with the decisions required, method, results, cross-page matrix, the new register findings F-31–F-45, a link-by-link review, the mapping to the 17 proposed pages, recommendations, corrections, and appendices (70 evidence figures, glossary, sources, reproducibility). Built by `export_en.py` → `report_en/build_docx.js` → `report_en/to_pdf.py` (LibreOffice, with the table of contents updated). |
| `content_findings_en.py` | English text for every observation (kept aligned with `content_findings.py`; the build fails if they diverge) |
| `content_findings.py` | The observations: the single source edited by hand |
| `texts.json`, `text/Cxx.txt` | Live main-content text of each page, with collapsed sections opened locally |
| `shots/Cxx-n.jpg` | The page region with the quoted text highlighted: red = high, orange = medium, blue = low |

## Result
- **80 observations:** 15 high, 39 medium, 26 low.
- **31 were new.** With the owner's approval on 2026-09-28 they were added to the findings register, consolidated into **F-31 to F-45** (15 findings). The MSHD empty "Work Experience" heading joined F-26. The register now has 45 findings.
- **The rest confirm or extend existing findings:** F-02, F-03, F-04, F-05, F-07, F-08, F-09, F-10, F-11, F-13, F-15, F-17, F-20, F-21, F-23, F-25, F-26, F-27 and F-28.
- **91 quotes, all checked automatically:** `build_content.py` fails if any quote is not verbatim in the live text.
- **New high-severity items:**
  - The application fee for international transfer and visiting students is SAR 500 excl. VAT (C07), while C27 and C28 give SAR 950 incl. VAT for the same applicants.
  - MA IBL claims 2 years full-time at a maximum of 6 credits per semester, for a programme of 36 credits.
- **Correction:** F-26 was not reproduced for 5 of its pages. It is logged in the register's self-correction log and its scope is narrowed.

## Re-run
```
NODE_PATH=$(npm root -g) node content/extract_text.js    # from ../ ; writes texts.json + text/
python3 content/make_jobs.py
NODE_PATH=$(npm root -g) node content/shots_content.js
cd content && python3 build_content.py
```

## Limits
- **C04** (staff list): its text was not copied because it contains personal names.
- **C06 and C08** (the portal): a JavaScript app that does not render this way.
- **C07 bank details:** C07 has bank payment details in hidden page code. They are not reproduced in any file.
- **Not verified:** the ETS code (6993) and the College Board code (7647).
- **AACSB:** the claim is checked only against AACSB's own statement that it accredits schools, and that fewer than 6% of business schools hold it (https://www.aacsb.edu/educators/accreditation/value-of-accreditation). PMU's own accreditation status was not verified.
