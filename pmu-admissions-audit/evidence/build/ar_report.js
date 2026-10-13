const fs=require('fs');const path=require('path');
const D=path.join(__dirname,'../../final_review');
const FONT=process.argv[3]||'Arial';
const ROWS=JSON.parse(fs.readFileSync(D+'/final_rows.json'));const PM=JSON.parse(fs.readFileSync(D+'/pagemap.json'));
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,BorderStyle,Header,Footer,PageNumber,LevelFormat,VerticalAlign,PageOrientation,HeadingLevel}=require('docx');
const NAVY='1F3864',ACC='2E75B6',LIGHT='EAF1FB',GREY='595959',RED='C00000',AMB='B7791F',GRN='2F855A';
const ORDER=['P00','P03','P04','P05','P06','P07','P08','P38','Shared menu','P09','P24','P25','P26','P27','P28','P29','P30','P31','P10','P11','P12','P13','P14','P15','P16','P17','P18','P19','P20','P21','P22','P23','P32','P33','P34','P35','P36','P37'];
const PR={'عالية':0,'متوسطة':1,'منخفضة':2};
ROWS.sort((a,b)=>(ORDER.indexOf(a.page_id)-ORDER.indexOf(b.page_id))||(PR[a.priority]-PR[b.priority]));
const N=ROWS.length;const cnt=(k)=>{const c={};ROWS.forEach(r=>c[r[k]]=(c[r[k]]||0)+1);return c};
const CL=cnt('classification'),PRI=cnt('priority'),AX=cnt('axis');
const r=(t,o={})=>new TextRun({text:String(t),font:{ascii:FONT,hAnsi:FONT,cs:FONT},size:o.size||22,sizeComplexScript:o.size||22,bold:o.bold,boldComplexScript:o.bold,color:o.color||'262626',rightToLeft:o.ltr?false:true,italics:o.italics});
const P=(runs,o={})=>new Paragraph({bidirectional:true,alignment:o.align||AlignmentType.JUSTIFIED,children:Array.isArray(runs)?runs:[r(runs,o)],spacing:{after:o.after??100,before:o.before??0,line:300},keepNext:o.keepNext,pageBreakBefore:o.pb});
const H1=(t,pb)=>new Paragraph({heading:HeadingLevel.HEADING_1,bidirectional:true,alignment:AlignmentType.RIGHT,pageBreakBefore:!!pb,keepNext:true,spacing:{before:220,after:110},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:ACC,space:4}},children:[r(t,{size:30,bold:true,color:NAVY})]});
const H2=t=>new Paragraph({bidirectional:true,alignment:AlignmentType.RIGHT,keepNext:true,spacing:{before:140,after:70},children:[r(t,{size:24,bold:true,color:ACC})]});
const B=(runs)=>new Paragraph({bidirectional:true,alignment:AlignmentType.JUSTIFIED,numbering:{reference:'b',level:0},children:Array.isArray(runs)?runs:[r(runs)],spacing:{after:60,line:290}});
const bd={style:BorderStyle.SINGLE,size:4,color:'BFBFBF'};const borders={top:bd,bottom:bd,left:bd,right:bd};
function T(W,widths,head,rows,o={}){const s=widths.reduce((a,b)=>a+b,0);widths=widths.map(x=>Math.round(x*W/s));widths[widths.length-1]+=W-widths.reduce((a,b)=>a+b,0);
 const cell=(c,i,isH,fill)=>{const runs=Array.isArray(c)?c.map(x=>typeof x==='string'?r(x,{size:o.size||16}):x):[typeof c==='object'&&c!==null&&c.t!==undefined?r(c.t,{...c,size:c.size||o.size||18}):r(c??'',{size:o.size||18,bold:isH||(o.boldCol===i),color:isH?'FFFFFF':'262626',ltr:(o.ltrCols||[]).includes(i)&&!isH})];
  return new TableCell({width:{size:widths[i],type:WidthType.DXA},borders,verticalAlign:VerticalAlign.CENTER,shading:{type:ShadingType.CLEAR,color:'auto',fill:isH?NAVY:(fill||'FFFFFF')},margins:{top:50,bottom:50,left:80,right:80},
   children:[new Paragraph({bidirectional:!(o.ltrCols||[]).includes(i)||isH,alignment:(o.center||[]).includes(i)?AlignmentType.CENTER:((o.ltrCols||[]).includes(i)&&!isH?AlignmentType.LEFT:AlignmentType.RIGHT),children:runs})]})};
 return new Table({visuallyRightToLeft:true,width:{size:W,type:WidthType.DXA},columnWidths:widths,rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>cell(h,i,true))}),...rows.map((row,k)=>new TableRow({cantSplit:o.cantSplit!==false,children:row.map((c,i)=>cell(c,i,false,(o.totalLast&&k===rows.length-1)?'D9E2F3':(k%2?LIGHT:'FFFFFF')))}))]});}
