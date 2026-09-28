"""Author the blueprint data (ia.json). Every legacy link, channel and pain point is
traceable to a page ID (P..) or finding (F-..) in the audit registers."""
import json, pathlib
L = lambda ar, en: {"ar": ar, "en": en}

sitemap = [
 {"id":"home","parent":None,"path":"/admissions","t":L("القبول","Admissions"),"type":"hub",
  "does":L("شريط حالة الدورة، و«من أنت؟» بستة مسارات، وأربعة إجراءات سريعة، والتواصل","Cycle-status bar, “Who are you?” with six routes, four quick actions, contact"),
  "feeds":["intake_status","application_channel","contacts"],"replaces":["P01","P23"],"fixes":["F-15","F-08","F-11"]},
 {"id":"ug","parent":"home","path":"/admissions/undergraduate","t":L("البكالوريوس","Undergraduate"),"type":"section",
  "does":L("اختيار المسار الجامعي ومقارنة سريعة بين المسارات","Choose the undergraduate route, with a short comparison"),"feeds":[],"replaces":["P02"],"fixes":["F-15"]},
 {"id":"ug_hs","parent":"ug","path":"/admissions/undergraduate/high-school","t":L("خريج الثانوية في المملكة","High-school graduate in KSA"),"type":"route",
  "does":L("صفحة مسار واحدة تدمج Freshman وDirect ومتطلبات التخصصات، وتعرض المكوّنات الستة","One route page merging Freshman, Direct and major requirements; shows the six components"),
  "feeds":["hs_gpa_min","gat_min","tahseely_rule","composite_formula","composite_minimum","english_ug_direct","test_validity","application_fee","tuition_ug","vat_statement","required_documents","application_channel"],
  "replaces":["P03","P04","P19","P20"],"fixes":["F-01","F-04","F-05","F-09","F-13","F-18"]},
 {"id":"ug_intl","parent":"ug","path":"/admissions/undergraduate/international","t":L("طالب دولي دون إقامة","International (no Saudi residence)"),"type":"route",
  "does":L("المسار الدولي مع قناة «ادرس في السعودية» ومعادلة الشهادات","International route with Study in Saudi and certificate equivalency"),
  "feeds":["hs_gpa_min","tahseely_rule","english_ug_direct","application_fee","tuition_ug","vat_statement","required_documents","application_channel"],"replaces":["P18","P52"],"fixes":["F-02","F-05"]},
 {"id":"ug_transfer","parent":"ug","path":"/admissions/undergraduate/transfer","t":L("التحويل من جامعة أخرى","Transfer from another university"),"type":"route",
  "does":L("شروط التحويل ومعادلة المواد في صفحة واحدة","Transfer conditions and credit transfer on one page"),
  "feeds":["english_ug_direct","application_fee","tuition_ug","required_documents","application_channel"],"replaces":["P17","P62"],"fixes":["F-02","F-16"]},
 {"id":"ug_med","parent":"ug","path":"/admissions/undergraduate/medicine","t":L("كلية الطب","College of Medicine"),"type":"route",
  "does":L("الشروط والمعادلة والمدة والتكلفة الإجمالية وحجز المقعد في مكان واحد","Requirements, formula, duration, total cost and seat reservation in one place"),
  "feeds":["composite_minimum","tahseely_rule","application_fee","tuition_medicine","refund_policy","application_channel","required_documents"],"replaces":["P09","P12"],"fixes":["F-03","F-07","F-20","F-23"]},
 {"id":"ug_prep","parent":"ug","path":"/admissions/undergraduate/preparatory","t":L("السنة التحضيرية","Preparatory Program"),"type":"route",
  "does":L("القبول في التحضيرية والانتقال منها إلى البكالوريوس","Admission to Prep and progression to the degree"),
  "feeds":["english_ug_direct","test_validity","tuition_ug"],"replaces":["P25","P26"],"fixes":["F-26","F-28"]},
 {"id":"ug_visit","parent":"ug","path":"/admissions/undergraduate/visiting","t":L("طالب زائر","Visiting student"),"type":"route",
  "does":L("شروط الزيارة والمدة والرسوم","Visiting conditions, duration and fees"),"feeds":["english_ug_direct","application_fee","application_channel"],"replaces":["P27"],"fixes":["F-17","F-16"]},
 {"id":"grad","parent":"home","path":"/admissions/graduate","t":L("الدراسات العليا","Graduate"),"type":"section",
  "does":L("قائمة البرامج من سجل البرامج الموحّد، مع مقارنة الشروط والرسوم","Programme list from the single programme register, with requirements and fees compared"),
  "feeds":["programme_register","english_grad","application_fee"],"replaces":["P33"],"fixes":["F-25"]},
 {"id":"grad_prog","parent":"grad","path":"/admissions/graduate/{programme}","t":L("صفحة البرنامج (قالب واحد × 11)","Programme page (one template × 11)"),"type":"template",
  "does":L("قالب واحد لكل برامج الدراسات العليا؛ لا قسم فارغ يُنشر","One template for all graduate programmes; no empty section can be published"),
  "feeds":["english_grad","application_fee","programme_register","required_documents"],"replaces":["P34","P35","P36","P37","P38","P39","P40","P41","P42","P43","P44"],"fixes":["F-21","F-26","F-27"]},
 {"id":"req","parent":"home","path":"/admissions/requirements/english-and-tests","t":L("الإنجليزية والاختبارات","English & tests"),"type":"reference",
  "does":L("جدول واحد لـIELTS وTOEFL (0–120 و1–6) وAptis وSAT مع الصلاحية","One table for IELTS, TOEFL (0–120 and 1–6), Aptis and SAT, with validity"),
  "feeds":["english_ug_direct","english_grad","test_validity","tahseely_rule","placement_fee"],"replaces":["P05","P06","P07","P08","P28","P71"],"fixes":["F-04","F-05","F-06","F-18"]},
 {"id":"costs","parent":"home","path":"/admissions/costs","t":L("التكاليف والمنح","Costs & scholarships"),"type":"reference",
  "does":L("الرسوم للدورة الحالية فقط، والضريبة، والاسترداد، وطرق الدفع، والمنح؛ الجداول السابقة في الأرشيف","Current-cycle fees only, VAT, refunds, payment and scholarships; previous tables in the archive"),
  "feeds":["tuition_ug","tuition_medicine","vat_statement","application_fee","placement_fee","refund_policy"],"replaces":["P10","P11","P13","P31","P45","P46","P47","P48","P49","P50","P51","P57","P58","P59"],"fixes":["F-10","F-22","F-06"]},
 {"id":"dates","parent":"home","path":"/admissions/dates","t":L("المواعيد وحالة الدورة","Dates & cycle status"),"type":"reference",
  "does":L("الدورة الحالية والقادمة، مفتوحة أو مغلقة، وآخر موعد لكل فئة","Current and next cycle, open or closed, and the deadline per category"),"feeds":["intake_status","application_channel"],"replaces":["P14","P32","P56","P65"],"fixes":["F-08","F-12"]},
 {"id":"apply","parent":"home","path":"/admissions/apply","t":L("قدّم الآن (موجّه القنوات)","Apply now (channel router)"),"type":"router",
  "does":L("سؤالان على الأكثر ثم القناة الصحيحة لفئتك؛ يستبدل كل روابط التقديم الحالية","At most two questions, then the right channel for your category; replaces every current apply link"),
  "feeds":["application_channel","intake_status"],"replaces":["P53","P16","P15"],"fixes":["F-02","F-08","F-16","F-24"]},
 {"id":"programs","parent":"home","path":"/admissions/programs","t":L("دليل البرامج","Programme finder"),"type":"reference",
  "does":L("البرامج النشطة فقط من سجل البرامج الموحّد، مرتبطة بشروطها ورسومها","Active programmes only, from the single register, linked to requirements and fees"),"feeds":["programme_register"],"replaces":["P24","P61","P60"],"fixes":["F-25"]},
 {"id":"contact","parent":"home","path":"/admissions/contact","t":L("التواصل والاستفسار","Contact & enquiries"),"type":"reference",
  "does":L("بريد وهاتف بأسماء أدوار، وساعات العمل، ونموذج الاستفسار مع زمن الرد","Role mailboxes and phone, hours, and the enquiry form with a response time"),"feeds":["contacts"],"replaces":["P29","P30","P63","P64"],"fixes":["F-11"]},
 {"id":"archive","parent":"home","path":"/admissions/archive","t":L("الأرشيف (غير مفهرس)","Archive (noindex)"),"type":"archive",
  "does":L("قواعد وجداول الدورات السابقة بلافتة «للمقبولين في…»","Previous-cycle rules and tables, bannered “for students admitted in…”"),"feeds":[],"replaces":["P20","P32","P46","P47","P55","P66","P72"],"fixes":["F-12","F-24"]},
]

