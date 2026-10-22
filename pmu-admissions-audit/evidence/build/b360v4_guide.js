// Internal submission guide (DOCX). Usage: node b360v4_guide.js data.json out.docx
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, HeadingLevel, BorderStyle, ShadingType } = require('docx');
const D = JSON.parse(fs.readFileSync(process.argv[2])); const OUT = process.argv[3];
const S = D.stats, C = D.coverage22; const am = {}; D.amend.forEach(a => am[a.code] = (am[a.code] || 0) + 1);
const pl = k => S.plevel[k] || 0;
const NAVY = '1F3864';
const r = (t, o = {}) => new TextRun({ text: t, font: o.ar ? 'Arial' : 'Arial', size: o.size || 20, bold: o.bold, color: o.color, rightToLeft: !!o.ar });
const P = (t, o = {}) => new Paragraph({ children: Array.isArray(t) ? t : [r(t, o)], bidirectional: !!o.ar, alignment: o.ar ? AlignmentType.RIGHT : AlignmentType.LEFT, spacing: { after: 100 } });
const H = (t, o = {}) => new Paragraph({ children: [r(t, { bold: true, size: o.size || 26, color: NAVY, ar: o.ar })], bidirectional: !!o.ar, alignment: o.ar ? AlignmentType.RIGHT : AlignmentType.LEFT, spacing: { before: 240, after: 120 } });
const B = (t, o = {}) => new Paragraph({ children: [r('• ' + t, o)], bidirectional: !!o.ar, alignment: o.ar ? AlignmentType.RIGHT : AlignmentType.LEFT, spacing: { after: 60 }, indent: o.ar ? { right: 300 } : { left: 300 } });
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF' };
const cell = (t, w, head) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd },
  shading: head ? { type: ShadingType.CLEAR, color: 'auto', fill: NAVY } : undefined, margins: { top: 60, bottom: 60, left: 90, right: 90 },
  children: [new Paragraph({ children: [r(String(t), { size: 17, bold: head, color: head ? 'FFFFFF' : undefined })] })] });
const table = (rows, widths) => new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
  rows: rows.map((row, i) => new TableRow({ tableHeader: i === 0, children: row.map((c, j) => cell(c, widths[j], i === 0)) })) });
const files = [
  ['Order', 'File', 'Status', 'Purpose', 'Audience'],
  ['1', '01_PMU_Admissions_Management_Review_AR.pdf', 'Essential', 'Management Review & Decision Package (Arabic)', 'Mr. Radhi Alkhaldi; leadership'],
  ['2', '03_PMU_Admissions_Management_Review_EN.pdf', 'Essential', 'Mirror English edition', 'Same'],
  ['3', '04_PMU_Admissions_Master_Register_EN.xlsx', 'Essential', 'Findings, evidence, decisions, actions, QC (English, LTR)', 'Mr. Radhi; owners'],
  ['4', '02_PMU_Admissions_Master_Register_AR.xlsx', 'Supporting', 'Arabic edition of the register (RTL)', 'Arabic readers; implementing team'],
  ['5', '05_PMU_Admissions_Evidence_Pack.zip', 'Supporting (internal / on request)', 'Original and annotated evidence, PDFs, references, QA records', 'Implementing team; verification'],
  ['—', '00_INTERNAL_Submission_Guide.docx', 'Internal — do not attach', 'This guide and the email text', 'Preparer'],
];
const email = [
  'Subject: RE: comments on Admission pages', '', 'Dear Mr. Radhi,', '',
  'Further to my email of 26 October 2025 in this thread, and as requested, I have completed an independent review of the published content of the Admissions Office webpage. The Management Review & Decision Package is attached for your review and direction.', '',
  `Scope: the five sections of the page, their ${C.unique_destinations} direct destinations, the shared admissions menu, two linked PDF guides and nine official pages used for verification. The scope was rediscovered and every finding re-verified on the live site on 22 October 2026 (${C.eligible} eligible resources; ${C.fully} fully and ${C.partially} partially reviewed; ${C.discovered_unique_urls} unique links; ${C.pdf_pages} PDF pages). The review was read-only.`, '',
  `Results: ${S.n} findings (${pl('P0')} P0, ${pl('P1')} P1, ${pl('P2')} P2, ${pl('P3')} P3), including ${S.conflicts} proven conflicts between published statements, and ${D.verified_correct.length} verified strengths. The highest-priority conflicts concern application fees: SAR 500 (excl. VAT) versus SAR 950 (incl. VAT) for international transfer and visiting applicants, and SAR 1,000 versus SAR 1,150 for the College of Medicine. High-priority issues also include the absence of a current admission cycle, the discontinued SAT II test in the international weighting, conflicting graduate English thresholds, and another university’s text on the Engineering Management requirements page.`, '',
  `Of the six amendments requested on 26 October 2025, ${am.NOT_PUBLISHED || 0} are not published and ${am.PARTIALLY_PUBLISHED || 0} are partially published.`, '',
  'Decisions: the package sets out ten decisions (D-01 to D-10). Five fall within the Admissions Office’s remit and can be directed now (interim cycle notice, withdrawal of the 2018 guide, official contact details, content ownership and 48 editorial corrections). Fees, admission and English-language requirements and the programme list are presented for referral to the competent authorities. A corrective action roadmap (A-01 to A-13) sets out approvals and verification steps; target dates are proposals only.', '',
  'Limitations: no approved, dated policy or fee decision was available, so conflicting values are reported as open conflicts and were not resolved by assumption; two items could not be verified from published content and are recorded for manual checking.', '',
  'Status: Management Package — READY FOR MANAGEMENT REVIEW; Overall Closure — NOT READY FOR VERIFIED CLOSURE.', '',
  'Attachments: (1) Management Review & Decision Package — Arabic and English; (2) Master Register. The Evidence Pack is available on request.', '',
  'I would be grateful for your direction to the competent units on the pending matters, the confirmation of governing references, and the assignment of corrective and follow-up actions.', '',
  'Kind regards,', 'Nader Al Farhan', 'Administrative Assistant, Student Affairs, Admission Office', 'Prince Mohammad Bin Fahd University (PMU)'];
