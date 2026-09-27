"""Build the Admissions Canonical Record (seed) from audit evidence.

Every record lists what PMU currently publishes (with source page IDs from
evidence/field-notes.md) and the decision needed. `approved_value` stays
null until the owning body signs the matching decision pack in ../decisions/.
Run:  python3 build_canonical.py   -> admissions-canonical.json + admissions-canonical.md
"""
import json
import pathlib

VERIFIED = "2026-09-27"

R = []


def rec(rid, label_en, label_ar, owner, decision, status, published, approved=None, note=""):
    R.append({
        "id": rid,
        "label": {"en": label_en, "ar": label_ar},
        "owner_role": owner,
        "decision_ref": decision,
        "status": status,  # conflict | gap | consistent | consistent-needs-label
        "published_values": [
            {"value": v, "sources": s} for v, s in published
        ],
        "approved_value": approved,
        "effective_intake": None,
        "last_verified": VERIFIED,
        "note": note,
    })


rec("hs_gpa_min", "Minimum secondary-school GPA", "الحد الأدنى لمعدل الثانوية",
    "Admissions Committee", "D1", "conflict", [
        ("80% (general)", ["P02", "P04", "P18", "P19", "P20"]),
        ("85% (CS/Eng/Architecture major-specific)", ["P19"]),
        ("95% (Medicine, stated in document list)", ["P09"]),
        ("70% floor, interview-dependent (legacy)", ["P20"]),
    ], note="Category-specific values may be legitimate; the 70% legacy floor is not stated anywhere else.")

rec("gat_min", "Minimum General Aptitude (Qudrat)", "الحد الأدنى لاختبار القدرات",
    "Admissions Committee", "D1", "conflict", [
        ("60%", ["P02", "P04", "P19", "P20"]),
        ("65% (major-specific)", ["P19"]),
        ("80 (Medicine)", ["P09"]),
        ("'Recent score' only, no minimum", ["P03"]),
    ])

rec("tahseely_rule", "Tahseely requirement and SAT equivalence", "اشتراط التحصيلي ومكافئ SAT",
    "Admissions Committee", "D3", "conflict", [
        ("Tahseely >= 65 or SAT 1 (1200)", ["P19"]),
        ("Tahseely 80 or SAT 1 1300 (Medicine)", ["P09"]),
        ("SAT >= 1200 instead of Qudrat AND Tahseely", ["P28"]),
        ("SAT II 30% (discontinued 2021, X06)", ["P18"]),
        ("Not mentioned", ["P03"]),
    ])

rec("composite_formula", "Weighted admission formula", "المعادلة الموزونة",
    "Admissions Committee -> Academic Council", "D1", "conflict", [
        ("HS 60% + GAT 40%", ["P02", "P04", "P18 (SAT I)", "P19 general", "P25"]),
        ("HS 30% + GAT 50% + Interview 20%", ["P03"]),
        ("HS 40% + GAT 30% + Tahseely 30%", ["P19 major-specific"]),
        ("HS 40% + SAT I 30% + SAT II 30%", ["P18 CS/Eng"]),
        ("(HS 20% + GAT 40% + Tahseely 40%) x 60% + Interview 40%", ["P09"]),
        ("Interview-based acceptance below 80%", ["P20"]),
    ], note="Same-category conflict: general freshman 60/40 vs 30/50/20 vs P20.")

rec("composite_minimum", "Minimum composite score", "الحد الأدنى المركّب",
    "Admissions Committee", "D1/D10", "conflict", [
        ("86 (Medicine) - unreachable at published minimums: 0.2x95+0.4x80+0.4x80 = 83", ["P09"]),
        ("'defined by the Admissions Office' (unpublished)", ["P19"]),
    ])

