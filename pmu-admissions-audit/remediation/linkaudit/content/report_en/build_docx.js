// Builds the English Word report from ../report-en-data.json (exported by ../export_en.py).
// Run: NODE_PATH=<dir with the "docx" package> node build_docx.js
const fs = require("fs");
const path = require("path");
const {
  TabStopType, Tab, Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, HeadingLevel, BorderStyle, PageBreak, Footer, Header, PageNumber, TableOfContents,
  LevelFormat, PositionalTab, PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
  VerticalAlign, TableLayoutType, ExternalHyperlink, Bookmark, InternalHyperlink,
} = require("docx");

const HERE = __dirname;
const D = JSON.parse(fs.readFileSync(path.join(HERE, "../report-en-data.json"), "utf8"));
const LINKAUDIT = path.join(HERE, "../..");
const OUT = path.join(HERE, "PMU-Admissions-Content-Audit-EN.docx");

// ---------- design tokens ----------
const FONT = "Arial";
const NAVY = "16325C", INK = "1F2433", MUTED = "5B6275", LINE = "C9D0DD", PALE = "F2F4F8", PALE2 = "E8ECF4";
const SEV = { H: { t: "High", c: "B3261E", f: "FBE9E7" }, M: { t: "Medium", c: "A15C00", f: "FFF4E0" }, L: { t: "Low", c: "2F5E9E", f: "E8F0FB" } };
const W = 9638; // A4 content width in DXA (11906 − 2 × 1134)

// ---------- helpers ----------
const r = (text, o = {}) => new TextRun({ text, font: FONT, ...o });
const P = (children, o = {}) => new Paragraph({ children: (Array.isArray(children) ? children : [children]).map(c => typeof c === "string" ? r(c) : c), spacing: { after: 120, line: 276 }, ...o });
const H1 = (t, id) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [id ? new Bookmark({ id, children: [r(t)] }) : r(t)] });
const H1b = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [r(t)] });
const H2 = (t, o = {}) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [r(t)], ...o });
const H3 = (t, o = {}) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [r(t)], keepNext: true, ...o });
const bullet = (children, level = 0) => new Paragraph({ numbering: { reference: "bul", level }, spacing: { after: 60, line: 264 }, children: (Array.isArray(children) ? children : [children]).map(c => typeof c === "string" ? r(c) : c) });
const numbered = (children, ref = "num") => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80, line: 264 }, children: (Array.isArray(children) ? children : [children]).map(c => typeof c === "string" ? r(c) : c) });
const hasArabic = s => /[؀-ۿ]/.test(s);
const border = (c = LINE, sz = 4) => ({ style: BorderStyle.SINGLE, size: sz, color: c });
const cellBorders = { top: border(), bottom: border(), left: border(), right: border() };
const noBorders = { top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" } };

function cell(content, width, o = {}) {
  const kids = (Array.isArray(content) ? content : [content]).map(c =>
    c instanceof Paragraph || c instanceof Table ? c : new Paragraph({ keepNext: o.keepNext, children: [typeof c === "string" ? r(c, { size: o.size || 18, bold: o.bold, color: o.color }) : c], spacing: { after: 40, line: 252 }, alignment: o.align }));
  return new TableCell({
    children: kids, width: { size: width, type: WidthType.DXA }, borders: o.borders || cellBorders,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 70, bottom: 70, left: 110, right: 110 }, verticalAlign: o.valign || VerticalAlign.TOP, columnSpan: o.span,
  });
}
function keepTogether(tbl) { return tbl; }
function table(widths, header, rows, o = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  const trs = [];
  if (header) trs.push(new TableRow({ tableHeader: true, cantSplit: true, children: header.map((h, i) => cell(h, widths[i], { fill: NAVY, bold: true, color: "FFFFFF", size: 17 })) }));
  rows.forEach((row, ri) => trs.push(new TableRow({ cantSplit: o.cantSplit !== false, children: row.map((c, i) => c instanceof TableCell ? c : cell(c, widths[i], { fill: o.zebra !== false && ri % 2 ? PALE : undefined, size: o.size, keepNext: o.keep && ri < rows.length - 1 })) })));
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, rows: trs, layout: TableLayoutType.FIXED });
}
const sevRun = (s, size = 16) => r(` ${SEV[s].t.toUpperCase()} `, { bold: true, color: "FFFFFF", size, shading: { type: ShadingType.CLEAR, fill: SEV[s].c, color: "auto" } });
const tag = (t, size = 16) => r(` ${t} `, { size, color: NAVY, bold: true, shading: { type: ShadingType.CLEAR, fill: PALE2, color: "auto" } });
const quoteP = (q0) => { const q = q0.replace(/\t/g, "  |  "); return new Paragraph({
  children: [r(q, { italics: !hasArabic(q), size: 18, color: INK, rightToLeft: hasArabic(q) && /^[؀-ۿ]/.test(q) })],
  bidirectional: /^[؀-ۿ]/.test(q), indent: { left: 280, right: 200 }, spacing: { before: 40, after: 80, line: 252 },
  shading: { type: ShadingType.CLEAR, fill: PALE, color: "auto" }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: "9AA3B5", space: 8 } },
}); };
const kv = (k, v) => P([r(`${k} `, { bold: true, size: 19 }), ...(Array.isArray(v) ? v : [r(v, { size: 19 })])], { spacing: { after: 70, line: 264 } });
const link = (text, url, size = 18) => new ExternalHyperlink({ link: url, children: [r(text, { style: "Hyperlink", size })] });
const S = D.summary;
const allObs = D.links.flatMap(l => l.obs.map(o => ({ ...o, link: l })));