const pc=p=>({'عالية':RED,'متوسطة':AMB,'منخفضة':GRN}[p]);
const cc=c=>({'تصحيح مطلوب':RED,'توصية تحسين':ACC,'متابعة وتحقق':AMB}[c]);
const W1=9638,W2=14570;
const pname=id=>id==='Shared menu'?'القائمة الجانبية لصفحات القبول':(PM[id]?PM[id].ar:id);
const high=ROWS.filter(x=>x.priority==='عالية');
// ---------- cover
const cover=[new Paragraph({children:[],spacing:{before:1500}}),
 P([r('جامعة الأمير محمد بن فهد',{size:26,bold:true,color:ACC})],{align:AlignmentType.RIGHT,after:40}),
 P([r('مكتب القبول',{size:24,color:GREY})],{align:AlignmentType.RIGHT,after:500}),
 P([r('تقرير المراجعة الشاملة لصفحات مكتب القبول',{size:48,bold:true,color:NAVY})],{align:AlignmentType.RIGHT,after:80}),
 new Paragraph({bidirectional:true,alignment:AlignmentType.RIGHT,spacing:{after:200},border:{bottom:{style:BorderStyle.SINGLE,size:18,color:ACC,space:10}},children:[r('رصد لغوي ومعلوماتي ووظيفي وتنظيمي للمحتوى المنشور',{size:30,color:NAVY})]}),
 P([r('صفحة مكتب القبول ',{size:22,color:GREY,italics:true}),r('https://pmu.edu.sa/admission/admission',{size:20,color:GREY,ltr:true}),r(' وجميع الصفحات والملفات المرتبطة بها ضمن قسم القبول',{size:22,color:GREY,italics:true})],{align:AlignmentType.RIGHT,after:800}),
 T(W1,[2600,7000],['ضبط الوثيقة',''],[['مقدَّم إلى','الأستاذ راضي الخالدي – مدير القبول'],['إعداد','نادر الفرحان – شؤون الطلاب'],['المرجع','استكمال لسلسلة البريد «comments on Admission pages»'],['تاريخ الرصد','10 أكتوبر 2026، مع إعادة تحقق في 11 أكتوبر 2026'],['حالة الوثيقة','الإصدار 1.0 – للمراجعة والاعتماد'],['التصنيف','داخلي']],{boldCol:0,size:20})];