rec("english_ug_direct", "UG direct-entry English threshold", "حد الإنجليزية للقبول المباشر",
    "English/Prep Program Director -> Admissions Committee", "D2", "conflict", [
        ("IELTS Academic 6.0 overall / 5.5 writing", ["P04", "P06", "P17", "P18", "P19", "P27", "P53"]),
        ("IELTS 5.5 overall / 5.5 writing", ["P03"]),
        ("TOEFL iBT 83 / writing 19", ["P07", "P53"]),
        ("TOEFL iBT 65 / PBT 513 / CBT 183", ["P03"]),
        ("'TOEFL or IELTS of 550' (invalid for IELTS)", ["P20"]),
    ], note="TOEFL moved to a 1-6 scale on 21 Jan 2026 (X01); CBT retired 2006 (X02).")

rec("english_grad", "Graduate English threshold", "حد الإنجليزية للدراسات العليا",
    "Graduate Studies -> Admissions Committee", "D2", "conflict", [
        ("IELTS 6.0 overall & 5.5 each skill / TOEFL iBT 83 & 19 each", ["P34", "P35", "P36", "P37", "P38", "P39", "P40", "P41", "P42"]),
        ("IELTS 7 (no band < 6) / TOEFL 79 / PTE 60 / 'UA CESL' endorsement", ["P43"]),
    ], note="P43 contains University of Arizona text (X09).")

rec("test_validity", "English test validity", "صلاحية اختبار اللغة",
    "English/Prep Program Director", "D2", "conflict", [
        ("'less than two years old'", ["P03"]),
        ("'two years from test date to commencement of applied semester'", ["P06", "P07"]),
        ("'within 2 years of enrollment term'", ["P43"]),
    ])

rec("application_fee", "Application fee", "رسم التقديم",
    "Finance", "D5", "conflict", [
        ("SAR 950 incl. VAT (UG and graduate)", ["P02", "P04", "P13", "P17", "P19", "P25", "P27"]),
        ("SR 950 'Admission and English Placement Test Fee' (no VAT)", ["P03"]),
        ("SR 950 non refundable (no VAT)", ["P20"]),
        ("SAR 1000 incl. VAT (Medicine)", ["P09"]),
        ("SAR 1,150 VAT inclusive (Medicine)", ["P12"]),
    ])

rec("placement_fee", "Placement (Aptis) test fee", "رسم اختبار تحديد المستوى",
    "Finance", "D5", "conflict", [
        ("Included in SR 950", ["P03"]),
        ("APTIS Exam Fees SAR 575", ["P13"]),
    ])

rec("refund_policy", "Tuition refund and seat reservation", "استرداد الرسوم وحجز المقعد",
    "Finance + Legal", "D9", "conflict", [
        ("'All tuition payments are non-refundable.'", ["P49"]),
        ("Deductions 25% / 50% / 75% by timing", ["P49"]),
        ("Partial refund per acceptance-letter terms (unpublished)", ["P50"]),
        ("Medicine seat reservation SAR 20,000 non-refundable", ["P12"]),
    ])

rec("tuition_ug", "UG tuition (new intake)", "الرسوم الدراسية للبكالوريوس",
    "Finance", "-", "consistent-needs-label", [
        ("2026/27: SAR 30,000/sem (COBA, Law, Prep); SAR 32,500/sem (CAD, CCES, COE); 12-18 hrs flat", ["P11", "P49 (undated)"]),
        ("2025/26 intake: SAR 29,000 all / 32,500 AI & Cyber", ["P46"]),
        ("Continuing (pre-2025/26): 29,000 / 32,500, 12+ hrs", ["P47"]),
    ], approved="2026/27 schedule as published on P11 (label as current; label P46/P47 as previous/continuing)")

rec("tuition_medicine", "Medicine tuition and duration", "رسوم ومدة برنامج الطب",
    "Dean, College of Medicine + Finance", "D10", "conflict", [
        ("7-year hybrid model", ["P09"]),
        ("6-year integrated curriculum (UIC collaboration)", ["P54"]),
        ("Medical Prep SAR 75,000/yr + Medical Program SAR 90,000/yr", ["P12"]),
    ])