// ---------- cover ----------
const cover = [
  new Paragraph({ spacing: { before: 1800, after: 120 }, children: [r("PRINCE MOHAMMAD BIN FAHD UNIVERSITY · ADMISSIONS OFFICE", { size: 18, color: MUTED, bold: true, characterSpacing: 20 })] }),
  new Paragraph({ spacing: { after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 24, color: NAVY, space: 12 } }, children: [r("Content Audit of the Admissions Office Web Pages", { size: 52, bold: true, color: NAVY })] }),
  new Paragraph({ spacing: { after: 600 }, children: [r("An independent, evidence-based review of the information published behind the 36 links of pmu.edu.sa/admission/admission", { size: 26, color: INK })] }),
  table([2600, 7038], null, [
    [cell("Prepared for", 2600, { bold: true, fill: PALE }), cell("Associate Director for Enrollment, Admissions Office", 7038)],
    [cell("Scope", 2600, { bold: true, fill: PALE }), cell("Content only — data, rules, figures, dates and their accuracy, consistency and completeness", 7038)],
    [cell("Evidence date", 2600, { bold: true, fill: PALE }), cell("28 September 2026 (live pages, read-only)", 7038)],
    [cell("Version", 2600, { bold: true, fill: PALE }), cell("1.0", 7038)],
    [cell("Classification", 2600, { bold: true, fill: PALE }), cell("Internal — for discussion", 7038)],
  ], { zebra: false }),
  new Paragraph({ spacing: { before: 900 }, children: [r("Independent review. This document is not an official publication of Prince Mohammad Bin Fahd University and does not state University policy. Where published values conflict, it does not choose the correct value; each such case is referred to its decision owner.", { size: 17, color: MUTED, italics: true })] }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- document control + TOC ----------
const control = [
  H1b("Document Control"),
  table([2600, 7038], null, [
    ["Title", "Content Audit of the Admissions Office Web Pages"],
    ["Version / date", "1.0 · 28 September 2026"],
    ["Prepared by", "________________________ (audit owner)"],
    ["Reviewed by", "________________________"],
    ["Approved for circulation", "________________________"],
    ["Status", "Draft for discussion with the Associate Director for Enrollment"],
    ["Related records", "Findings Register (45 findings, F-01–F-45) · Arabic interactive report · Link audit · UX / IA Blueprint"],
  ].map(([a, b]) => [cell(a, 2600, { bold: true, fill: PALE }), cell(b, 7038)]), { zebra: false }),
  new Paragraph({ spacing: { before: 360, after: 120 }, children: [r("Revision history", { bold: true, color: NAVY, size: 22 })] }),
  table([1300, 2000, 6338], ["Version", "Date", "Change"], [["1.0", "28 Sep 2026", "First issue. Observations F-31–F-45 added to the Findings Register with the audit owner's approval."]]),
  new Paragraph({ pageBreakBefore: true, spacing: { before: 0, after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 6 } }, children: [r("Contents", { bold: true, color: NAVY, size: 34 })] }),
  new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-2" }),
];

