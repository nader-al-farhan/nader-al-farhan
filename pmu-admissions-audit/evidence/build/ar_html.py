import json,html,collections,sys
D='final_review/'
R=json.load(open(D+'final_rows.json'));PM=json.load(open(D+'pagemap.json'))
ORDER=['P00','P03','P04','P05','P06','P07','P08','P38','Shared menu','P09','P24','P25','P26','P27','P28','P29','P30','P31','P10','P11','P12','P13','P14','P15','P16','P17','P18','P19','P20','P21','P22','P23','P32','P33','P34','P35','P36','P37']
PR={'عالية':0,'متوسطة':1,'منخفضة':2}
R.sort(key=lambda a:(ORDER.index(a['page_id']),PR[a['priority']]))
N=len(R);CL=collections.Counter(r['classification'] for r in R);PRI=collections.Counter(r['priority'] for r in R);AX=collections.Counter(r['axis'] for r in R)
import re
def e(x):
    parts=re.split(r'([A-Za-z0-9"“(/\'][^\u0600-\u06FF]*[A-Za-z0-9"”).%/\'])',x)
    out=[]
    for i,pt in enumerate(parts):
        if i%2==1 and re.search(r'[A-Za-z]',pt): out.append('<bdi>'+html.escape(pt)+'</bdi>')
        else: out.append(html.escape(pt))
    return ''.join(out)