G = lambda ar,en: L(ar,en)
legacy = []
def add(group, label, url, pid, node, action, finds, note_ar, note_en):
    legacy.append({"group":group,"label":label,"url":url,"page":pid,"to":node,"action":action,"findings":finds,"note":L(note_ar,note_en)})
FS=G("الطلاب الجدد","Future Students"); IO=G("مكتب الطلاب الدوليين","International Students’ Office")
GA=G("القبول للدراسات العليا","Graduate Admissions"); UA=G("القبول للبكالوريوس","Undergraduate Admissions"); PT=G("اختبارات تحديد المستوى","Undergraduate Placement Tests")
add(FS,"Overview","../Admission/Future_Students_RO.aspx","P23","home","merge",["F-15"],"نص تسويقي عام يُدمج في مقدمة الصفحة الرئيسية","Generic marketing text merged into the home intro")
add(FS,"Degrees & Programs","../Admission/Degrees_Programs_FS_RO.aspx","P24","programs","rebuild",["F-25"],"يُعاد بناؤه من سجل البرامج الموحّد","Rebuilt from the single programme register")
add(FS,"Admissions Calendar","../Admission/Admission_Calendar_FS_RO.aspx","P14","dates","move",["F-08","F-02"],"يصبح صفحة المواعيد، وتُغذّى حالة الدورة من السجل","Becomes the dates page; cycle status fed by the record")
add(FS,"Contact Us","../Staff_Profile/Staff_List.aspx?&DEpt=4","P63","contact","replace",["F-11"],"قائمة موظفين لقسم آخر تُستبدل ببريد أدوار","A staff list for another department, replaced by role mailboxes")
add(FS,"Admission Query","../Admission/admissions_queries","P29","contact","move",[],"ينتقل إلى صفحة التواصل مع زمن رد معلن","Moves to the contact page with a stated response time")
add(FS,"Apply Now","https://www.pmu.edu.sa/apply","P53","apply","replace",["F-02"],"يُستبدل بموجّه القنوات","Replaced by the channel router")
add(IO,"International Students without Saudi Residence","../Admission/International_Students.aspx","P18","ug_intl","rewrite",["F-02","F-05"],"إعادة كتابة: SAT II متوقف، والقناة متعارضة مع التقويم","Rewrite: SAT II is discontinued and the channel conflicts with the calendar")
add(IO,"Apply","https://www.pmu.edu.sa/apply","P53","apply","replace",["F-02"],"موجّه القنوات بالمسار الدولي محدّدًا مسبقًا","Router with the international route preselected")
add(GA,"Home","../Admission/Admission_Graduate_Degree_Programs.aspx","P33","grad","move",["F-25"],"صفحة قسم الدراسات العليا","Graduate section page")
for pid,lbl,fs in [("P34","PhD in Mechanical Engineering",[]),("P35","PhD in Business Administration",["F-26"]),("P36","EMBA",["F-26"]),("P37","MBA",["F-27"]),("P38","MSHD",[]),("P39","MSME",["F-26"]),("P40","MSEE",["F-27"]),("P41","MSCE",["F-27"]),("P42","MSID",["F-27"]),("P43","EMGMS",["F-21"]),("P44","MIBL",["F-26","F-17"])]:
    act = "rewrite" if pid=="P43" else "template"
    add(GA,f"Admissions to the {lbl}", "../Admission/…_GDP.aspx", pid, "grad_prog", act, fs,
        "سحب فوري ثم إعادة كتابة (نص جامعة أخرى)" if pid=="P43" else "ينتقل إلى قالب البرنامج الموحّد",
        "Withdraw now, then rewrite (another university’s text)" if pid=="P43" else "Moves to the single programme template")