// ---------- 1 executive summary ----------
const hi = allObs.filter(o => o.sev === "H");
const hiRefs = [...new Set(hi.map(o => o.ref))];
const kpi = (n, t) => cell([new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [r(String(n), { bold: true, size: 40, color: NAVY })] }), new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [r(t, { size: 16, color: MUTED })] })], 1927, { fill: PALE, valign: VerticalAlign.CENTER });
const exec = [
  H1("1. Executive Summary"),
  P("This audit reviewed what the Admissions Office website tells applicants. Each of the 36 links on the live Admissions Office page (pmu.edu.sa/admission/admission) was followed, and the full text of every target page was read and compared with the other 35. The review covers content only: admission rules, thresholds, fees, dates, programme information and their consistency. Technical matters (redirects, accessibility, code) are reported separately."),
  new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [1927, 1927, 1928, 1928, 1928], layout: TableLayoutType.FIXED, rows: [new TableRow({ children: [kpi(S.links, "links reviewed"), kpi(S.obs, "content observations"), kpi(S.H, "high severity"), kpi(S.new_findings, "new register findings (F-31–F-45)"), kpi(S.quotes, "verbatim quotes machine-checked")] })] }),
  H2("Key messages", { spacing: { before: 280, after: 100 } }),
  bullet([r("No link is broken, but the information behind the links is not reliable as a whole. ", { bold: true }), r(`${S.obs} content observations were recorded: ${S.H} high, ${S.M} medium and ${S.L} low.`)]),
  bullet([r("The same fact is published with different values. ", { bold: true }), r("Nine data points are contradicted across pages, including the application fee (SAR 950, SAR 1000 and SAR 500 excluding VAT), the application channel, SAT alternatives, the meaning of a 'Very Good' GPA and the list of majors with specific requirements (Section 4).")]),
  bullet([r("The calendar is out of date. ", { bold: true }), r("On the audit date every published date of the Fall 2026–2027 intake had passed, and no page states whether admission is currently open (F-08).")]),
  bullet([r("Several programme pages contain errors of fact or arithmetic. ", { bold: true }), r("The Medicine composite minimum cannot be reached at the published component minimums (F-20); the MA in International Business Law cannot be completed in the stated two years at six credits per semester (F-32); the EMGMS page reproduces another university's requirements (F-21).")]),
  bullet([r("Most issues are governance issues, not editing issues. ", { bold: true }), r("They arise because each page restates rules independently. They will recur unless rules are published from a single approved record, with an owner and an effective date.")]),
  H2("Decisions required", { spacing: { before: 240, after: 100 } }),
  P("Each high-severity observation belongs to a register finding. The following findings need a decision by their owner before the pages can be corrected:", { spacing: { after: 100 } }),
  table([900, 5338, 3400], ["Finding", "Decision required", "Decision owner"], hiRefs.map(ref => {
    const f = D.register[ref];
    return [cell([new Paragraph({ children: [r(ref, { bold: true, size: 18, color: NAVY })] })], 900), f.finding.replace(/\.$/, ""), f.owner];
  })),
  H2("Overall conclusion", { spacing: { before: 240, after: 100 } }),
  P("The Admissions Office pages cannot currently be relied on as a single, consistent statement of admission requirements. The priority is to decide the contested values (fees, channel, thresholds, programme facts) and to publish them once, from an approved record, before the pages are restructured into the proposed 17-page architecture (Section 7). Moving the current text without these decisions would carry the conflicts into the new site."),
];

