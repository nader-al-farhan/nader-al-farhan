const fs=require('fs');
const D=JSON.parse(fs.readFileSync(__dirname+'/decisions.json'));
const CAT=JSON.parse(fs.readFileSync(process.argv[3]));
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,HeadingLevel,BorderStyle,Header,Footer,PageNumber,LevelFormat,VerticalAlign,PageBreak}=require('docx');
const NAVY='1F3864',ACC='2E75B6',LIGHT='EAF1FB',GREY='595959',RED='C00000',AMB='B7791F',GRN='2F855A';
const W=9638;
const r=(t,o={})=>new TextRun({text:t,font:'Calibri',size:o.size||20,bold:o.bold,color:o.color||'262626',italics:o.italics});
const p=(runs,o={})=>new Paragraph({children:Array.isArray(runs)?runs:[r(runs,o)],spacing:{after:o.after??110,before:o.before??0,line:276},alignment:o.align??AlignmentType.JUSTIFIED,keepNext:o.keepNext});
const h1=(t,pb)=>new Paragraph({pageBreakBefore:!!pb,heading:HeadingLevel.HEADING_1,children:[new TextRun({text:t,font:'Calibri',size:28,bold:true,color:NAVY})],spacing:{before:200,after:100},keepNext:true,border:{bottom:{style:BorderStyle.SINGLE,size:6,color:ACC,space:4}}});
const h2=t=>new Paragraph({heading:HeadingLevel.HEADING_2,children:[new TextRun({text:t,font:'Calibri',size:22,bold:true,color:ACC})],spacing:{before:140,after:70},keepNext:true});
const bullet=(runs)=>new Paragraph({numbering:{reference:'b',level:0},children:Array.isArray(runs)?runs:[r(runs)],spacing:{after:60,line:268}});
const num=(runs)=>new Paragraph({numbering:{reference:'n',level:0},children:Array.isArray(runs)?runs:[r(runs)],spacing:{after:60,line:268}});
const bd={style:BorderStyle.SINGLE,size:4,color:'BFBFBF'};const borders={top:bd,bottom:bd,left:bd,right:bd};
function table(widths,head,rows,opts={}){
 const sum=widths.reduce((a,b)=>a+b,0);widths=widths.map(x=>Math.round(x*W/sum));widths[widths.length-1]+=W-widths.reduce((a,b)=>a+b,0);
 const mk=(t,i,isH,fill)=>new TableCell({width:{size:widths[i],type:WidthType.DXA},borders,verticalAlign:VerticalAlign.CENTER,
  shading:{type:ShadingType.CLEAR,color:'auto',fill:isH?NAVY:(fill||'FFFFFF')},margins:{top:45,bottom:45,left:90,right:90},
  children:[new Paragraph({alignment:(opts.center||[]).includes(i)?AlignmentType.CENTER:AlignmentType.LEFT,children:[typeof t==='object'?t:new TextRun({text:String(t),font:'Calibri',size:opts.size||18,bold:isH||(opts.boldCol===i)||(opts.boldRows||[]).includes(t),color:isH?'FFFFFF':'262626'})]})]});
 return new Table({width:{size:W,type:WidthType.DXA},columnWidths:widths,rows:[
  new TableRow({tableHeader:true,children:head.map((t,i)=>mk(t,i,true))}),
  ...rows.map((row,k)=>new TableRow({cantSplit:true,children:row.map((t,i)=>mk(t,i,false,(opts.totalLast&&k===rows.length-1)?'D9E2F3':(k%2?LIGHT:'FFFFFF')))}))]});
}
const st=(t,c)=>new TextRun({text:t,font:'Calibri',size:18,bold:true,color:c});
const sp=()=>new Paragraph({children:[],spacing:{after:80}});
const kpi=(items)=>{const w=Math.floor(W/items.length);return new Table({width:{size:W,type:WidthType.DXA},columnWidths:items.map(()=>w),rows:[new TableRow({children:items.map(([v,l,c])=>new TableCell({width:{size:w,type:WidthType.DXA},borders:{top:{style:BorderStyle.SINGLE,size:18,color:c||ACC},bottom:bd,left:bd,right:bd},shading:{type:ShadingType.CLEAR,color:'auto',fill:'F7F9FC'},margins:{top:80,bottom:80,left:80,right:80},children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:v,font:'Calibri',size:34,bold:true,color:c||NAVY})]}),new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:l,font:'Calibri',size:16,color:GREY})]})]}))})]})};