// ---------- body (portrait)
const body=[
 H1('1. الملخص التنفيذي'),
 P(`بناءً على طلب مدير القبول، رُوجع المحتوى المنشور لصفحة مكتب القبول وجميع الصفحات المرتبطة بها ضمن قسم القبول، وعددها 36 صفحة بما فيها بوابة التقديم، إضافة إلى ملفين مرفقين بصيغة PDF وثلاث صفحات رسوم رسمية استُخدمت مرجعًا للتحقق. قُرئت كل وحدة محتوى سطرًا بسطر (1,248 سطرًا) على ستة محاور: اللغة، ودقة المعلومات، والجانب الوظيفي، والتنظيم، والاتساق، وتجربة المستخدم.`),
 P(`رُصدت ${N} ملاحظة موحّدة بعد دمج المتكرر: ${CL['تصحيح مطلوب']} تصحيحًا مطلوبًا، و${CL['توصية تحسين']} توصية تحسين، و${CL['متابعة وتحقق']} بندًا للمتابعة والتحقق؛ منها ${PRI['عالية']} ملاحظات عالية الأولوية و${PRI['متوسطة']} متوسطة و${PRI['منخفضة']} منخفضة.`),
 P([r('أبرز ثلاث أولويات: ',{bold:true}),r('(1) لا يجد المتقدم دورة قبول سارية؛ فالتقويم الوحيد لخريف 2026 وجميع مواعيده منتهية، وبوابة التقديم لا تعرض أي مواعيد. (2) تعارض رسوم التقديم بين الصفحات (500 ريال غير شاملة الضريبة مقابل 950 ريالًا شاملة للمحولين والزائرين الدوليين، و1,000 مقابل 1,150 ريالًا لكلية الطب). (3) تعارض شروط القبول واللغة، ومنها اشتراط SAT II الموقوف منذ 2021 للطلاب الدوليين، واختلاف درجة IELTS المطلوبة في عدد من برامج الدراسات العليا، ووجود نص يشير إلى جامعة أخرى في صفحة EMGMS.')]),
 P([r('الحكم: ',{bold:true}),r('الصفحة غير جاهزة للاعتماد النهائي إلى أن تُعالَج عوائق الإغلاق الواردة في القسم 5.',{bold:true,color:RED})]),
 H1('2. نطاق الرصد'),
 P('شمل الرصد صفحة مكتب القبول وكل رابط داخلي مباشر في حاويات القبول، وما يتفرع منها مما يلزم لفهم شرط أو رسم أو إجراء، والملفات المرفقة المرتبطة مباشرة بالقبول. وفيما يلي قائمة ما فُحص وحالته:'),
];
const inv=[];const ids=Object.keys(PM).filter(k=>/^P\d\d$/.test(k)).sort();
for(const id of ids){const st=id==='P06'?'فُحص الرابط ووجهته فقط (لم يُنسخ المحتوى لاحتوائه أسماء موظفين)':(['P01','P02'].includes(id)?'خارج النطاق (صفحة عامة غير تابعة لمكتب القبول) – ذُكرت إحالاتها فقط':'فُحصت سطرًا بسطر');
 inv.push([id,PM[id].ar||PM[id].title,{t:PM[id].url.replace('https://www.','').replace('https://',''),ltr:true,size:15},st]);}