// ---------- 2 scope & method ----------
const method = [
  H1("2. Scope and Methodology"),
  H2("2.1 Scope"),
  table([4819, 4819], ["In scope", "Out of scope"], [[
    [bullet("The 36 content links on the Admissions Office page and the pages they open"), bullet("Admission rules, thresholds, weights, documents, fees, dates, programme names and facts"), bullet("Consistency between the 36 pages"), bullet("Accuracy against authoritative external sources where a claim can be checked")],
    [bullet("Technical issues: redirects, page code, accessibility (reported in the separate link audit)"), bullet("Pages not linked from the Admissions Office page, except where needed as a comparison"), bullet("The logged-in application portal"), bullet("University policy decisions — the audit identifies conflicts but does not choose values")],
  ].map((c, i) => cell(c, 4819)) ], { zebra: false }),
  H2("2.2 Method", { spacing: { before: 240 } }),
  numbered("Every link on the live page was extracted and numbered C01–C36 in page order."),
  numbered("The main text of each target page was extracted in a browser, with collapsed sections expanded, on 28 September 2026."),
  numbered("Each page was read in full and compared with the other pages on every data point it states."),
  numbered("Each observation records the exact published wording. An automated check confirms that every quotation appears verbatim in the live text; the report cannot be built if one does not. Where a quotation spans the cells of a table, the cells are separated by \u201c | \u201d."),
  numbered("For each quoted observation, the relevant region of the live page was captured with the quoted text highlighted (Appendix A)."),
  numbered("Observations were mapped to the Findings Register. Thirty new observations were consolidated into fifteen new findings (F-31–F-45), and one joined F-26."),
  H2("2.3 Evidence standard", { spacing: { before: 240 } }),
  P("Text in quotation marks is verbatim from the University's live pages. External facts are cited to the issuing body (Appendix C). Where the audit could not verify a statement, it says so. The audit was strictly read-only: no form was submitted, no account was created and no application step was taken."),
  H2("2.4 Severity scale"),
  table([1300, 8338], ["Severity", "Definition"], [
    [cell([new Paragraph({ children: [sevRun("H")] })], 1300), "Materially misleading or contradictory on a decision path: eligibility, money, the application route or programme duration."],
    [cell([new Paragraph({ children: [sevRun("M")] })], 1300), "Inconsistency, gap or ambiguity with an indirect effect on the applicant's decision or file."],
    [cell([new Paragraph({ children: [sevRun("L")] })], 1300), "Quality, wording or completeness issue with limited decision impact."],
  ]),
  H2("2.5 Limitations", { spacing: { before: 240 } }),
  bullet("C04 (Contact Us) opens a staff list with personal names; its text was not reproduced."),
  bullet("C06 and C08 open the application portal, a JavaScript application that was not reviewed in this content audit."),
  bullet("Page code on C07 contains bank payment details that are not displayed; they are referred to but not reproduced."),
  bullet("The ETS (6993) and College Board (7647) institution codes, and the University's own AACSB status, were not verified."),
  bullet("Findings reflect the pages on 28 September 2026 and may change if the pages are edited."),
];