add(GA,"Tuition & Fees","../Admission/Post_Graduate_Fees_TF_RO.aspx","P45","costs","merge",[],"قسم الدراسات العليا في صفحة التكاليف","Graduate section of the costs page")
add(GA,"Contact Info","../Admission/Admission_Contact_GDP.aspx","P30","contact","merge",["F-11"],"بريد الدراسات العليا الوظيفي في صفحة التواصل","Graduate role mailbox on the contact page")
add(UA,"Home","../Admission/Undergraduate_Programs_Admission.aspx","P02","ug","move",[],"صفحة قسم البكالوريوس","Undergraduate section page")
add(UA,"Admission to the College of Medicine","../admission/college_of_medicine_admission","P09","ug_med","rewrite",["F-03","F-07","F-20","F-23"],"إعادة كتابة بعد القرارين D5 وD10","Rewrite after decisions D5 and D10")
add(UA,"Admissions to the Preparatory Program","../Admission/Admission-to-the-Preparatory-Program.aspx","P25","ug_prep","rewrite",["F-26"],"أقسام فارغة تُعبّأ من السجل","Empty sections filled from the record")
add(UA,"Direct Admissions from Secondary School","../Admission/Direct-Admissions-from-Secondary-School.aspx","P04","ug_hs","merge",["F-01","F-04"],"يُدمج مع Freshman في مسار واحد","Merged with Freshman into one route")
add(UA,"Admissions from Other Universities","../Admission/Admission-from-Other-Universities.aspx","P17","ug_transfer","move",["F-16"],"مع سياسة التحويل (P62) ورابط HTTPS","With the transfer policy (P62) and an HTTPS link")
add(UA,"Visting Students","../Admission/Visiting-Student-Admission.aspx","P27","ug_visit","move",["F-17"],"تصحيح الإملاء «Visiting»","Spelling fixed to “Visiting”")
add(UA,"Admissions from the Preparatory Program","../Admission/Admission-from-the-Prep-to-UG-Programs.aspx","P26","ug_prep","merge",["F-28"],"قسم «الانتقال إلى البكالوريوس»","“Progression to the degree” section")
add(UA,"Computer Science and Engineering Majors Admission Requirements","../Admission/Admissions_Requirements_CS_Eng_Majors.aspx","P19","ug_hs","merge",["F-01","F-05"],"مكوّن «شروط التخصص» داخل المسار","“Major requirements” component inside the route")
add(UA,"Tuition & Fees","../Admission/Fees_TF_RO.aspx","P10","costs","merge",["F-10"],"الدورة الحالية فقط؛ السابقة إلى الأرشيف","Current cycle only; previous ones to the archive")
add(PT,"Overview","../Admission/Overview-Undergraduate-Placement-Tests.aspx","P05","req","merge",[],"مقدمة صفحة الإنجليزية والاختبارات","Intro of the English & tests page")
add(PT,"Aptis","../Admission/Aptis-Placement-Test.aspx","P08","req","merge",["F-12"],"مع استبدال دليل 2017","With the 2017 guide replaced")
add(PT,"IELTS","../Admission/IELTS-Admission.aspx","P06","req","merge",["F-04","F-18"],"صف في الجدول الموحّد","A row in the single table")
add(PT,"TOEFL","../Admission/TOEFL-Admission.aspx","P07","req","merge",["F-04"],"مع سلّم 1–6 (X01)","With the 1–6 scale (X01)")
add(PT,"Scholastic Aptitude Test (SAT)","../Admission/SAT-Admission.aspx","P28","req","merge",["F-05"],"مكافئ التحصيلي بعد القرار D3","Tahseely equivalent after decision D3")