inv.push(['PDF','دليل المرشح لاختبار Aptis (2017)',{t:'pmu.edu.sa/Attachments/Admission/PDF/Appendix 3.3 (Aptis Candidate Guide).pdf',ltr:true,size:15},'فُحص (50 صفحة)']);
inv.push(['PDF','دليل التقديم الإلكتروني Web Admission Guide (2018)',{t:'pmu.edu.sa/Attachments/Admission/Images/PDF/Web-Admission-Guide-v2-2_20-12-18.pdf',ltr:true,size:15},'فُحص (21 صفحة)']);
inv.push(['L2','صفحات الرسوم الرسمية (رسوم أخرى، رسوم البرنامج الطبي، رسوم البكالوريوس 2026/2027)',{t:'pmu.edu.sa/admission/student_fees_tf_ro …',ltr:true,size:15},'مرجع تحقق للرسوم']);
body.push(T(W1,[700,3300,3600,2000],['المعرّف','الصفحة','الرابط','حالة الفحص'],inv,{size:16,center:[0]}));
body.push(P('ملاحظة: 39 صفحة اكتُشفت ضمن النطاق؛ فُحصت منها 36 صفحة سطرًا بسطر، وصفحة واحدة (قائمة الموظفين) فُحص رابطها فقط، وصفحتان عامتان خارج قسم القبول ذُكرت إحالاتهما للعلم فقط.',{size:18,color:GREY,before:60}));
// ---------- register (landscape)
const reg=[H1('3. سجل الملاحظات'),P(`يعرض السجل ${N} ملاحظة مرتبة حسب الصفحة ثم الأولوية. النص الحالي منقول حرفيًا كما هو منشور (وغالبه باللغة الإنجليزية)، وما بين معقوفين [ ] يحدد الصفحة المصدر عند المقارنة بين أكثر من صفحة.`,{size:20})];
const rows=ROWS.map((x,i)=>[String(i+1),[r(pname(x.page_id),{size:16,bold:true}),r(' — ',{size:16}),r(x.url.split(';')[0].replace('https://www.','').replace('https://',''),{size:13,ltr:true,color:GREY})],r(x.location,{size:16}),r(x.current_text,{size:15,ltr:true}),[r(x.type+' ',{size:16,bold:true}),r('('+x.axis+'): ',{size:15,color:GREY}),r(x.description,{size:16})],r(x.classification,{size:16,bold:true,color:cc(x.classification)}),r(x.priority,{size:16,bold:true,color:pc(x.priority)}),r(x.recommendation,{size:16})]);
reg.push(T(W2,[450,1700,1500,2900,3300,900,800,3020],['#','الصفحة / الرابط','الموقع','النص الحالي (حرفيًا)','نوع الملاحظة والوصف','التصنيف','الأولوية','التصحيح أو التوصية المقترحة'],rows.map(rr=>rr.map(c=>Array.isArray(c)?c:[c])),{center:[0,5,6],cantSplit:false}));
// ---------- stats etc (portrait)
const axes=['دقة المعلومات','لغوي ونحوي','الاتساق','تجربة المستخدم','وظيفي وتقني','تنظيمي'];const cls=['تصحيح مطلوب','توصية تحسين','متابعة وتحقق'];const pris=['عالية','متوسطة','منخفضة'];
const cross=cls.map(c=>[c,...pris.map(p=>ROWS.filter(x=>x.classification===c&&x.priority===p).length),ROWS.filter(x=>x.classification===c).length]);
cross.push(['المجموع',...pris.map(p=>PRI[p]),N]);
const axr=axes.map(a=>[a,...pris.map(p=>ROWS.filter(x=>x.axis===a&&x.priority===p).length),AX[a]||0]);axr.push(['المجموع',...pris.map(p=>PRI[p]),N]);
const tail=[
 H1('4. الإحصاء الختامي'),
 P(`العدد الإجمالي للعناصر المرصودة: ${N} ملاحظة، وهو مطابق لعدد صفوف سجل الملاحظات. وقد نتج هذا العدد عن دمج 271 ملاحظة أولية متحقق منها في ملاحظات موحّدة دون تكرار.`),
 H2('4.1 حسب التصنيف والأولوية'),
 T(W1,[3000,1500,1500,1500,1500],['التصنيف','عالية','متوسطة','منخفضة','المجموع'],cross,{center:[1,2,3,4],totalLast:true,boldCol:0,size:19}),
 H2('4.2 حسب المحور والأولوية'),
 T(W1,[3000,1500,1500,1500,1500],['المحور','عالية','متوسطة','منخفضة','المجموع'],axr,{center:[1,2,3,4],totalLast:true,boldCol:0,size:19}),
 H2('4.3 الملاحظات عالية الأولوية'),
 T(W1,[500,2600,6500],['#','الصفحة','الملاحظة'],high.map(x=>[String(ROWS.indexOf(x)+1),pname(x.page_id),x.description]),{center:[0],size:17}),
 H1('5. عوائق الإغلاق والحلول الجذرية'),
 P('العوائق التالية تمنع اعتماد الصفحة نهائيًا. ولكلٍّ منها حل جذري يعالج السبب لا العَرَض، حتى لا تتكرر المشكلة في الدورة القادمة:'),
 T(W1,[2800,3600,3200],['العائق','الحل الجذري المقترح','الجهة المعنية'],[
  ['غياب دورة قبول سارية منشورة؛ تقويم خريف 2026 منتهٍ، وبوابة التقديم بلا مواعيد','اعتماد مصدر واحد لتقويم القبول تُغذّى منه الصفحات والبوابة، مع إجراء تحديث إلزامي قبل كل دورة، ونشر إعلان مؤقت بحالة القبول فورًا','مكتب القبول، تقنية المعلومات'],
  ['تعارض رسوم التقديم بين الصفحات (500 / 950 / 1,000 / 1,150 ريالًا) وغموض المعالجة الضريبية','جدول رسوم رسمي واحد معتمد من الإدارة المالية، تحيل إليه جميع صفحات القبول بدل تكرار المبالغ فيها','الإدارة المالية، مكتب القبول'],
  ['تعارض شروط القبول (SAT II، بديل SAT 1200، الحدود الموزونة، قوائم التخصصات ذات المتطلبات الخاصة)','مصفوفة شروط قبول موحّدة لكل فئة وبرنامج وفصل، تُعتمد من مالك سياسة القبول وتُنشر من مصدر واحد','مكتب القبول، الكليات'],
  ['تعارض متطلبات اللغة للدراسات العليا، ونص يشير إلى جامعة أخرى في صفحة EMGMS','قرار من عمادة الدراسات العليا بمتطلب لغة لكل برنامج، وإزالة النص الخارجي فورًا، وربط كل برنامج بنموذج تقديم خاص به','عمادة الدراسات العليا، كلية الهندسة'],
  ['شروط القبول منشورة في صفحة لا يراها المتقدم (/apply تُحوِّل فورًا)، ومسار التقديم غير واضح حسب الفئة','صفحة تقديم مرئية تبدأ باختيار فئة المتقدم وتعرض الشروط والرسوم والموعد وقناة التقديم الصحيحة','مكتب القبول، الويب'],
  ['غياب قناة تواصل رسمية للقبول وإشعار خصوصية في نموذج الاستفسار والبوابة','صفحة تواصل رسمية لمكتب القبول (بريد وهاتف وساعات عمل)، وإشعار خصوصية بعد مراجعة الامتثال لنظام حماية البيانات الشخصية','مكتب القبول، الشؤون القانونية'],
  ['أدلة وملفات قديمة (دليل التقديم 2018، دليل Aptis 2017) وصفحات قديمة ما زالت منشورة','سحب الملفات القديمة أو استبدالها، وإعادة توجيه الصفحات القديمة، ومراجعة سنوية لمخزون الملفات','مكتب القبول، الويب'],
  ['غياب مالك ومعتمد وتاريخ نفاذ لكل قيمة حرجة، وتكرار طلبات التعديل دون أثر اعتماد موثق','حوكمة محتوى: مالك ومعتمد وتاريخ نفاذ لكل قيمة، ومسار طلب تعديل ← اعتماد ← نشر ← قراءة راجعة للصفحة الحية','الراعي التنفيذي، مكتب القبول'],
 ],{size:17,boldCol:0}),
 H1('6. ملاحظات خارج النطاق (للعلم فقط)'),
 P('رُصدت أثناء الفحص صفحات خارج قسم القبول أو صفحات قديمة غير مرتبطة بصفحة مكتب القبول. لم تدخل في السجل والإحصاء، وتُذكر هنا لأنها قد تضلل المتقدم عبر محركات البحث أو القوائم العامة:',{size:20}),
 B('صفحة قديمة للقبول «freshman_admission» ما زالت منشورة بأوزان قديمة (30/50/20)، وصفحة تحويل قديمة تشترط IELTS بدرجة 5.0 لكل مهارة، وصفحة دورة IELTS لعام 2019.'),
 B('جداول السداد والأسئلة الشائعة للرسوم على رسوم 2025/2026، وتعارض في عبارات الاسترداد بصفحة طرق السداد.'),
 B('تراكم 13 تقويمًا أكاديميًا قديمًا وملفاتها، وأخبار قديمة (2010، 1435/1436هـ)، ورابط إلى خادم داخلي (http://web1:8066/...) في صفحة مكتب التسجيل.'),
 B('الصفحة الرئيسية للجامعة: فقرة NCAAA مكررة، و«STUDENT ORIENTATION 2027-2028»، و«THE Ranking 2024»، واختلاف سنوات حقوق النشر.'),
 B('صفحة Study @ PMU: رابط التقويم الأكاديمي يفتح تقويم 2023/2024 رغم نشر تقويم 2026/2027، ولا تعرض حالة دورة القبول.'),
 H1('7. منهجية الإعداد والأدوات المستخدمة'),
 B([r('أدوات التصفح والفحص: ',{bold:true}),r('متصفح Chromium آلي (Playwright) بعرض جوال 390 بكسل لقراءة النص المعروض والمحتوى المخفي في التبويبات، وقراءة مصدر HTML لصفحة /apply، واستخراج نص ملفات PDF (pdftotext)، وفحص آلي لحالة 565 رابطًا وسمة اللغة والنص البديل للصور والعرض على الجوال، وتدقيق إملائي آلي مساند.')]),
 B([r('التحقق: ',{bold:true}),r('كل ملاحظة مدعومة بنص منقول حرفيًا تحقق منه آليًا مقابل النص الملتقط، وأُعيد التحقق من الحقائق الجوهرية على الموقع الحي في 11 أكتوبر 2026. وفي 13 أكتوبر 2026 قُوبلت الملاحظات بحزمة معالجة محتوى شاملة للموقع (530 إجراءً)؛ يقع منها 73 إجراءً فقط ضمن نطاق صفحة مكتب القبول، وكان أغلبها مغطًّى في هذا السجل، فأُضيفت ثلاث ملاحظات جديدة بعد التحقق (اثنتان مؤكدتان وواحدة للمتابعة) وعُزّز بند دليل التقديم الإلكتروني. وأُعدّت المراجعة بمساعدة أدوات الذكاء الاصطناعي (Claude) في القراءة والمطابقة والصياغة، مع إخضاع النتائج لتحقق مستقل من الأدلة.')]),
 B([r('حدود المراجعة: ',{bold:true}),r('لم يُختبر عرض سطح المكتب لأن الموقع يحجب الوصول الآلي بهذا الوضع؛ ولم تُنسخ قائمة الموظفين لاحتوائها بيانات شخصية؛ وتعذّر الوصول إلى بوابتي مكتب الدعم الفني وBanner من بيئة الفحص فلم يُحكم على حالتهما؛ ولم يُقدَّم أي طلب قبول أو دفع، ولم تُختبر نماذج الإرسال فعليًا؛ ولم يُراجَع إلا ما يظهر دون تفاعل إضافي كالنوافذ المنبثقة.')]),
 B([r('ما يحتاج تحققًا: ',{bold:true}),r(`${CL['متابعة وتحقق']} بندًا مصنّفة «متابعة وتحقق» لاعتمادها على قرار مالك السياسة أو على معلومة خارجية لم يمكن تأكيدها من المحتوى المنشور، ولم تُعدّ مخالفات.`)]),
 B([r('المصطلحات: ',{bold:true}),r('«تصحيح مطلوب» خطأ أو تعارض ثابت في المحتوى؛ «توصية تحسين» تحسين للوضوح أو التجربة؛ «متابعة وتحقق» بند يحتاج تأكيدًا من الجهة المالكة قبل الحكم عليه.')]),
];
const mk=(o)=>({properties:{page:{size:o.land?{width:11906,height:16838,orientation:PageOrientation.LANDSCAPE}:{width:11906,height:16838},margin:{top:900,bottom:850,left:1000,right:1000}}},
 headers:{default:new Header({children:[new Paragraph({bidirectional:true,alignment:AlignmentType.LEFT,children:[r('تقرير المراجعة الشاملة لصفحات مكتب القبول | داخلي',{size:16,color:GREY})]})]})},
 footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({font:FONT,size:16,color:GREY,children:['',PageNumber.CURRENT]})]})]})},children:o.children});
const doc=new Document({creator:'Nader Alfarhan',title:'تقرير المراجعة الشاملة لصفحات مكتب القبول',
 styles:{default:{document:{run:{font:FONT,size:22}}}},
 numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.RIGHT,style:{paragraph:{indent:{right:400,hanging:260}}}}]}]},
 sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1000,bottom:900,left:1100,right:1100}}},children:cover},mk({children:body}),mk({land:true,children:reg}),mk({children:tail})]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(process.argv[2],b);console.log('rows',N,CL,PRI)});