// ---------- 3 results ----------
const groups = [...new Set(D.links.map(l => l.group))];
const gRow = g => { const o = D.links.filter(l => l.group === g).flatMap(l => l.obs); return [g, String(D.links.filter(l => l.group === g).length), ...["H", "M", "L"].map(s => String(o.filter(x => x.sev === s).length)), String(o.length)]; };
const kinds = [...new Set(allObs.map(o => o.kind))];
const refRows = Object.entries(D.register).map(([id, f]) => {
  const os = allObs.filter(o => o.ref === id);
  return [cell([new Paragraph({ children: [r(id, { bold: true, size: 17, color: NAVY })] })], 900), cell(f.finding, 5038, { size: 17 }), cell(f.severity, 1200, { size: 17 }), cell(String(os.length), 900, { size: 17, align: AlignmentType.CENTER }), cell([...new Set(os.map(o => o.link.id))].join(", "), 1600, { size: 16 })];
});
const results = [
  H1("3. Results at a Glance"),
  H2("3.1 Observations by section of the Admissions Office page"),
  table([3638, 1100, 1200, 1300, 1200, 1200], ["Section", "Links", "High", "Medium", "Low", "Total"], [...groups.map(gRow), ["Total", "36", String(S.H), String(S.M), String(S.L), String(S.obs)].map((c, i) => cell(c, [3638, 1100, 1200, 1300, 1200, 1200][i], { bold: true, fill: PALE2 }))]),
  H2("3.2 Observations by type", { spacing: { before: 240 } }),
  table([5638, 4000], ["Type", "Observations"], kinds.map(k => [k, String(allObs.filter(o => o.kind === k).length)])),
  H2("3.3 Findings Register entries evidenced by this audit", { spacing: { before: 240 } }),
  P(`The ${S.obs} observations evidence ${Object.keys(D.register).length} findings of the Findings Register, which now contains ${S.register_total} findings.`),
  table([900, 5038, 1200, 900, 1600], ["ID", "Finding", "Register severity", "Obs.", "Links"], refRows, { zebra: false }),
];

// ---------- 4 matrix ----------
const matrix = [
  H1("4. Cross-page Inconsistencies"),
  P("The same fact is stated with different values on different pages. An applicant who reads two pages cannot tell which value applies. Each row needs one decision and one published value."),
  table([2300, 5838, 1500], ["Data point", "What the pages say", "Severity · Ref."], D.matrix.map(m => [
    cell([new Paragraph({ children: [r(m.topic, { bold: true, size: 18 })] })], 2300),
    cell(m.values.map(([w, v]) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 30 }, children: [r(`${w}: `, { bold: true, size: 17 }), r(v, { size: 17 })] })), 5838),
    cell([new Paragraph({ children: [sevRun(m.sev, 15)] }), new Paragraph({ children: [r(m.ref, { size: 16, color: MUTED })] })], 1500),
  ]), { zebra: false }),
];

// ---------- 5 new findings ----------
const evidenceRef = shots => shots.length ? shots.map(s => "Figure E-" + path.basename(s, ".jpg")).join(", ") : "—";
const newF = [H1("5. New Findings Added to the Register (F-31 to F-45)"),
  P("With the audit owner's approval, the new observations of this audit were added to the Findings Register on 28 September 2026 as fifteen findings. The register text is reproduced below; quotations are verbatim.")];
D.new.forEach(f => {
  const sev = f.severity.startsWith("High") ? "H" : f.severity.startsWith("Medium") ? "M" : "L";
  const shots = allObs.filter(o => o.ref === f.id && o.shot).map(o => o.shot);
  newF.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, keepLines: true, children: [r(`${f.id}  `, { color: NAVY }), r(f.finding.replace(/\.$/, ""), { color: NAVY })] }));
  newF.push(P([sevRun(sev), r("  "), tag(f.type)], { spacing: { after: 100 }, keepNext: true }));
  newF.push(table([2100, 7538], null, [
    ["Where", f.where], ["Published text", f.current], ["Conflicting source / value", f.conflicting], ["Impact on applicants", f.impact],
    ["Recommended treatment", f.treatment], ["Decision owner", f.owner], ["Evidence", evidenceRef(shots)],
  ].map(([a, b], i, arr) => [cell(a, 2100, { bold: true, fill: PALE, size: 17, keepNext: i < arr.length - 1 }), cell(b, 7538, { size: 17, keepNext: i < arr.length - 1 })]), { zebra: false }));
  newF.push(P("", { spacing: { after: 120 } }));
});