routes = [
 {"id":"saudi_hs","node":"ug_hs","icon":"🎓","t":L("خريج ثانوية في المملكة","High-school graduate in KSA"),"sub":L("سعودي أو مقيم","Saudi or resident"),"preset":{"level":"ug","ug_type":"hs"}},
 {"id":"international","node":"ug_intl","icon":"🌍","t":L("طالب دولي","International student"),"sub":L("دون إقامة في المملكة","No Saudi residence"),"preset":{"level":"ug","ug_type":"hs","residency":"intl"}},
 {"id":"transfer","node":"ug_transfer","icon":"🔁","t":L("محوّل من جامعة أخرى","Transfer student"),"sub":L("معادلة المواد","Credit transfer"),"preset":{"level":"ug","ug_type":"transfer"}},
 {"id":"medicine","node":"ug_med","icon":"🩺","t":L("كلية الطب","College of Medicine"),"sub":L("مسار خاص","Dedicated route"),"preset":{"level":"ug","ug_type":"hs","program":"medicine"}},
 {"id":"graduate","node":"grad","icon":"📚","t":L("الدراسات العليا","Graduate studies"),"sub":L("ماجستير ودكتوراه","Master’s and doctorate"),"preset":{"level":"grad"}},
 {"id":"visiting","node":"ug_visit","icon":"🧭","t":L("طالب زائر","Visiting student"),"sub":L("فصل أو أكثر","One term or more"),"preset":{"level":"visiting"}},
]