const emailAr = [
  'سعادة الأستاذ راضي الخالدي المحترم،', '',
  'إلحاقًا برسالتي المؤرخة في 26 أكتوبر 2025 في هذه السلسلة، وبناءً على طلب سعادتكم، أكملتُ مراجعة مستقلة للمحتوى المنشور لصفحة مكتب القبول، وأرفق حزمة المراجعة والقرارات الإدارية لاطلاعكم وتوجيهكم.',
  `النطاق: الأقسام الخمسة ووجهاتها المباشرة الـ${C.unique_destinations} والقائمة المشتركة ودليلا PDF وتسع صفحات رسمية للتحقق؛ وأُعيد اكتشاف النطاق والتحقق من كل الملاحظات حيًا في 22 أكتوبر 2026.`,
  `النتائج: ${S.n} ملاحظة (${pl('P0')} من P0 و${pl('P1')} من P1 و${pl('P2')} من P2 و${pl('P3')} من P3)، منها ${S.conflicts} تعارضات منشورة مثبتة، و${D.verified_correct.length} نقاط قوة. وأعلاها تعارض رسوم التقديم للمحولين والزائرين الدوليين ولكلية الطب.`,
  `التعديلات السابقة: ${am.NOT_PUBLISHED || 0} غير منشورة و${am.PARTIALLY_PUBLISHED || 0} منشورة جزئيًا.`,
  'القرارات: عشرة قرارات؛ خمسة ضمن صلاحية مكتب القبول يمكن توجيهها الآن، والبقية للإحالة إلى الجهات المختصة.',
  'الحالة: الحزمة جاهزة للمراجعة الإدارية؛ والإغلاق غير جاهز للتحقق النهائي.', '',
  'وتفضلوا بقبول فائق الاحترام والتقدير،', 'نادر آل فرحان', 'مساعد إداري، شؤون الطلاب، مكتب القبول'];
const children = [
  new Paragraph({ children: [r('INTERNAL — NOT FOR ATTACHMENT', { bold: true, color: '9C0006', size: 18 })] }),
  new Paragraph({ children: [r('PMU Admissions — Submission Guide', { bold: true, size: 34, color: NAVY })], spacing: { after: 60 } }),
  P('Reference PMU-ADM-360-MASTER-20261022 · Version 4.0 · 22 October 2026 · Prepared by Nader Al Farhan, Administrative Assistant, Student Affairs, Admission Office'),
  H('1. Thread'),
  B('Reply All to the latest message in “RE: comments on Admission pages” (Ms. Rawan Al Qahtani → Mr. Radhi, 17 Feb 2026, 3:40 PM). Your reply of 26 Oct 2025 is already quoted in this thread.'),
  B('To: Mr. Radhi Alkhaldi. Cc: keep the existing recipients; add no one new. Subject: unchanged.'),
  B('The way the request was made stays internal; the email says only “as requested”.'),
  H('2. Attachments and presentation order'), table(files, [700, 3300, 1600, 2700, 1800]),
  H('3. Required from you before sending'),
  B('Confirm the VAT basis of the SAR 950 fee (your 26 Oct 2025 request said “excl. VAT”; the official schedule says “includes the VAT 15%”) — D-01 / H-3.'),
  B('Clarify the scope of request H-4: remove SAT 2 only, or Tahseely as well.'),
  B('Provide any approved, dated reference you hold (fee schedule, admission criteria, graduate requirements, next-cycle dates); otherwise the items remain OPEN CONFLICT / ESCALATION REQUIRED.'),
  B('Optional: open http://admissions.pmu.edu.sa/ from an ordinary browser (F-131) and view the four portal registration labels without entering data (F-033).'),
  B('Confirm Cc list and signature; send the email yourself. Nothing has been sent.'),
  H('4. Email draft (English)'), ...email.map(t => P(t)),
  H('5. النص العربي المرجعي', { ar: true }), ...emailAr.map(t => P(t, { ar: true })),
  H('6. Status'), P('Management Package: READY FOR MANAGEMENT REVIEW · Overall Closure: NOT READY FOR VERIFIED CLOSURE. VERIFIED-OUTCOME-CLOSED is used only after decision, approval, implementation, publication, read-back, verification, regression and acceptance.'),
];
const doc = new Document({ creator: 'Nader Al Farhan', lastModifiedBy: 'Nader Al Farhan', title: 'PMU Admissions — Submission Guide (internal)', description: 'Internal submission guide',
  styles: { default: { document: { run: { font: 'Arial', size: 20 } } } },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1000, left: 900, right: 900 } } }, children }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('docx ok', OUT); });