// ---------- 6 link by link ----------
const lbl = [H1("6. Link-by-Link Review"),
  P("Each of the 36 links is reviewed below in the order in which it appears on the Admissions Office page. For each link the report gives the page's purpose, the key facts it states, its destination in the proposed architecture, and every content observation with the verbatim wording, the recommended action and a reference to the evidence figure.")];
groups.forEach(g => {
  lbl.push(H2(g));
  D.links.filter(l => l.group === g).forEach(l => {
    lbl.push(H3(`${l.id} · ${l.label}`));
    lbl.push(table([2100, 7538], null, [
      ["Page", [new Paragraph({ children: [link(l.url, l.url, 16)] })]],
      ["Purpose", l.purpose],
      ["Key facts stated", l.data.map(d => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 20 }, children: [r(d, { size: 17 })] }))],
      ["Proposed destination", `${l.dest.title} (${l.dest.path})`],
      ["Observations", l.obs.length ? `${l.obs.length} — ${["H", "M", "L"].map(s => `${l.obs.filter(o => o.sev === s).length} ${SEV[s].t.toLowerCase()}`).join(", ")}` : "None — no content issue found"],
      ...l.verified.map(v => ["Verified", v]),
    ].map(([a, b]) => [cell(a, 2100, { bold: true, fill: PALE, size: 17 }), cell(b, 7538, { size: 17 })]), { zebra: false }));
    l.obs.forEach(o => {
      lbl.push(new Paragraph({ keepNext: true, spacing: { before: 160, after: 60 }, children: [r(`${l.id}-${o.n}  `, { bold: true, size: 19, color: NAVY }), sevRun(o.sev, 15), r("  "), tag(o.kind, 15), r("  "), tag(o.ref, 15)] }));
      lbl.push(P(o.note, { spacing: { after: 60, line: 264 } }));
      o.quotes.forEach(q => lbl.push(quoteP(q)));
      if (o.spelling.length) lbl.push(table([3000, 3000], ["As published", "Correct spelling"], o.spelling.map(([a, b]) => [a, b].map(t => cell([new Paragraph({ bidirectional: hasArabic(t), alignment: hasArabic(t) ? AlignmentType.START : AlignmentType.LEFT, children: [r(t, { size: 19, rightToLeft: hasArabic(t) })] })], 3000)))), P("", { spacing: { after: 60 } }));
      lbl.push(P([r("Recommended action: ", { bold: true, size: 19 }), r(o.action, { size: 19 })], { spacing: { after: 40 } }));
      if (o.shot) lbl.push(P([r(`Evidence: Figure E-${l.id}-${o.n} (Appendix A)`, { size: 17, color: MUTED, italics: true })], { spacing: { after: 80 } }));
    });
  });
});

// ---------- 7 mapping ----------
const mapping = [
  H1("7. From 36 Links to 17 Proposed Pages"),
  P("The UX / Information Architecture Blueprint proposes a 17-page admissions structure. Every current link has a destination in that structure. The table shows which current pages feed each proposed page and how many content observations must be resolved before the content is moved."),
  table([3000, 2438, 2200, 1000, 1000], ["Proposed page", "Path", "Current links", "Obs.", "High"], D.sitemap.map(n => {
    const os = allObs.filter(o => n.links.includes(o.link.id));
    return [cell(n.title, 3000, { bold: true, size: 17 }), cell(n.path, 2438, { size: 16 }), cell(n.links.join(", ") || "New page (no current source)", 2200, { size: 16 }), cell(String(os.length), 1000, { size: 17, align: AlignmentType.CENTER }), cell(String(os.filter(o => o.sev === "H").length), 1000, { size: 17, align: AlignmentType.CENTER })];
  })),
];