questions = [
 {"id":"level","q":L("ما المرحلة؟","Which level?"),"opts":[["ug",L("بكالوريوس","Undergraduate")],["grad",L("دراسات عليا","Graduate")],["visiting",L("زائر","Visiting")]]},
 {"id":"ug_type","when":{"level":"ug"},"q":L("ما وضعك؟","Your situation?"),"opts":[["hs",L("خريج ثانوية","High-school graduate")],["transfer",L("محوّل من جامعة","Transfer")]]},
 {"id":"residency","when":{"level":"ug","ug_type":"hs"},"q":L("الجنسية والإقامة","Nationality and residence"),"opts":[["saudi",L("سعودي","Saudi")],["resident",L("غير سعودي مقيم (إقامة)","Non-Saudi resident (Iqama)")],["intl",L("غير سعودي دون إقامة","Non-Saudi, no residence")]]},
]

channels = {
 "qabool":{"t":L("منصة «قبول» الوطنية","National Qabool platform"),"url":"https://www.uap.sa/","owner":"MoE"},
 "sis":{"t":L("منصة «ادرس في السعودية»","Study in Saudi platform"),"url":"https://studyinsaudi.sa/","owner":"MoE"},
 "portal":{"t":L("بوابة التقديم في الجامعة","PMU application portal"),"url":"https://admissions.pmu.edu.sa/","owner":"PMU"},
}

# Decision table. basis = what PMU publishes today (live-verified 2026-09-27/28); status says whether it can go live.
rules = [
 {"id":"R1","when":{"level":"ug","ug_type":"hs","residency":"saudi"},"channel":"qabool","basis":["P14","P09","X05"],"status":"proposed",
  "note":L("مطابق للتقويم والنموذج الوطني، لكن صفحات أخرى تحيل إلى البوابة (F-02)","Matches the calendar and the national model, but other pages send to the portal (F-02)")},
 {"id":"R2","when":{"level":"ug","ug_type":"hs","residency":"intl"},"channel":"sis","basis":["P14","X08"],"status":"proposed",
  "note":L("التقويم يقول «ادرس في السعودية» (مغلق)، وصفحة الطلاب الدوليين P18 تحيل إلى البوابة","The calendar says Study in Saudi (Closed); the international page P18 sends to the portal")},
 {"id":"R3","when":{"level":"ug","ug_type":"hs","residency":"resident"},"channel":None,"basis":[],"status":"gap",
  "note":L("لا تذكر أي صفحة قناة غير السعودي المقيم؛ يحتاج قرارًا صريحًا في D4","No page states the channel for a non-Saudi resident; needs an explicit D4 ruling")},
 {"id":"R4","when":{"level":"ug","ug_type":"transfer"},"channel":"portal","basis":["P17"],"status":"proposed",
  "note":L("منشور اليوم برابط http غير آمن (F-16)","Published today as an insecure http link (F-16)")},
 {"id":"R5","when":{"level":"grad"},"channel":"portal","basis":["P33","P36","P16"],"status":"proposed",
  "note":L("اليوم: صفحة البرنامج ← Application Form ← Apply_Now_ADS ← البوابة (أربع قفزات)","Today: programme page → Application Form → Apply_Now_ADS → portal (four hops)")},
 {"id":"R6","when":{"level":"visiting"},"channel":"portal","basis":["P27"],"status":"proposed",
  "note":L("منشور اليوم برابط http غير آمن (F-16)","Published today as an insecure http link (F-16)")},
]

