const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,HeadingLevel,BorderStyle,Header,Footer,PageNumber,LevelFormat,TabStopType,VerticalAlign}=require('docx');
const NAVY='1F3864',ACC='2E75B6',LIGHT='EAF1FB',GREY='595959',RED='C00000',AMB='B7791F',GRN='2F855A';
const W=9638;
const r=(t,o={})=>new TextRun({text:t,font:'Calibri',size:o.size||20,bold:o.bold,color:o.color||'262626',italics:o.italics});
const p=(runs,o={})=>new Paragraph({children:Array.isArray(runs)?runs:[r(runs,o)],spacing:{after:o.after??120,before:o.before??0,line:276},alignment:o.align,keepNext:o.keepNext});
const h1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,children:[new TextRun({text:t,font:'Calibri',size:26,bold:true,color:NAVY})],spacing:{before:200,after:90},keepNext:true,border:{bottom:{style:BorderStyle.SINGLE,size:6,color:ACC,space:4}}});
const bullet=(runs)=>new Paragraph({numbering:{reference:'b',level:0},children:runs,spacing:{after:80,line:276}});
const num=(runs)=>new Paragraph({numbering:{reference:'n',level:0},children:runs,spacing:{after:80,line:276}});
const bd={style:BorderStyle.SINGLE,size:4,color:'BFBFBF'};const borders={top:bd,bottom:bd,left:bd,right:bd};
function table(widths,head,rows,opts={}){
 const mk=(t,i,isH,fill)=>new TableCell({width:{size:widths[i],type:WidthType.DXA},borders,verticalAlign:VerticalAlign.CENTER,
  shading:{type:ShadingType.CLEAR,color:'auto',fill:isH?NAVY:(fill||'FFFFFF')},margins:{top:45,bottom:45,left:100,right:100},
  children:[new Paragraph({alignment:(opts.center||[]).includes(i)?AlignmentType.CENTER:AlignmentType.LEFT,children:[typeof t==='object'?t:new TextRun({text:String(t),font:'Calibri',size:19,bold:isH||(opts.boldCol===i),color:isH?'FFFFFF':'262626'})]})]});
 return new Table({width:{size:W,type:WidthType.DXA},columnWidths:widths,rows:[
  new TableRow({tableHeader:true,children:head.map((t,i)=>mk(t,i,true))}),
  ...rows.map((row,k)=>new TableRow({cantSplit:true,children:row.map((t,i)=>mk(t,i,false,k%2?LIGHT:'FFFFFF'))}))]});
}
const status=(t,c)=>new TextRun({text:t,font:'Calibri',size:19,bold:true,color:c});
const children=[
 // Title block
 new Paragraph({children:[new TextRun({text:'PRINCE MOHAMMAD BIN FAHD UNIVERSITY  |  ADMISSIONS OFFICE',font:'Calibri',size:18,bold:true,color:ACC})],spacing:{after:60}}),
 new Paragraph({children:[new TextRun({text:'Admissions Office Webpages – Revisit Review',font:'Calibri',size:40,bold:true,color:NAVY})],spacing:{after:60}}),
 new Paragraph({children:[r('Published content of pmu.edu.sa/admission/admission and its directly linked pages',{color:GREY,size:22})],spacing:{after:200},border:{bottom:{style:BorderStyle.SINGLE,size:12,color:NAVY,space:8}}}),
 table([2349,7289],['Item','Details'],[
  ['Reference','Thread: "comments on Admission pages" (Oct 2025 – Sep 2026)'],
  ['Prepared for','Mr. Radhi H. Alkhaldi'],
  ['Prepared by','Nader Alfarhan, Student Affairs'],
  ['Content status as of','10 October 2026'],
  ['Review type','Read-only review of published content; no page was changed'],
 ],{boldCol:0}),
 h1('1. Purpose'),
 p('This review follows up on the thread "comments on Admission pages", as requested, by revisiting the Admissions Office webpages to identify comments of the same kind and any others. It covers only the content published on the website.'),
 h1('2. Overall Status'),
 table([3203,6435],['Indicator','Result'],[
  ['Overall status',status('NOT READY FOR CLOSURE',RED)],
  ['Pages reviewed','39 (Admissions page, 37 directly linked pages, application portal)'],
  ['Comments – linked pages','51  (Priority 1: 6 · Priority 2: 29 · Priority 3: 16)'],
  ['Comments – legacy pages','10  (still online, not linked from the Admissions page)'],
  ['Decisions required','10 (policy and fee owners)'],
 ],{boldCol:0}),
 h1('3. Scope and Method'),
 bullet([r('The Admissions Office page, its 37 directly linked pages and the application portal welcome page. The Contact Us staff list was not copied because it contains personal names.')]),
 bullet([r('Each page was read line by line in a mobile view (390 px), including tables and content inside tabs. The '),r('/apply',{bold:true}),r(' page was read from its source because it redirects visitors immediately.')]),
 bullet([r('Each amendment previously requested in the thread was re-checked against the live page.')]),
 bullet([r('Read-only: no page, form or payment was changed or submitted. The desktop view was not tested.')]),
 h1('4. Priority 1 Items'),
 table([534,2456,6648],['#','Topic','What the published pages show'],[
  ['1','International CS/Engineering','Criteria still require SAT II, which has been discontinued since 2021.'],
  ['2','International transfer / visiting fee','SAR 500 (excl. VAT); the transfer and visiting pages show SAR 950 (incl. VAT).'],
  ['3','Medicine application fee','SAR 1,000 on the admission page vs SAR 1,150 on the medical fees page.'],
  ['4','Admission calendar','Covers Fall 2026 only and all dates have passed. The application portal shows "No events are currently published".'],
  ['5','EMGMS page','Contains another university\'s text ("UA Center for English as Second Language"). Its English requirements differ from other graduate pages, and it has no application link.'],
  ['6','Non-Saudi applicants','The route and deadline are not stated on the international page, and the calendar shows the route as "Closed" with no date.'],
 ],{center:[0],boldCol:1}),
 h1('5. Previously Requested Amendments – Live Status'),
 table([4378,5260],['Request (thread)','Status on the live site'],[
  ['B.S. Chemical Engineering',status('Implemented',GRN)],
  ['Minimum weighted score 74% / 72%',status('Decision needed – published minima compute to 73% / 72%',AMB)],
  ['International / transfer / visitor fee SAR 950',status('Partial – international page still SAR 500 (excl. VAT)',AMB)],
  ['Remove SAT II',status('Not implemented',RED)],
  ['Aptis re-test fee SAR 950',status('Not implemented – fees page shows SAR 575',RED)],
  ['Retire old CS/Engineering page and old guide',status('Not implemented / not verifiable',RED)],
  ['Graphic Design – female only',status('Not implemented – page shows Male and Female',RED)],
 ],{boldCol:0}),
 h1('6. Decisions Required'),
 p('Ten decisions with proposed owners are listed in the attached register (sheet "Decisions required"). Pending values should not be published as policy until the relevant owner confirms them in writing. The main ones are:',{after:80}),
 num([r('Next intake and one application route per applicant type.',{bold:true}),r(' Admissions, Web and IT.')]),
 num([r('Fee and VAT matrix',{bold:true}),r(' (international, Medicine, Aptis). Finance with Admissions.')]),
 num([r('Minimum weighted scores and SAT alternatives',{bold:true}),r(' (SAT II, SAT 1200 scope). Admissions with the Colleges.')]),
 num([r('Graduate English requirements and EMGMS page.',{bold:true}),r(' Graduate Studies.')]),
 num([r('Admissions contact channel and privacy notice.',{bold:true}),r(' Admissions with Compliance.')]),
 h1('7. Attachments'),
 table([747,3524,5367],['No.','File','Content'],[
  ['02','Admission Pages Comments Register (xlsx)','Page-by-page comments with verbatim evidence and proposed change; decisions required; live status of previous requests.'],
  ['03','Published Content Line-by-Line Ledger (xlsx)','Full extracted text of each page, for reference.'],
 ],{center:[0]}),
 h1('8. Limits'),
 bullet([r('The desktop view was not tested.')]),
 bullet([r('Content that only appears after interaction (pop-ups) and the downloadable PDF files were not fully reviewed.')]),
 bullet([r('TOEFL/IELTS equivalences refer to published ETS tables; setting the thresholds remains the owners\' decision.')]),
];
const doc=new Document({creator:'Nader Alfarhan',title:'Admissions Office Webpages – Revisit Review',
 styles:{default:{document:{run:{font:'Calibri',size:20}}}},
 numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:270}}}}]},
  {reference:'n',levels:[{level:0,format:LevelFormat.DECIMAL,text:'%1.',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:300}}}}]}]},
 sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1000,bottom:900,left:1134,right:1134}}},
  headers:{default:new Header({children:[new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:'Admissions Office Webpages – Revisit Review  |  Internal – for review',font:'Calibri',size:16,color:GREY})]})]})},
  footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({font:'Calibri',size:16,color:GREY,children:['Page ',PageNumber.CURRENT,' of ',PageNumber.TOTAL_PAGES]})]})]})},
  children}]});
Packer.toBuffer(doc).then(b=>fs.writeFileSync(process.argv[2],b));