// ---------- 8 recommendations ----------
const recs = [
  H1("8. Recommendations and Next Steps"),
  H2("8.1 Recommended sequence"),
  numbered([r("Decide. ", { bold: true }), r("Each decision owner confirms the contested values listed in Section 1 and Section 4 (fees, channel, English and SAT thresholds, GPA descriptors, programme facts and durations).")], "num2"),
  numbered([r("Record. ", { bold: true }), r("Enter each approved value once in a canonical admissions record, with its owner, effective intake and date of last review.")], "num2"),
  numbered([r("Rewrite. ", { bold: true }), r("Correct or rewrite the affected pages from the record, starting with the high-severity links (C03, C06, C07, C08, C19, C20, C24, C27, C28).")], "num2"),
  numbered([r("Restructure. ", { bold: true }), r("Move the corrected content into the proposed 17-page structure (Section 7), and retire the superseded pages.")], "num2"),
  numbered([r("Verify. ", { bold: true }), r("Re-run the automated consistency check and a second content review before each intake opens.")], "num2"),
  H2("8.2 Publishing controls", { spacing: { before: 240 } }),
  bullet("Show 'Effective for intake · Owner · Last reviewed' on every rule page (F-19)."),
  bullet("Block publication of pages with empty required sections or placeholder text such as 'TBA' or 'to be developed' (F-26, F-43)."),
  bullet("Generate programme lists, names and facts from a single programme register (F-25, F-38, F-40)."),
  bullet("Add an editorial review in both languages before publication (F-17)."),
  bullet("State accreditations precisely, with the accreditor, scope and date (F-37)."),
];

// ---------- 9 corrections ----------
const corr = [
  H1("9. Corrections to Earlier Findings"),
  P([r("F-26 (empty required sections). ", { bold: true }), r("On 28 September 2026 the sections previously recorded as empty were present and visible: EMBA 'Educational Background' and 'Personal Interview'; PhD-BA 'Personal Interview'; MSME and MA IBL 'Educational Background'; and the Preparatory Program criteria and process. It cannot be established from the evidence whether they were added after 27 September or were misread earlier. F-26 is kept with a narrowed scope: the undescribed MA IBL written test and the empty MSHD 'Work Experience' heading. The correction is recorded in the register's self-correction log.")]),
];

// ---------- appendices ----------
const appA = [H1("Appendix A — Evidence Figures"),
  P("Each figure shows the live page region with the quoted text highlighted (red: high; orange: medium; blue: low). Captured read-only on 28 September 2026 at 1,366 px width.")];
allObs.filter(o => o.shot).forEach(o => {
  const file = path.join(LINKAUDIT, o.shot);
  const buf = fs.readFileSync(file);
  const dim = jpegSize(buf); const width = 600, height = Math.round(dim.h * width / dim.w);
  appA.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 60 }, children: [r(`Figure E-${o.link.id}-${o.n}. `, { bold: true, size: 18, color: NAVY }), r(`${o.link.id} ${o.link.label} — ${o.kind.toLowerCase()} (${o.ref}).`, { size: 18 })] }));
  appA.push(new Paragraph({ keepNext: true, spacing: { after: 40 }, children: [new ImageRun({ type: "jpg", data: buf, transformation: { width, height }, altText: { title: `Evidence ${o.link.id}-${o.n}`, description: `Screenshot of ${o.link.url} with the quoted text highlighted`, name: `E-${o.link.id}-${o.n}` } })] }));
  appA.push(P([r("Source: ", { size: 16, color: MUTED }), link(o.link.url, o.link.url, 16)], { spacing: { after: 160 } }));
});
function jpegSize(b) { let i = 2; while (i < b.length) { if (b[i] !== 0xFF) { i++; continue; } const m = b[i + 1]; const len = b.readUInt16BE(i + 2); if (m >= 0xC0 && m <= 0xC3) return { h: b.readUInt16BE(i + 5), w: b.readUInt16BE(i + 7) }; i += 2 + len; } throw new Error("no SOF"); }