tests = [
 {"id":"T1","persona":"saudi_hs","answers":{"residency":"saudi"},"expect":"qabool"},
 {"id":"T2","persona":"international","answers":{},"expect":"sis"},
 {"id":"T3","persona":"transfer","answers":{},"expect":"portal"},
 {"id":"T4","persona":"medicine","answers":{"residency":"saudi"},"expect":"qabool"},
 {"id":"T5","persona":"graduate","answers":{},"expect":"portal"},
 {"id":"T6","persona":"visiting","answers":{},"expect":"portal"},
 {"id":"T7","persona":"saudi_hs","answers":{"residency":"resident"},"expect":None},
]

stages = [
 {"id":"discover","t":L("اكتشف","Discover"),"q":L("هل تقدّم الجامعة التخصص الذي أريده؟","Does PMU offer the programme I want?"),"touch":"programs","feeds":["programme_register"]},
 {"id":"eligible","t":L("تحقق من الأهلية","Check eligibility"),"q":L("هل أنا مؤهل، وبأي معادلة؟","Am I eligible, and under which formula?"),"touch":"route","feeds":["hs_gpa_min","gat_min","composite_formula","english_ug_direct"]},
 {"id":"costs","t":L("احسب التكاليف","Plan costs"),"q":L("كم سأدفع إجمالًا، وهل يُسترد؟","What will it cost in total, and is it refundable?"),"touch":"costs","feeds":["application_fee","tuition_ug","vat_statement","refund_policy"]},
 {"id":"dates","t":L("المواعيد والقناة","Dates & channel"),"q":L("هل القبول مفتوح، وأين أقدّم؟","Is admission open, and where do I apply?"),"touch":"dates","feeds":["intake_status","application_channel"]},
 {"id":"docs","t":L("جهّز الوثائق","Prepare documents"),"q":L("ما الذي أحتاجه بالضبط؟","What exactly do I need?"),"touch":"route","feeds":["required_documents"]},
 {"id":"apply","t":L("قدّم","Apply"),"q":L("أين أضغط؟","Where do I click?"),"touch":"apply","feeds":["application_channel"]},
 {"id":"track","t":L("تابع القرار","Track the decision"),"q":L("ماذا يحدث بعد التقديم، ومن أسأل؟","What happens next, and whom do I ask?"),"touch":"contact","feeds":["contacts","refund_policy"]},
]
# today's pain per persona per stage: (finding ids, short text)
P = lambda f, ar, en: {"f":f,"t":L(ar,en)}
pain = {
 "saudi_hs":{"discover":P(["F-25"],"كتالوج ناقص (لا طب)","Incomplete catalogue (no Medicine)"),"eligible":P(["F-01","F-04"],"معادلتان وحدّا إنجليزية","Two formulas, two English thresholds"),"costs":P(["F-06","F-10"],"رسم 950 يشمل الاختبار أم لا؟ ثلاثة جداول","Does the 950 fee include the test? Three tables"),"dates":P(["F-08","F-02"],"تقويم دورة بدأت، و«قبول» مقابل البوابة","Calendar of a cycle already started; Qabool vs portal"),"docs":P(["F-13"],"أصل أم نسخة؟","Original or copy?"),"apply":P(["F-02"],"خمسة مداخل تقديم","Five apply entry points"),"track":P(["F-11"],"«تواصل» يفتح قائمة قسم آخر","“Contact” opens another department’s list")},
 "international":{"discover":P(["F-25"],"كتالوج ناقص","Incomplete catalogue"),"eligible":P(["F-05"],"شرط SAT II المتوقف","Discontinued SAT II requirement"),"costs":P(["F-10"],"الضريبة 15% غير موضحة في صفحة المسار","15% VAT not shown on the route page"),"dates":P(["F-02","F-08"],"«ادرس في السعودية» مغلق والبوابة تقول قدّم","Study in Saudi closed while the portal says apply"),"docs":P(["F-13"],"معادلة الشهادة في صفحة أخرى","Equivalency on another page"),"apply":P(["F-02"],"قناتان متعارضتان","Two conflicting channels"),"track":P(["F-11"],"لا بريد وظيفي للقبول الجامعي","No role mailbox for UG admissions")},
 "transfer":{"discover":P([],"—","—"),"eligible":P(["F-04"],"حد الإنجليزية غير واضح","Unclear English threshold"),"costs":P(["F-10"],"أي جدول رسوم ينطبق؟","Which fee table applies?"),"dates":P(["F-08"],"لا موعد للتحويل","No transfer deadline"),"docs":P(["F-13"],"قائمة مختلفة عن غيرها","A different document list"),"apply":P(["F-16"],"رابط http غير آمن","Insecure http link"),"track":P(["F-11"],"—","—")},
 "medicine":{"discover":P(["F-25"],"الطب غائب عن الكتالوج","Medicine missing from the catalogue"),"eligible":P(["F-20","F-05"],"الحد 86 لا يتحقق بالحدود الدنيا (83)","The 86 floor is unreachable at the minimums (83)"),"costs":P(["F-03","F-07"],"1,000 أم 1,150؟ وحجز 20,000 غير مذكور","1,000 or 1,150? The 20,000 seat fee is not mentioned"),"dates":P(["F-23"],"7 سنوات أم 6؟","Seven years or six?"),"docs":P(["F-13"],"—","—"),"apply":P(["F-02"],"«قبول» مذكور في صفحة الطب فقط","Qabool mentioned only on the Medicine page"),"track":P(["F-22"],"الاسترداد متناقض","Contradictory refund policy")},
 "graduate":{"discover":P(["F-25"],"برنامجان مسعّران بلا صفحة","Two priced programmes without a page"),"eligible":P(["F-21","F-27"],"شروط EMGMS من جامعة أخرى","EMGMS requirements from another university"),"costs":P([],"—","—"),"dates":P(["F-08"],"لافتة لفصل سابق في البوابة","A past-term banner on the portal"),"docs":P(["F-26"],"أقسام إلزامية فارغة","Empty required sections"),"apply":P(["F-24"],"أربع قفزات ودليل لنظام متوقف","Four hops and a guide for a retired system"),"track":P([],"—","—")},
 "visiting":{"discover":P([],"—","—"),"eligible":P([],"—","—"),"costs":P([],"—","—"),"dates":P(["F-08"],"لا مواعيد للزائرين","No dates for visitors"),"docs":P([],"—","—"),"apply":P(["F-16"],"رابط http غير آمن","Insecure http link"),"track":P(["F-17"],"«Visting» خطأ إملائي في العنوان","“Visting” misspelt in the title")},
}