rec("vat_statement", "VAT treatment", "بيان ضريبة القيمة المضافة",
    "Finance", "-", "consistent", [
        ("Non-Saudi: 15% on tuition and fees; Saudi: 15% on fees only", ["P11", "P12", "P45", "P46", "P49", "P51"]),
    ], approved="As published (consistent with ZATCA, X07)")

rec("application_channel", "Application channel per applicant type", "قناة التقديم لكل فئة",
    "Executive Sponsor + Admissions Director", "D4", "conflict", [
        ("Saudi UG -> Qabool (uap.sa); non-Saudi -> Study in Saudi (Closed)", ["P14"]),
        ("Everyone -> pmu.edu.sa/apply -> admissions.pmu.edu.sa", ["P02", "P04", "P18", "P53"]),
        ("http://admissions.pmu.edu.sa", ["P17", "P19"]),
        ("Apply_Now_ADS.aspx", ["P03", "sidebars"]),
        ("uap.sa (Medicine)", ["P09"]),
    ])

rec("required_documents", "Required documents per applicant type", "الوثائق المطلوبة لكل فئة",
    "Admissions Director", "OPS-1", "conflict", [
        ("Original certificate; Saudi ID or Iqama", ["P03"]),
        ("Copy of certificate; Saudi ID only", ["P04", "P19"]),
        ("Certificate certified by Saudi Cultural Mission and Embassy; National ID", ["P18"]),
        ("Embassy stamp + MoE equivalency", ["P53", "P02"]),
    ])

rec("intake_status", "Intake calendar and status", "تقويم الدورة وحالتها",
    "Admissions Director + IT (portal)", "OPS-2", "conflict", [
        ("Fall 2026-27 only (classes began 2026-08-30)", ["P14"]),
        ("'No events are currently published'", ["P15"]),
        ("Footer: 2021-22; Study at PMU hub: 2023-24", ["P32", "P56"]),
    ])

rec("contacts", "Admissions contact points", "جهات تواصل القبول",
    "Admissions Director", "OPS-3", "gap", [
        ("enrollment@pmu.edu.sa (Contact Us; 2018 guide)", ["P64", "P55"]),
        ("graduateadm@pmu.edu.sa (graduate)", ["P30"]),
        ("UG sidebars -> graduate contact page", ["P04", "P17", "P19"]),
        ("financal_aid@ vs financial_aid@", ["P64", "P66"]),
    ])

rec("programme_register", "Programmes open for admission", "البرامج المتاحة للقبول",
    "Vice President for Academic Affairs", "OPS-4", "conflict", [
        ("Degrees & Programs: no Medicine, no EMGMS, no Eng. ISE, no Pre-Master M.Ed.", ["P61"]),
        ("List of Majors: includes EMGMS and 'MS' Eng. ISE; no Medicine", ["P60"]),
        ("Graduate fees: prices 'Master of Engineering' ISE and Pre-Master M.Ed.", ["P45"]),
    ])

out = pathlib.Path(__file__).parent
(out / "admissions-canonical.json").write_text(json.dumps(R, ensure_ascii=False, indent=2))

md = ["# Admissions Canonical Record — seed (generated)", "",
      f"Verified {VERIFIED}. `approved_value` fills only after the decision in the Decision column is signed.", "",
      "| ID | Rule (EN / AR) | Owner | Decision | Status | Published values (sources) | Approved value |",
      "|---|---|---|---|---|---|---|"]
for r in R:
    pv = "<br>".join(f"{p['value']} ({', '.join(p['sources'])})" for p in r["published_values"])
    md.append(f"| `{r['id']}` | {r['label']['en']} / {r['label']['ar']} | {r['owner_role']} | {r['decision_ref']} | {r['status']} | {pv} | {r['approved_value'] or '— pending —'} |")
counts = {}
for r in R:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
md += ["", "**Status counts:** " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))]
(out / "admissions-canonical.md").write_text("\n".join(md) + "\n")
print(len(R), "records", counts)