const gloss = [["Aptis", "British Council English test used by PMU for placement in the Preparatory Program."], ["Core Program", "Term used on C33 for direct entry to a degree programme; not defined elsewhere."],
  ["EXIT exam", "Exam required to leave the Preparatory Program (C29); content and passing standard are not published."], ["Iqama", "Residence permit held by non-Saudi residents of the Kingdom."],
  ["Qabool (uap.sa)", "National unified admission platform for Saudi applicants to universities."], ["Qudrat", "General Aptitude Test (Education and Training Evaluation Commission)."],
  ["SAT / SAT II", "College Board tests; SAT Subject Tests (SAT II) were discontinued in 2021 (X06)."], ["Study in Saudi", "National platform for international applicants to Saudi universities."],
  ["Tahseely", "Standard Achievement Admission Test (Education and Training Evaluation Commission)."], ["TOEFL iBT", "ETS English test; reported on a 1–6 scale from 21 January 2026 (X01)."], ["VAT", "Value-added tax, 15% in the Kingdom."]];
const appB = [H1("Appendix B — Glossary"), table([2400, 7238], ["Term", "Meaning in this report"], gloss)];
const appC = [H1("Appendix C — External Sources"), table([900, 4738, 4000], ["Ref.", "Source", "Link"], D.sources.map(([id, t, u]) => [id, t, cell([new Paragraph({ children: [link(u, u, 16)] })], 4000)])),
  P("External facts were checked against the issuing organisation's own website. The Findings Register and the external-verification log in the audit repository record the full verification trail.", { spacing: { before: 200 } })];
const appD = [H1("Appendix D — Reproducibility"),
  P("All material in this report is generated from source files in the audit repository (branch claude/pmu-admissions-audit-jm54d8, folder pmu-admissions-audit/remediation/linkaudit/content):"),
  bullet("extract_text.js — extracts the live text of the 36 pages (read-only)."),
  bullet("content_findings.py / content_findings_en.py — the observations, in Arabic and English."),
  bullet("shots_content.js — captures the highlighted evidence figures."),
  bullet("export_en.py and report_en/build_docx.js — build this report; the build stops if any quotation is not verbatim."),
  bullet("PMU-Admissions-Content-Audit.html — the interactive Arabic edition of the same review."),
];

// ---------- document ----------
const doc = new Document({
  creator: "Admissions Office — independent content audit", title: "Content Audit of the Admissions Office Web Pages", description: "Independent content audit of the 36 links on pmu.edu.sa/admission/admission (28 September 2026)",
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: 20, color: INK } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 34, bold: true, color: NAVY, font: FONT }, paragraph: { spacing: { before: 120, after: 200 }, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 6 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 25, bold: true, color: NAVY, font: FONT }, paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1, keepNext: true } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, color: INK, font: FONT }, paragraph: { spacing: { before: 320, after: 100 }, outlineLevel: 2, keepNext: true } },
    ],
  },
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }, { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 240 } } } }] },
    { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 300 } } } }] },
    { reference: "num2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 300 } } } }] },
  ] },
  sections: [
    { properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } }, children: cover },
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1200, left: 1134, right: 1134, header: 560, footer: 560 }, pageNumbers: { start: 1 } } },
      headers: { default: new Header({ children: [new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: W }], border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 4 } }, children: [r("Content Audit of the Admissions Office Web Pages", { size: 15, color: MUTED }), new TextRun({ font: FONT, size: 15, color: MUTED, children: [new Tab(), "Internal — for discussion"] })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: W }], children: [r("Independent review · 28 September 2026", { size: 15, color: MUTED }), new TextRun({ font: FONT, size: 15, color: MUTED, children: [new Tab(), "Page ", PageNumber.CURRENT] })] })] }) },
      children: [...control, ...exec, ...method, ...results, ...matrix, ...newF, ...lbl, ...mapping, ...recs, ...corr, ...appA, ...appB, ...appC, ...appD],
    },
  ],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("wrote", OUT, (b.length / 1024 / 1024).toFixed(1) + " MB"); });