esc=html.escape
pn=lambda i:'القائمة الجانبية لصفحات القبول' if i=='Shared menu' else PM[i]['ar']
short=lambda u:u.split(';')[0].strip().replace('https://www.','').replace('https://','')
pcol={'عالية':'#C00000','متوسطة':'#B7791F','منخفضة':'#2F855A'};ccol={'تصحيح مطلوب':'#C00000','توصية تحسين':'#2E75B6','متابعة وتحقق':'#B7791F'}
font='/root/.fonts/'
css=f"""
@font-face{{font-family:Naskh;src:url(file://{font}NotoNaskhArabic_400Regular.ttf);font-weight:400}}
@font-face{{font-family:Naskh;src:url(file://{font}NotoNaskhArabic_700Bold.ttf);font-weight:700}}
@page{{size:A4;margin:18mm 16mm 16mm 16mm;@bottom-center{{content:counter(page);font-size:9pt;color:#595959}}}}
@page land{{size:A4 landscape;margin:14mm 12mm 14mm 12mm}}
@page cover{{margin:0}}
body{{font-family:Naskh,'DejaVu Sans',sans-serif;direction:rtl;color:#262626;font-size:10.5pt;line-height:1.75;margin:0}}
.cover{{page:cover;height:297mm;padding:55mm 22mm 0 22mm;box-sizing:border-box;background:linear-gradient(180deg,#fff 0,#fff 78%,#EAF1FB 78%)}}
.cover .uni{{color:#2E75B6;font-weight:700;font-size:14pt}} .cover .dept{{color:#595959;font-size:12pt;margin-bottom:28mm}}
.cover h1{{font-size:27pt;color:#1F3864;margin:0 0 4mm}} .cover .sub{{font-size:15pt;color:#1F3864;border-bottom:3px solid #2E75B6;padding-bottom:5mm;margin-bottom:6mm}}
.cover .scope{{color:#595959;font-size:11pt;margin-bottom:24mm}}
h2{{color:#1F3864;font-size:16pt;border-bottom:2px solid #2E75B6;padding-bottom:2mm;margin:7mm 0 3mm;break-after:avoid}}
h3{{color:#2E75B6;font-size:12.5pt;margin:5mm 0 2mm;break-after:avoid}}
p{{text-align:justify;margin:0 0 2.5mm}}
table{{border-collapse:collapse;width:100%;margin:2mm 0 4mm}} th{{background:#1F3864;color:#fff;font-weight:700;padding:2mm;font-size:9.5pt}}
td{{border:1px solid #BFBFBF;padding:1.6mm 2mm;vertical-align:top;font-size:9.5pt}} tr:nth-child(even) td{{background:#EAF1FB}}
thead{{display:table-header-group}} tr{{break-inside:avoid}}
.ltr{{direction:ltr;text-align:left;unicode-bidi:isolate;font-family:'DejaVu Sans',sans-serif;font-size:8.3pt;color:#333}}
.url{{direction:ltr;unicode-bidi:isolate;font-family:'DejaVu Sans';font-size:7.4pt;color:#595959;word-break:break-all}}
.c{{text-align:center}} .b{{font-weight:700}} .kpis{{display:flex;gap:3mm;margin:3mm 0 4mm}}
.kpi{{flex:1;border:1px solid #BFBFBF;border-top:4px solid #2E75B6;background:#F7F9FC;text-align:center;padding:2mm}} .kpi .v{{font-size:20pt;font-weight:700;color:#1F3864;line-height:1.3}} .kpi .l{{font-size:8.5pt;color:#595959}}
.reg{{page:land}} .reg td{{font-size:8.4pt;line-height:1.5}} .reg .ltr{{font-size:7.8pt}} table{{table-layout:fixed}} .reg th{{font-size:8.8pt}}
.tot td{{background:#D9E2F3 !important;font-weight:700}} ul{{margin:0 0 2mm;padding-right:6mm}} li{{margin-bottom:1.5mm;text-align:justify}}
.verdict{{color:#C00000;font-weight:700}} .muted{{color:#595959;font-size:9pt}}
.doc td:first-child{{font-weight:700;width:30%}}
"""
def tr(cells,cls=''): return '<tr%s>'%(f' class="{cls}"' if cls else '')+''.join(cells)+'</tr>'
td=lambda x,c='':f'<td class="{c}">{x}</td>'
H=[]
H.append(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>تقرير المراجعة الشاملة لصفحات مكتب القبول</title><style>{css}</style></head><body>')
H.append(f'''<section class="cover"><div class="uni">جامعة الأمير محمد بن فهد</div><div class="dept">مكتب القبول</div>
<h1>تقرير المراجعة الشاملة لصفحات مكتب القبول</h1><div class="sub">رصد لغوي ومعلوماتي ووظيفي وتنظيمي للمحتوى المنشور</div>
<div class="scope">صفحة مكتب القبول <span class="url" style="font-size:9pt">https://pmu.edu.sa/admission/admission</span> وجميع الصفحات والملفات المرتبطة بها ضمن قسم القبول</div>
<table class="doc"><thead><tr><th colspan="2">ضبط الوثيقة</th></tr></thead><tbody>
{tr([td('مقدَّم إلى'),td('الأستاذ راضي الخالدي – مدير القبول')])}{tr([td('إعداد'),td('نادر الفرحان – شؤون الطلاب')])}
{tr([td('المرجع'),td('استكمال لسلسلة البريد «comments on Admission pages»')])}{tr([td('تاريخ الرصد'),td('10 أكتوبر 2026، مع إعادة تحقق في 11 أكتوبر 2026')])}
{tr([td('حالة الوثيقة'),td('الإصدار 1.0 – للمراجعة والاعتماد')])}{tr([td('التصنيف'),td('داخلي')])}</tbody></table></section>''')
high=[r for r in R if r['priority']=='عالية']
H.append('<h2>1. الملخص التنفيذي</h2>')
H.append('<p>بناءً على طلب مدير القبول، رُوجع المحتوى المنشور لصفحة مكتب القبول وجميع الصفحات المرتبطة بها ضمن قسم القبول، وعددها 36 صفحة بما فيها بوابة التقديم، إضافة إلى ملفين مرفقين بصيغة PDF وثلاث صفحات رسوم رسمية استُخدمت مرجعًا للتحقق. وقُرئت كل وحدة محتوى سطرًا بسطر (1,248 سطرًا) على ستة محاور: اللغة، ودقة المعلومات، والجانب الوظيفي، والتنظيم، والاتساق، وتجربة المستخدم.</p>')
H.append(f'<div class="kpis"><div class="kpi"><div class="v">36</div><div class="l">صفحة فُحصت سطرًا بسطر</div></div><div class="kpi"><div class="v">1,248</div><div class="l">سطر محتوى مُدقَّق</div></div><div class="kpi"><div class="v">{N}</div><div class="l">ملاحظة موحّدة</div></div><div class="kpi"><div class="v" style="color:#C00000">{PRI["عالية"]}</div><div class="l">ملاحظات عالية الأولوية</div></div></div>')
H.append(f'<p>رُصدت {N} ملاحظة موحّدة بعد دمج المتكرر: {CL["تصحيح مطلوب"]} تصحيحًا مطلوبًا، و{CL["توصية تحسين"]} توصية تحسين، و{CL["متابعة وتحقق"]} بندًا للمتابعة والتحقق؛ منها {PRI["عالية"]} ملاحظات عالية الأولوية، و{PRI["متوسطة"]} متوسطة، و{PRI["منخفضة"]} منخفضة.</p>')
H.append('<p><b>أبرز ثلاث أولويات:</b> (1) لا يجد المتقدم دورة قبول سارية؛ فالتقويم الوحيد لخريف 2026 وجميع مواعيده منتهية، وبوابة التقديم لا تعرض أي مواعيد. (2) تعارض رسوم التقديم بين الصفحات (500 ريال غير شاملة الضريبة مقابل 950 ريالًا شاملة للمحولين والزائرين الدوليين، و1,000 مقابل 1,150 ريالًا لكلية الطب). (3) تعارض شروط القبول واللغة، ومنها اشتراط SAT II الموقوف منذ 2021 للطلاب الدوليين، واختلاف درجة IELTS المطلوبة في عدد من برامج الدراسات العليا، ووجود نص يشير إلى جامعة أخرى في صفحة EMGMS.</p>')
H.append('<p><b>الحكم:</b> <span class="verdict">الصفحة غير جاهزة للاعتماد النهائي إلى أن تُعالَج عوائق الإغلاق الواردة في القسم 5.</span></p>')
H.append('<h2>2. نطاق الرصد</h2><p>شمل الرصد صفحة مكتب القبول وكل رابط داخلي مباشر في حاويات القبول، وما يتفرع منها مما يلزم لفهم شرط أو رسم أو إجراء، والملفات المرفقة المرتبطة مباشرة بالقبول:</p>')
rows=[]
for i in sorted(k for k in PM if k.startswith('P') and k[1:].isdigit()):
    st='فُحص الرابط ووجهته فقط (لم يُنسخ المحتوى لاحتوائه أسماء موظفين)' if i=='P06' else ('خارج النطاق (صفحة عامة) – ذُكرت إحالاتها فقط' if i in('P01','P02') else 'فُحصت سطرًا بسطر')
    rows.append(tr([td(i,'c'),td(e(PM[i]['ar'] or PM[i]['title'])),td(f'<span class="url">{e(short(PM[i]["url"]))}</span>'),td(st)]))
rows.append(tr([td('PDF','c'),td('دليل المرشح لاختبار Aptis (2017)'),td('<span class="url">pmu.edu.sa/Attachments/Admission/PDF/Appendix 3.3 (Aptis Candidate Guide).pdf</span>'),td('فُحص (50 صفحة)')]))
rows.append(tr([td('PDF','c'),td('دليل التقديم الإلكتروني Web Admission Guide (2018)'),td('<span class="url">pmu.edu.sa/Attachments/Admission/Images/PDF/Web-Admission-Guide-v2-2_20-12-18.pdf</span>'),td('فُحص (21 صفحة)')]))
rows.append(tr([td('مرجع','c'),td('صفحات الرسوم الرسمية (رسوم أخرى، رسوم البرنامج الطبي، رسوم البكالوريوس 2026/2027)'),td('<span class="url">pmu.edu.sa/admission/student_fees_tf_ro …</span>'),td('مرجع تحقق للرسوم')]))
H.append('<table><thead><tr><th style="width:7%">المعرّف</th><th style="width:30%">الصفحة</th><th style="width:43%">الرابط</th><th>حالة الفحص</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>')
H.append('<p class="muted">اكتُشفت 39 صفحة ضمن النطاق: فُحصت منها 36 صفحة سطرًا بسطر، وصفحة واحدة (قائمة الموظفين) فُحص رابطها فقط، وصفحتان عامتان خارج قسم القبول ذُكرت إحالاتهما للعلم فقط.</p>')
# register
H.append(f'<section class="reg"><h2>3. سجل الملاحظات</h2><p class="muted">يعرض السجل {N} ملاحظة مرتبة حسب الصفحة ثم الأولوية. النص الحالي منقول حرفيًا كما هو منشور (وغالبه بالإنجليزية)، وما بين معقوفين [ ] يحدد الصفحة المصدر عند المقارنة بين أكثر من صفحة.</p>')
H.append('<table><thead><tr><th style="width:3%">#</th><th style="width:10%">الصفحة / الرابط</th><th style="width:10%">الموقع</th><th style="width:19%">النص الحالي (حرفيًا)</th><th style="width:23%">نوع الملاحظة والوصف</th><th style="width:6%">التصنيف</th><th style="width:5%">الأولوية</th><th style="width:24%">التصحيح أو التوصية المقترحة</th></tr></thead><tbody>')
for i,r in enumerate(R,1):
    H.append(tr([td(str(i),'c'),td(f'<b>{e(pn(r["page_id"]))}</b><br><span class="url">{e(short(r["url"]))}</span>'),td(e(r['location'])),td(f'<div class="ltr">{esc(r["current_text"])}</div>'),
      td(f'<b>{e(r["type"])}</b> <span class="muted">({e(r["axis"])})</span><br>{e(r["description"])}'),td(f'<b style="color:{ccol[r["classification"]]}">{e(r["classification"])}</b>','c'),td(f'<b style="color:{pcol[r["priority"]]}">{e(r["priority"])}</b>','c'),td(e(r['recommendation']))]))
H.append('</tbody></table></section>')
# stats
pris=['عالية','متوسطة','منخفضة']
def stat(title,key,labels):
    s=f'<h3>{title}</h3><table><thead><tr><th>البند</th>'+''.join(f'<th>{p}</th>' for p in pris)+'<th>المجموع</th></tr></thead><tbody>'
    for l in labels:
        c=[sum(1 for r in R if r[key]==l and r['priority']==p) for p in pris]
        s+=tr([td(f'<b>{l}</b>')]+[td(str(x),'c') for x in c]+[td(f'<b>{sum(c)}</b>','c')])
    s+=tr([td('المجموع')]+[td(str(PRI[p]),'c') for p in pris]+[td(str(N),'c')],'tot')+'</tbody></table>';return s
H.append(f'<h2>4. الإحصاء الختامي</h2><p>العدد الإجمالي للعناصر المرصودة: <b>{N}</b> ملاحظة، وهو مطابق لعدد صفوف سجل الملاحظات. وقد نتج هذا العدد عن دمج 271 ملاحظة أولية متحقق منها في ملاحظات موحّدة دون تكرار.</p>')
H.append(stat('4.1 حسب التصنيف والأولوية','classification',['تصحيح مطلوب','توصية تحسين','متابعة وتحقق']))
H.append(stat('4.2 حسب المحور والأولوية','axis',['دقة المعلومات','لغوي ونحوي','الاتساق','تجربة المستخدم','وظيفي وتقني','تنظيمي']))
H.append('<h3>4.3 الملاحظات عالية الأولوية</h3><table><thead><tr><th style="width:6%">#</th><th style="width:24%">الصفحة</th><th>الملاحظة</th></tr></thead><tbody>'+''.join(tr([td(str(R.index(r)+1),'c'),td(e(pn(r['page_id']))),td(e(r['description']))]) for r in high)+'</tbody></table>')
B=[('غياب دورة قبول سارية منشورة؛ تقويم خريف 2026 منتهٍ، وبوابة التقديم بلا مواعيد','اعتماد مصدر واحد لتقويم القبول تُغذّى منه الصفحات والبوابة، مع إجراء تحديث إلزامي قبل كل دورة، ونشر إعلان مؤقت بحالة القبول فورًا','مكتب القبول، تقنية المعلومات'),
('تعارض رسوم التقديم بين الصفحات (500 / 950 / 1,000 / 1,150 ريالًا) وغموض المعالجة الضريبية','جدول رسوم رسمي واحد معتمد من الإدارة المالية، تحيل إليه جميع صفحات القبول بدل تكرار المبالغ فيها','الإدارة المالية، مكتب القبول'),
('تعارض شروط القبول (SAT II، بديل SAT 1200، الحدود الموزونة، قوائم التخصصات ذات المتطلبات الخاصة)','مصفوفة شروط قبول موحّدة لكل فئة وبرنامج وفصل، يعتمدها مالك سياسة القبول وتُنشر من مصدر واحد','مكتب القبول، الكليات'),
('تعارض متطلبات اللغة للدراسات العليا، ونص يشير إلى جامعة أخرى في صفحة EMGMS','قرار من عمادة الدراسات العليا بمتطلب لغة لكل برنامج، وإزالة النص الخارجي فورًا، وربط كل برنامج بنموذج تقديم خاص به','عمادة الدراسات العليا، كلية الهندسة'),
('شروط القبول منشورة في صفحة لا يراها المتقدم (/apply تُحوِّل فورًا)، ومسار التقديم غير واضح حسب الفئة','صفحة تقديم مرئية تبدأ باختيار فئة المتقدم وتعرض الشروط والرسوم والموعد وقناة التقديم الصحيحة','مكتب القبول، الويب'),
('غياب قناة تواصل رسمية للقبول وإشعار خصوصية في نموذج الاستفسار والبوابة','صفحة تواصل رسمية لمكتب القبول (بريد وهاتف وساعات عمل)، وإشعار خصوصية بعد مراجعة الامتثال لنظام حماية البيانات الشخصية','مكتب القبول، الشؤون القانونية'),
('أدلة وملفات قديمة (دليل التقديم 2018، دليل Aptis 2017) وصفحات قديمة ما زالت منشورة','سحب الملفات القديمة أو استبدالها، وإعادة توجيه الصفحات القديمة، ومراجعة سنوية لمخزون الملفات','مكتب القبول، الويب'),
('غياب مالك ومعتمد وتاريخ نفاذ لكل قيمة حرجة، وتكرار طلبات التعديل دون أثر اعتماد موثّق','حوكمة محتوى: مالك ومعتمد وتاريخ نفاذ لكل قيمة، ومسار: طلب تعديل ← اعتماد ← نشر ← قراءة راجعة للصفحة الحية','الراعي التنفيذي، مكتب القبول')]
H.append('<h2>5. عوائق الإغلاق والحلول الجذرية</h2><p>العوائق التالية تمنع اعتماد الصفحة نهائيًا، ولكلٍّ منها حل جذري يعالج السبب لا العَرَض، حتى لا تتكرر المشكلة في الدورة القادمة:</p><table><thead><tr><th style="width:5%">#</th><th style="width:33%">العائق</th><th style="width:40%">الحل الجذري المقترح</th><th>الجهة المعنية</th></tr></thead><tbody>'+''.join(tr([td(str(i),'c'),td(f'<b>{a}</b>'),td(b),td(c)]) for i,(a,b,c) in enumerate(B,1))+'</tbody></table>')
H.append('''<h2>6. ملاحظات خارج النطاق (للعلم فقط)</h2><p>رُصدت أثناء الفحص صفحات خارج قسم القبول أو صفحات قديمة غير مرتبطة بصفحة مكتب القبول. لم تدخل في السجل والإحصاء، وتُذكر هنا لأنها قد تضلل المتقدم عبر محركات البحث أو القوائم العامة:</p><ul>
<li>صفحة قبول قديمة («freshman_admission») ما زالت منشورة بأوزان قديمة (30/50/20)، وصفحة تحويل قديمة تشترط IELTS بدرجة 5.0 لكل مهارة، وصفحة دورة IELTS لعام 2019.</li>
<li>جداول السداد والأسئلة الشائعة للرسوم على رسوم 2025/2026، وتعارض في عبارات الاسترداد في صفحة طرق السداد.</li>
<li>تراكم 13 تقويمًا أكاديميًا قديمًا وملفاتها، وأخبار قديمة (2010، 1435/1436هـ)، ورابط إلى خادم داخلي في صفحة مكتب التسجيل.</li>
<li>الصفحة الرئيسية للجامعة: فقرة NCAAA مكررة، وعبارة «STUDENT ORIENTATION 2027-2028»، و«THE Ranking 2024»، واختلاف سنوات حقوق النشر.</li>
<li>صفحة Study @ PMU: رابط التقويم الأكاديمي يفتح تقويم 2023/2024 رغم نشر تقويم 2026/2027، ولا تعرض حالة دورة القبول.</li></ul>''')
H.append(f'''<h2>7. منهجية الإعداد والأدوات المستخدمة</h2><ul>
<li><b>أدوات التصفح والفحص:</b> متصفح Chromium آلي (Playwright) بعرض جوال 390 بكسل لقراءة النص المعروض والمحتوى المخفي في التبويبات، وقراءة مصدر HTML لصفحة ‎/apply‎، واستخراج نصوص ملفات PDF، وفحص آلي لحالة 565 رابطًا ولسمة اللغة والنص البديل للصور والعرض على الجوال، وتدقيق إملائي آلي مساند.</li>
<li><b>التحقق:</b> كل ملاحظة مدعومة بنص منقول حرفيًا جرى التحقق منه مقابل النص الملتقط، وأُعيد التحقق من الحقائق الجوهرية على الموقع الحي في 11 أكتوبر 2026. وفي 13 أكتوبر 2026 قُوبلت الملاحظات بحزمة معالجة محتوى شاملة للموقع (530 إجراءً)؛ يقع منها 73 إجراءً فقط ضمن نطاق صفحة مكتب القبول، وكان أغلبها مغطًّى في هذا السجل، فأُضيفت ثلاث ملاحظات جديدة بعد التحقق (اثنتان مؤكدتان وواحدة للمتابعة) وعُزّز بند دليل التقديم الإلكتروني. وأُعدّت المراجعة بمساعدة أدوات الذكاء الاصطناعي (Claude) في القراءة والمطابقة والصياغة، مع إخضاع النتائج لتحقق مستقل من الأدلة.</li>
<li><b>حدود المراجعة:</b> لم يُختبر عرض سطح المكتب لأن الموقع يحجب الوصول الآلي بهذا الوضع؛ ولم تُنسخ قائمة الموظفين لاحتوائها بيانات شخصية؛ وتعذّر الوصول إلى بوابتي الدعم الفني وBanner من بيئة الفحص فلم يُحكم على حالتهما؛ ولم يُقدَّم أي طلب قبول أو دفع، ولم تُختبر نماذج الإرسال فعليًا؛ ولم يُراجَع إلا ما يظهر دون تفاعل إضافي كالنوافذ المنبثقة.</li>
<li><b>ما يحتاج تحققًا:</b> {CL["متابعة وتحقق"]} بندًا مصنّفة «متابعة وتحقق» لاعتمادها على قرار مالك السياسة أو على معلومة خارجية لم يمكن تأكيدها من المحتوى المنشور، ولم تُعدّ مخالفات.</li>
<li><b>المصطلحات:</b> «تصحيح مطلوب» خطأ أو تعارض ثابت في المحتوى؛ «توصية تحسين» تحسين للوضوح أو التجربة؛ «متابعة وتحقق» بند يحتاج تأكيدًا من الجهة المالكة قبل الحكم عليه.</li></ul>''')
H.append('</body></html>')
open(D+'report.html','w').write('\n'.join(H));print('html ok',N)