// ---------- COVER
const cover=[
 new Paragraph({children:[],spacing:{before:1800}}),
 new Paragraph({children:[new TextRun({text:'PRINCE MOHAMMAD BIN FAHD UNIVERSITY',font:'Calibri',size:22,bold:true,color:ACC})],spacing:{after:60}}),
 new Paragraph({children:[new TextRun({text:'Admissions Office',font:'Calibri',size:22,color:GREY})],spacing:{after:600}}),
 new Paragraph({children:[new TextRun({text:'Admissions Office Webpages',font:'Calibri',size:52,bold:true,color:NAVY})]}),
 new Paragraph({children:[new TextRun({text:'Revisit Review and Recommendations',font:'Calibri',size:40,color:NAVY})],spacing:{after:200},border:{bottom:{style:BorderStyle.SINGLE,size:18,color:ACC,space:10}}}),
 new Paragraph({children:[new TextRun({text:'Executive report on the published content of pmu.edu.sa/admission/admission and its directly linked pages',font:'Calibri',size:22,italics:true,color:GREY})],spacing:{after:900}}),
 table([2600,7000],['Document control',''],[
  ['Prepared for','Mr. Radhi H. Alkhaldi'],
  ['Prepared by','Nader Alfarhan, Student Affairs'],
  ['Reference','Email thread "comments on Admission pages" (October 2025 – September 2026)'],
  ['Content reviewed as of','10 October 2026 (key facts re-checked 11 October 2026)'],
  ['Version / status','1.0 – For review and decision'],
  ['Classification','Internal'],
 ],{boldCol:0,size:19}),
];
// ---------- BODY
const C=CAT.sum;const areas=Object.keys(C);
const tot=k=>areas.reduce((a,x)=>a+C[x][k],0);
const body=[
 h1('1. Executive Summary'),
 p('At your request, the Admissions Office webpages were revisited to review their published content and provide feedback, continuing the comments exchanged in the thread "comments on Admission pages". The review covered the Admissions Office page, all 37 pages linked directly from it and the application portal. Every content line was read and checked against the other pages and the University\'s own fee tables.'),
 kpi([['39','Pages reviewed'],['1,248','Content lines audited'],['71','Key findings'],['211','Detailed page notes'],['10','Decisions required',RED]]),
 sp(),
 h2('Key messages'),
 bullet([r('Applicants cannot currently see a valid admission cycle. ',{bold:true}),r('The only admission calendar covers Fall 2026, all its dates have passed, and the application portal shows "No events are currently published".')]),
 bullet([r('Several critical values conflict between pages. ',{bold:true}),r('These include application fees (SAR 500 excl. VAT vs SAR 950 incl. VAT; Medicine SAR 1,000 vs SAR 1,150), entry tests (SAT II is still required for international CS/Engineering applicants) and English requirements for graduate programmes.')]),
 bullet([r('Most amendments requested in the thread are not yet live. ',{bold:true}),r('B.S. Chemical Engineering has been added; the weighted minimums, fee changes, SAT II removal, Aptis fee and retirement of the old CS/Engineering page are not yet reflected.')]),
 bullet([r('The root cause is structural rather than editorial. ',{bold:true}),r('The same rule or fee is maintained on several pages without a single approved source, owner or effective date, so corrections do not propagate.')]),
 bullet([r('37 of the 71 key findings can be corrected directly ',{bold:true}),r('(wording, links, accessibility, page titles); 34 depend on ten owner decisions, listed in Section 7.')]),
 h2('Overall status'),
 p([r('NOT READY FOR CLOSURE. ',{bold:true,color:RED}),r('Closure requires the ten decisions, the corresponding page corrections and a read-back check of the live pages.')]),

 h1('2. Background and Mandate'),
 p('The thread "comments on Admission pages" (October 2025 – September 2026) recorded comments and requested amendments to the Admissions webpages, including weighted minimum scores, fees, SAT II requirements, the Aptis fee, new programmes and the retirement of older pages. Mr. Radhi requested a revisit of the Admissions Office page to review it carefully and provide feedback. This report responds to that request and updates the status of the earlier comments against what is currently published.'),
 h1('3. Scope and Methodology'),
 table([2400,7200],['Element','Approach'],[
  ['Scope','Admissions Office page (Level 0), the 37 pages linked from its content (Level 1), the application portal, and three official fee pages used to verify amounts (Level 2). Site-wide header, footer and menus were excluded.'],
  ['Reading','Every page was read line by line in a mobile browser view (390 px), including tables and content inside tabs (257 lines). The /apply page was read from its source (136 lines) because it redirects visitors immediately.'],
  ['Checks per line','Applicant segment, term or date, consistency with other pages and with the official fee tables, spelling and wording, and a review status.'],
  ['Independent verification','An earlier set of 214 detailed page notes was re-verified one by one against the captured pages: 169 confirmed, 42 partly confirmed, 3 not verifiable, none rejected.'],
  ['Re-check','The Priority 1 facts were re-checked on the live site on 11 October 2026; all remained unchanged.'],
  ['Evidence standard','A finding is recorded only with verbatim text from the published page. Requests in the thread are treated as requests, not as approved policy.'],
  ['Boundaries','Read-only: no page, form or payment was changed or submitted. The Contact Us staff list was not copied (personal names).'],
 ],{boldCol:0}),

 h1('4. Results by Area'),
 table([4200,900,900,900,1000,1400],['Area','P1','P2','P3','Total','Needs decision'],[
  ...areas.map(a=>[a,C[a].P1,C[a].P2,C[a].P3,C[a].total,C[a].decision]),
  ['Total',tot('P1'),tot('P2'),tot('P3'),tot('total'),tot('decision')]
 ],{center:[1,2,3,4,5],totalLast:true,boldRows:['Total']}),
 p('Priority definitions: P1 – affects eligibility, fees or the application route; P2 – inconsistency or missing information; P3 – wording, accessibility or housekeeping. Ten of the key findings concern legacy pages that are still online but no longer linked from the Admissions page.',{size:17,color:GREY,before:60}),
 h2('Priority 1 findings'),
 table([500,2200,4300,2600],['#','Topic','What the published pages show','Impact'],[
  ['1','International CS/Engineering criteria','"Computer Science & Engineering Majors: Secondary School 40% / SAT I 30% / SAT II 30%". SAT Subject Tests were discontinued in 2021.','Applicants are asked for a test they cannot take.'],
  ['2','International transfer / visiting fee','"SAR 500 (excl. VAT)" on the international page; "SAR 950 (incl. VAT)" on the transfer and visiting pages and the official fees page.','Different amounts for the same service; billing disputes.'],
  ['3','Medicine application fee','"SAR 1000 (incl. VAT)" on the admission page; "SAR 1,150 (VAT inclusive)" on the medical fees page.','Applicants may pay the wrong amount.'],
  ['4','Admission calendar','Fall 2026-2027 only; last application date 2026-06-24; orientation "TBA"; portal: "No events are currently published".','No visible next intake for prospective applicants.'],
  ['5','EMGMS page','Refers to "UA Center for English as Second Language (CESL)"; TOEFL 79 / IELTS 7 unlike all other pages; no application link.','Reputational risk; unclear requirements.'],
  ['6','Non-Saudi applicants','Calendar: "Apply online through Study in Saudi platform … Closed" with no date; the international page gives no route or deadline.','Non-Saudi applicants cannot tell how or when to apply.'],
 ],{center:[0],boldCol:1,size:17}),

 h1('5. Status of Previously Requested Amendments'),
 table([3800,3800,2000],['Request in the thread','Live status (re-checked 11 Oct 2026)','Status'],[
  ['B.S. Chemical Engineering','Listed on Degrees & Programs',st('Implemented',GRN)],
  ['Minimum weighted score 74% (CS/Eng) / 72% (others)','Not shown on visible pages; published minima compute to 73% / 72%',st('Decision needed',AMB)],
  ['International / transfer / visitor fee SAR 950','International page still SAR 500 (excl. VAT)',st('Partial',AMB)],
  ['Remove SAT II (CS & Engineering)','International page still shows SAT II 30%',st('Not implemented',RED)],
  ['Aptis re-test fee SAR 950','Fees page SAR 575; Aptis page shows no fee',st('Not implemented',RED)],
  ['Retire old CS/Engineering page and old guide','CS/Engineering page still live; guide not verifiable',st('Not implemented',RED)],
  ['Graphic Design – female only','Degrees & Programs shows Male and Female',st('Not implemented',RED)],
  ['Admission data-flow (February 2026 draft)','Not published',st('Draft',AMB)],
 ],{boldCol:0,size:17}),
 h1('6. Root Causes'),
 p('The findings point to a small number of underlying causes. Correcting individual sentences without addressing them is likely to reproduce the same issues in the next cycle.'),
 table([3000,4300,2300],['Cause','Evidence','Basis'],[
  ['No single approved source for admission values','The same fee, test or threshold appears on several pages with different values (e.g. SAR 500/950; IELTS 6.0/6.5 for MIBL).','Observed'],
  ['No recorded owner, approver or effective date','Pages carry no "last updated" or effective-intake information; requests in the thread have no recorded approval or implementation date.','Observed'],
  ['No seasonal update routine','The calendar still shows Fall 2026; orientation "TBA"; home-page items dated 2023–2028.','Observed'],
  ['Legacy pages not retired','Older admission pages with outdated rules remain online and searchable.','Observed'],
  ['Content placed where applicants cannot see it','Bachelor\'s minimums appear only in /apply, which redirects instantly; 257 lines sit in hidden tabs.','Observed'],
  ['Copied or template content not reviewed','EMGMS text from another institution; repeated misspelling "ADMISSSIONS" across six pages.','Inferred'],
 ],{boldCol:0,size:17}),

 h1('7. Decisions Required'),
 p('The following decisions are required before the related wording can be corrected. Recommendations are subject to the owners\' approval; no value should be published as policy without written confirmation.'),
 table([700,2300,4300,2300],['ID','Decision','Recommendation','Owner'],D.map(d=>[d[0],d[1],d[4],d[5]]),{boldCol:1,size:17,center:[0]}),

 h1('8. Recommendations and Implementation Roadmap'),
 h2('Recommendations'),
 num([r('Publish an interim admission-cycle notice now ',{bold:true}),r('and one application route per applicant type (Decision D-01).')]),
 num([r('Make the official fee table the only fee reference ',{bold:true}),r('and link every admission page to it (D-02).')]),
 num([r('Correct the 37 findings that need no decision ',{bold:true}),r('(wording, titles, links, accessibility, Arabic spelling) as a first batch.')]),
 num([r('Remove the external text from the EMGMS page immediately ',{bold:true}),r('and publish approved requirements (D-05).')]),
 num([r('Create a single admissions source of truth ',{bold:true}),r('in which every critical value has an owner, approver, effective intake and last-reviewed date.')]),
 num([r('Introduce a pre-cycle content review ',{bold:true}),r('before each intake, with a read-back check of the live pages after every change.')]),
 num([r('Restructure the Admissions page around applicant type ',{bold:true}),r('(Saudi, non-Saudi, transfer, visiting, graduate, Medicine), showing status, requirements, fees, deadline and route.')]),
 h2('Roadmap (durations start from the relevant approval)'),
 table([1600,4400,2000,1600],['Phase','Work','Dependency','Indicative effort'],[
  ['0 – Decide','Owners decide D-01 to D-10 and confirm values in writing.','Leadership direction','Owner-dependent'],
  ['1 – Quick fixes','Interim cycle notice; remove EMGMS external text; correct wording, titles, links and Arabic spelling (37 direct findings).','None for direct fixes','Short (days)'],
  ['2 – Decided corrections','Apply approved fees, thresholds, tests, graduate requirements and contact/privacy changes (34 findings).','Phase 0 decisions','Short to medium'],
  ['3 – Structural','Single source of truth, applicant-type entry page, retirement of legacy pages, pre-cycle review routine.','Web/IT capacity','Medium'],
 ],{boldCol:0,size:17}),
 h1('9. Acceptance and Closure Criteria'),
 p('An item is closed only when all of the following are evidenced:'),
 bullet('The approved value is recorded with its owner, approver and effective intake.'),
 bullet('The live page has been updated and re-read after publication (Arabic and English, mobile and desktop).'),
 bullet('Related pages, links and the application portal show the same value.'),
 bullet('The register entry is updated with the date and evidence of the read-back check.'),
 h1('10. Limitations'),
 bullet('The desktop view could not be tested because automated desktop access was blocked; mobile view was used throughout.'),
 bullet('Content that appears only after interaction (pop-ups) and the downloadable PDF guides were not fully reviewed.'),
 bullet('TOEFL/IELTS equivalences refer to the published ETS tables; setting thresholds remains the owners\' decision.'),
 bullet('This is a content review; it did not test the application or payment workflows.'),
 h1('Appendix A – Attachments',true),
 table([700,3600,5300],['No.','File','Content'],[
  ['02','Admission Pages Comments Register (xlsx)','Summary; A. 71 key findings with area, evidence, proposed change and decision link; B. 211 page-by-page notes; C. ten decisions with options and recommendations; D. status of earlier requests.'],
  ['03','Published Content Line-by-Line Ledger (xlsx)','Every published line of each page with its review status and cross-reference (for reference).'],
 ],{center:[0],size:17}),
 h1('Appendix B – Pages Reviewed'),
 (()=>{const P=CAT.pages.map(x=>[x.slice(0,3),x.slice(4)]);const h=Math.ceil(P.length/2);const rows=[];for(let i=0;i<h;i++){const a=P[i]||['',''],b=P[i+h]||['',''];rows.push([a[0],a[1],b[0],b[1]]);}return table([600,4200,600,4200],['ID','Page','ID','Page'],rows,{size:16,center:[0,2]});})(),
];
const doc=new Document({creator:'Nader Alfarhan',title:'Admissions Office Webpages – Revisit Review and Recommendations',
 styles:{default:{document:{run:{font:'Calibri',size:20}}}},
 numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:270}}}}]},
  {reference:'n',levels:[{level:0,format:LevelFormat.DECIMAL,text:'%1.',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:300}}}}]}]},
 sections:[
  {properties:{page:{size:{width:11906,height:16838},margin:{top:1134,bottom:1000,left:1134,right:1134}}},children:cover},
  {properties:{page:{size:{width:11906,height:16838},margin:{top:1000,bottom:900,left:1134,right:1134},pageNumbers:{start:1}}},
   headers:{default:new Header({children:[new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:'Admissions Office Webpages – Revisit Review  |  Internal',font:'Calibri',size:16,color:GREY})]})]})},
   footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({font:'Calibri',size:16,color:GREY,children:['Page ',PageNumber.CURRENT,]})]})]})},
   children:body}]});
Packer.toBuffer(doc).then(b=>fs.writeFileSync(process.argv[2],b));