components = [
 {"id":"cycle","t":L("شريط حالة الدورة","Cycle-status bar"),"fields":["intake_status","application_channel"],"where":["home","dates","apply","ug_hs","ug_intl","ug_med"]},
 {"id":"reqs","t":L("الشروط والمعادلة","Requirements & formula"),"fields":["hs_gpa_min","gat_min","tahseely_rule","composite_formula","composite_minimum"],"where":["ug_hs","ug_intl","ug_med"]},
 {"id":"english","t":L("الإنجليزية والاختبارات","English & tests"),"fields":["english_ug_direct","english_grad","test_validity","placement_fee"],"where":["req","ug_hs","ug_intl","ug_transfer","ug_prep","grad_prog"]},
 {"id":"costs","t":L("التكاليف","Costs"),"fields":["application_fee","tuition_ug","tuition_medicine","vat_statement","refund_policy"],"where":["costs","ug_hs","ug_intl","ug_med","grad_prog"]},
 {"id":"docs","t":L("قائمة الوثائق","Document checklist"),"fields":["required_documents"],"where":["ug_hs","ug_intl","ug_transfer","ug_med","grad_prog"]},
 {"id":"howto","t":L("طريقة التقديم","How to apply"),"fields":["application_channel"],"where":["apply","ug_hs","ug_intl","ug_transfer","ug_med","ug_visit","grad_prog"]},
 {"id":"programs","t":L("دليل البرامج","Programme finder"),"fields":["programme_register"],"where":["programs","grad"]},
 {"id":"contact","t":L("التواصل","Contact"),"fields":["contacts"],"where":["contact","home"]},
]

json.dump({"generated_from":"make_ia.py","verified":"2026-09-28","sitemap":sitemap,"legacy":legacy,"routes":routes,"questions":questions,
           "channels":channels,"rules":rules,"tests":tests,"stages":stages,"pain":pain,"components":components},
          open(pathlib.Path(__file__).with_name("ia.json"),"w"),ensure_ascii=False,indent=1)
print("legacy links:",len(legacy),"sitemap nodes:",len(sitemap),"rules:",len(rules))
