# Content audit of the 36 links on the Admissions Office page (2026-09-28).
# Scope: what each page SAYS (data, rules, facts, completeness, consistency) — not technical
# issues. Every string in "q" is verbatim from the live page text (checked by build_content.py).
# sev: H high · M medium · L low. kind: conflict | error | gap | stale | wording | claim
# ref: existing finding ID, or "NEW" (proposal — not yet in the findings register).

PAGES = {
 "C01": dict(purpose="تعريف عام بالجامعة لمن يبحث عن برنامج", data=["لا بيانات قبول؛ روابط للبكالوريوس والدراسات العليا"], issues=[
   ("L", "claim", ["PMU’s system and academic programs were designed by the international educational consultant, Texas International Education Consortium (TIEC), which is a consortium of 32 universities in Texas, USA",
                   "reviewed and verified by around 70 multinational academic and industrial experts"],
    "ادعاءات رقمية بلا تاريخ أو مصدر، وعبارة «accredited by prestigious national and international organizations» لا تسمّي أي جهة اعتماد", "ذكر جهات الاعتماد بأسمائها وتواريخها، أو حذف الأرقام غير الموثّقة", "NEW"),
 ]),
 "C02": dict(purpose="قائمة البرامج المتاحة (بكالوريوس ودراسات عليا) مع توفرها للطلاب/الطالبات", data=["6 كليات للبكالوريوس (العمارة والتصميم، الهندسة، الحاسب، إدارة الأعمال، القانون)", "برامج دراسات عليا في الهندسة، إدارة الأعمال، العلوم والدراسات الإنسانية، العمارة والتصميم، القانون"], issues=[
   ("M", "gap", ["B.S. in Chemical Engineering", "B.S. in Cybersecurity"],
    "القائمة لا تتضمن كلية الطب ولا كلية العلوم والدراسات الإنسانية (بكالوريوس)، ولا برامج EMGMS و MSEE/MSCE في مكانها الكامل، بينما تضيف برامج (الهندسة الكيميائية، الأمن السيبراني) لا تذكرها صفحات شروط التخصصات (C30/C36)", "قائمة برامج واحدة من سجل البرامج الموحّد، مع حالة القبول لكل برنامج", "F-25"),
   ("L", "gap", ["Undergraduate Programs", "Graduate Programs"],
    "البرامج مخفية داخل قائمتين مطويتين؛ من يفتح الصفحة يرى عنوانين فقط. وتوجد في كود الصفحة بقايا برنامج «Master of LAW» مخفي", "عرض البرامج مباشرة مع رابط لكل برنامج إلى شروطه", "NEW"),
 ]),
 "C03": dict(purpose="مواعيد القبول للدورة الحالية", data=["Fall 2026-2027 (بكالوريوس ودراسات عليا)", "بدء الدراسة 2026-08-30", "السعوديون عبر «قبول»؛ غير السعوديين عبر «ادرس في السعودية» (Closed)"], issues=[
   ("H", "stale", ["Fall 2026-2027", "First day of classes\t2026-08-30"],
    "في تاريخ التدقيق (2026-09-28) كل مواعيد الدورة انتهت، ولا توجد أي معلومة عن الدورة القادمة (الفصل الثاني) أو حالة القبول الآن", "مكوّن «حالة القبول الآن» + مواعيد الدورة القادمة أو عبارة صريحة «القبول مغلق حتى …»", "F-08"),
   ("M", "conflict", ["Announcement of admission results through Qabool platform\tFrom July 19 to July 21, 2026", "Last day to submit IELTS or TOEFL iBT\t2026-07-20", "Last day for Transfer applicants to submit documents in person\t2026-07-20"],
    "إعلان النتائج يبدأ 19 يوليو قبل آخر موعد لتقديم IELTS/TOEFL ووثائق المحوّلين (20 يوليو)", "إعادة ترتيب المواعيد أو توضيح أن النتائج لفئات محددة", "F-08"),
   ("H", "conflict", ["For non Saudi Students: Apply online through Study in Saudi platform: https://studyinsaudi.sa/ar\tClosed"],
    "التقويم يقول إن تقديم غير السعوديين «مغلق» عبر «ادرس في السعودية»، بينما صفحة الطلاب الدوليين (C07) تقول إن التقديم يتم بالكامل أونلاين عبر بوابة الجامعة", "تحديد قناة واحدة لكل فئة وإظهارها في الصفحتين", "F-02"),
   ("L", "gap", ["Orientation for new applicants\tTBA"], "موعد التوجيه ما زال «TBA» رغم بدء الدراسة", "تحديثه أو حذفه بعد انقضائه", "NEW"),
 ]),
 "C04": dict(purpose="التواصل مع مكتب القبول", data=["يفتح قائمة موظفين بأسمائهم (لم تُنسخ هنا)"], issues=[
   ("H", "gap", [], "لا يوجد في الصفحة رقم هاتف أو بريد موحّد لمكتب القبول أو ساعات عمل؛ يُحال المتقدم إلى أسماء أفراد", "صفحة تواصل موحّدة (بريد وهاتف مكتب القبول، ساعات العمل، نموذج الاستفسار)", "F-11"),
 ]),
 "C05": dict(purpose="نموذج استفسار للمتقدمين", data=["الاسم، البريد، الجوال، الاستفسار، طريقة التواصل المفضّلة"], issues=[
   ("L", "wording", ["Name [الأسم]", "مكتب القبول يسعد بالإجابة على إستفساراتكم", "Email [البريد الإللكتروني]", "Enter Verifaction Code"],
    "أخطاء إملائية في النص العربي والإنجليزي: «الأسم» (الاسم)، «إستفساراتكم/الإستفسار» (استفسار)، «الإللكتروني» (لام زائدة)، «Verifaction»", "تدقيق لغوي", "F-17"),
   ("L", "gap", [], "لا يذكر النموذج مدة الرد المتوقعة ولا بديل تواصل مباشر", "إضافة زمن الرد المتوقع وقناة بديلة", "NEW"),
 ]),
 "C06": dict(purpose="زر التقديم", data=["يفتح بوابة التقديم admissions.pmu.edu.sa"], issues=[
   ("H", "conflict", [], "زر «Apply Now» يرسل الجميع للبوابة نفسها، بينما التقويم (C03) يوجّه السعوديين إلى منصة «قبول» وغير السعوديين إلى «ادرس في السعودية» — ثلاث قنوات لنفس الخطوة", "موجّه تقديم حسب فئة المتقدم", "F-02"),
 ]),
 "C07": dict(purpose="القبول للطلاب الدوليين غير المقيمين (مستجد، محوّل، زائر، دراسات عليا، رسوم، سكن)", data=["مستجد: معدل 80% + SAT I + IELTS 6.0/5.5 كتابة + مقابلة أونلاين", "رسوم الطلب: 950 شامل الضريبة (مستجد) / 500 غير شامل (محوّل وزائر)"], issues=[
   ("H", "conflict", ["Pay a non-refundable application fee of SAR 500 (excl. VAT) upon submission of documents"],
    "رسوم طلب المحوّل والزائر الدولي 500 ريال غير شاملة الضريبة، بينما صفحتا المحوّلين (C27) والزائرين (C28) تذكران 950 ريالًا شاملة الضريبة للفئة نفسها", "قرار مالي بقيمة واحدة لكل فئة ونشرها من سجل الرسوم", "NEW"),
   ("H", "error", ["SAT II 30%"], "يشترط SAT II (اختبارات المواد) للهندسة والحاسب، وقد أوقفتها College Board دوليًا في 2021", "استبدالها بالشرط المعتمد (تحصيلي أو ما يعادله)", "F-05"),
   ("M", "error", ["Copy of National ID"], "يطلب «الهوية الوطنية» من طالب دولي بلا إقامة سعودية — مستند لا يملكه", "استبدالها بجواز السفر فقط", "F-13"),
   ("M", "gap", ["Acceptable SAT I"], "لا يذكر الحد الأدنى لـ SAT I، بينما صفحة SAT (C36) تحدده 1200", "ذكر الحد الرقمي", "F-09"),
   ("M", "gap", ["MBA", "MSHD", "MSME"], "قسم الدراسات العليا للدوليين يعرض 3 برامج فقط من أصل 11 برنامجًا في الصفحة الرئيسية", "ربطه بقائمة البرامج الكاملة وتوضيح المتاح للدوليين", "NEW"),
   ("L", "gap", ["Transportation"], "قسم «Transportation» عنوان بلا محتوى، وقسم السكن بصيغة المستقبل «will be located»", "كتابة معلومات النقل والسكن الفعلية", "NEW"),
   ("L", "gap", ["Get Information on Tuition and Fees"], "تعليمات الدفع للطلاب الدوليين موجودة في كود الصفحة لكنها مخفية عن الزائر (لم تُنسخ هنا لأنها بيانات بنكية)", "قرار: نشر طريقة الدفع الرسمية أو حذف البقايا", "NEW"),
 ]),
 "C08": dict(purpose="زر التقديم للطلاب الدوليين", data=["يفتح البوابة العامة نفسها"], issues=[
   ("H", "conflict", [], "لا يوضح القناة الصحيحة لغير المقيم، والتقويم يقول إن قناتهم «مغلقة»", "كما في C06", "F-02"),
 ]),
 "C09": dict(purpose="الصفحة الرئيسية للدراسات العليا وقائمة البرامج", data=["10 برامج مع روابط «Application Form» و«Admissions Requirements»"], issues=[
   ("M", "gap", ["Admissions to the Master of Arts (MA) in International Business Law Program"],
    "القائمة لا تتضمن برنامج EMGMS (الموجود في صفحة القبول الرئيسية C19 وفي جدول الرسوم C21)، ولا «Master of Engineering in Innovation, Sustainability, and Entrepreneurship» المسعّر في C21", "قائمة البرامج من السجل الموحّد", "F-25"),
   ("M", "conflict", ["Admission to the Master of Human Development", "Admissions to the Doctorate in Mechanical Engineering Program"],
    "أسماء البرامج تختلف بين الصفحات: «Master of Human Development» هنا، و«MSHD» في صفحة القبول، و«Master of Science in Human Development» في C14، و«Master of Science in Education and Human Development» في C21؛ و«Doctorate» هنا مقابل «PhD» في C10 و«Doctoral program» في C21", "اسم رسمي واحد لكل برنامج (عربي/إنجليزي)", "F-25"),
   ("L", "gap", ["Admissions to the Master of Science in Civil Engineering (MSCE) Program"], "برامج MSCE و MSEE و MSID تعرض «Application Form» دون رابط، بينما بقية البرامج لها رابط", "توحيد روابط نموذج الطلب", "NEW"),
 ]),
 "C10": dict(purpose="شروط قبول الدكتوراه في الهندسة الميكانيكية", data=["بكالوريوس وماجستير هندسة ميكانيكية", "معدل 3.00/4.00", "IELTS 6.0 (5.5 لكل مهارة) أو TOEFL 83 (19)", "خطابا توصية + بيان غرض + مقابلة"], issues=[
   ("M", "conflict", ["A minimum cumulative GPA of 3.00 out of 4.00 or equivalent (Very Good)"], "الوصف «Very Good» مقرون هنا بـ 3.00، وفي ست صفحات أخرى بـ 2.50", "جدول تحويل تقديرات موحّد من عمادة القبول والتسجيل", "F-27"),
   ("L", "gap", [], "لا تذكر الصفحة عدد الساعات أو مدة البرنامج أو الرسوم أو مواعيد التقديم (الرسوم موجودة في C21: 72 ساعة، 150,000 ريال)", "إضافة بطاقة «حقائق البرنامج»", "NEW"),
 ]),
 "C11": dict(purpose="شروط قبول الدكتوراه في إدارة الأعمال", data=["مساران: الإدارة والتمويل", "ماجستير إدارة أعمال/تمويل أو تخصص قريب", "3 خطابات توصية"], issues=[
   ("M", "wording", ["Otherwise, if the master degree is not from another discipline they must successfully attend and complete with minimum GPA 2.80 12 credit hours of MBA"],
    "صياغة بنفي مزدوج تعكس المعنى (المقصود: إذا كان الماجستير من تخصص آخر)، وشرطا المعدل (3.00 أو 3.20) غير واضحين لمن ينطبق كل منهما", "إعادة صياغة الشرط بجدول واضح", "NEW"),
   ("M", "claim", ["The Ph.D. program is internationally accredited by AACSB as top 6% of business schools worldwide."],
    "اعتماد AACSB يُمنح للكلية/المؤسسة وليس لبرنامج منفرد، ونسبة 6% تخص عدد الكليات المعتمدة لا ترتيبًا («top»)", "صياغة دقيقة: «كلية إدارة الأعمال معتمدة من AACSB، وهو اعتماد تحمله أقل من 6% من كليات الأعمال عالميًا» بعد تأكيد الكلية", "NEW"),
 ]),
 "C12": dict(purpose="شروط قبول EMBA", data=["33 ساعة، سنتان، عطلة نهاية الأسبوع", "معدل 2.50", "خبرة 3–5 سنوات", "خطاب من جهة العمل + 3 توصيات"], issues=[
   ("M", "conflict", ["A minimum GPA of 2.50 out of 4.00 or equivalent (Very Good) in Bachelor’s Degree"], "2.50 موصوفة بـ «Very Good» بينما 3.00 موصوفة بالوصف نفسه في C10", "جدول تحويل موحّد", "F-27"),
   ("L", "conflict", ["Successful candidates should have from three to five years of professional work experience", "Participants are required to have several years of work experience"], "الخبرة «من 3 إلى 5 سنوات» (هل تُستبعد 6 سنوات فأكثر؟) مقابل «several years» في الفقرة نفسها", "صياغة «3 سنوات على الأقل»", "NEW"),
 ]),
 "C13": dict(purpose="شروط قبول MBA", data=["36 ساعة، مسائي، 6 تركيزات", "معدل 2.50", "IELTS 6.0 / TOEFL 83"], issues=[
   ("M", "conflict", ["A minimum GPA of 2.50 out of 4.00 or equivalent (Very Good) in Bachelor’s Degree"], "كما في C12", "جدول تحويل موحّد", "F-27"),
   ("L", "gap", [], "لا تذكر أي مستندات داعمة (توصيات، بيان غرض، سيرة ذاتية) خلافًا لبقية برامج الدراسات العليا — يحتاج تأكيد أنها غير مطلوبة فعلًا", "تأكيد القائمة من الكلية", "NEW"),
 ]),
 "C14": dict(purpose="شروط قبول ماجستير التنمية البشرية", data=["بكالوريوس بمعدل 2.50 في تخصص ذي صلة", "خطابا توصية + بيان غرض + مقابلة"], issues=[
   ("M", "gap", ["Work Experience"], "عنوان «Work Experience» بلا أي شرط تحته (يليه مباشرة بند السيرة الذاتية)", "تحديد شرط الخبرة أو حذف العنوان", "NEW"),
   ("L", "gap", [], "لا تذكر عدد الساعات أو المدة (جدول الرسوم C21 يوحي بـ 42 ساعة: 50,000 ÷ 1,191)", "إضافة بطاقة حقائق البرنامج", "NEW"),
 ]),
 "C15": dict(purpose="شروط قبول ماجستير الهندسة الميكانيكية", data=["30 ساعة على الأقل، مساران، رسالة/بدون رسالة", "معدل 2.50", "خطابا توصية"], issues=[
   ("M", "conflict", ["A minimum cumulative GPA of 2.50 out of 4.00 or equivalent (Very Good) in Bachelor’s Degree"], "كما في C12", "جدول تحويل موحّد", "F-27"),
 ]),
 "C16": dict(purpose="شروط قبول ماجستير الهندسة الكهربائية", data=["مساران", "بكالوريوس هندسة (أي تخصص هندسي)", "معدل 2.50"], issues=[
   ("L", "stale", ["The program will be offered under the College of Engineering."], "صيغة المستقبل «will be offered» توحي بأن البرنامج لم يُطلق — هل هو متاح للقبول الآن؟", "إظهار حالة البرنامج (متاح/غير متاح) وتحديث الصياغة", "NEW"),
   ("M", "conflict", ["A minimum cumulative GPA of 2.50 out of 4.00 or equivalent (Very Good) in Bachelor’s Degree"], "كما في C12", "جدول تحويل موحّد", "F-27"),
 ]),
 "C17": dict(purpose="شروط قبول ماجستير الهندسة المدنية", data=["مساران", "بكالوريوس هندسة مدنية", "معدل 2.50"], issues=[
   ("L", "stale", ["The program will be offered under the College of Engineering."], "كما في C16", "كما في C16", "NEW"),
   ("M", "conflict", ["A minimum cumulative GPA of 2.50 out of 4.00 or equivalent (Very Good) in Bachelor’s Degree"], "كما في C12", "جدول تحويل موحّد", "F-27"),
 ]),
 "C18": dict(purpose="شروط قبول ماجستير التصميم الداخلي", data=["بكالوريوس تصميم داخلي", "معدل 2.50"], issues=[
   ("L", "stale", ["The Department of Interior Design at PMU will educate tomorrow’s interior design leaders"], "النص التعريفي كله بصيغة المستقبل (will educate / will be to provide)", "تحديث الصياغة", "NEW"),
   ("M", "conflict", ["A minimum cumulative GPA of 2.50 out of 4.00 or equivalent (Very Good) in Bachelor’s Degree"], "كما في C12", "جدول تحويل موحّد", "F-27"),
 ]),
 "C19": dict(purpose="شروط قبول ماجستير إدارة الهندسة (EMGMS)", data=["معدل 3.00", "IELTS 7 / TOEFL 79 / PTE 60"], issues=[
   ("H", "error", ["Graduate English Language Endorsement from UA Center for English as Second Language (CESL)"], "محتوى منسوخ من جامعة أخرى (University of Arizona)؛ مسار لا ينطبق على متقدمي PMU", "سحب الصفحة وإعادة كتابتها من شروط PMU", "F-21"),
   ("H", "conflict", ["IELTS – minimum composite score of 7, with no subject area below a 6", "TOEFL – minimum of 79 iBT"], "IELTS 7 أعلى من كل برامج PMU (6.0) بينما TOEFL 79 أقل منها (83) — المعادلة نفسها متناقضة داخل الصفحة", "اعتماد عتبة PMU الموحّدة", "F-21"),
   ("M", "gap", [], "لا وصف للبرنامج ولا مدة ولا مقابلة، خلافًا لكل برامج الدراسات العليا الأخرى", "قالب صفحة البرنامج الموحّد", "F-21"),
 ]),
 "C20": dict(purpose="شروط قبول ماجستير القانون التجاري الدولي", data=["مساران", "بكالوريوس قانون بتقدير «جيد جدًا»", "IELTS 6.5", "الأوزان: المعدل 50% + اختبار تحريري 30% + مقابلة 20%"], issues=[
   ("H", "conflict", ["Typically, candidates will complete the program within two years in a full-time mode (maximum 6 credits in each semester)"],
    "البرنامج 36 ساعة (حسب C21)، و6 ساعات كحد أقصى لكل فصل تعني 6 فصول (3 سنوات) لا سنتين", "تصحيح المدة أو الحد الأقصى للساعات", "NEW"),
   ("M", "gap", ["30% for the written test."], "وزن 30% لـ«اختبار تحريري» غير مذكور ضمن شروط القبول ولا موصوف", "وصف الاختبار (المحتوى، الموعد، الحد الأدنى)", "F-26"),
   ("M", "conflict", ["minimum scores of 6.5 overall and 5.5 in each skill or equivalent TOEFL iBT minimum scores of 83 overall"], "IELTS 6.5 تُعادَل بـ TOEFL 83، بينما TOEFL 83 يُعادَل بـ IELTS 6.0 في بقية البرامج", "توحيد جدول المعادلة", "NEW"),
   ("M", "gap", ["A minimum (Very Good) in Bachelor’s Degree"], "التقدير «Very Good» بلا رقم (بقية البرامج تذكر رقمًا)", "ذكر المعدل الرقمي", "F-27"),
   ("L", "stale", ["The year 2025 marks another milestone"], "عبارة مرتبطة بسنة 2025", "صياغة غير مؤقتة", "NEW"),
 ]),
 "C21": dict(purpose="رسوم الدراسات العليا", data=["13 برنامجًا بسعر إجمالي وسعر للساعة، للخريجين وغيرهم", "الضريبة: 15% على غير السعوديين (رسوم دراسية ورسوم أخرى)، والسعوديون يدفعون الضريبة على الرسوم الأخرى فقط"], issues=[
   ("M", "gap", ["Master of Engineering in Innovation, Sustainability, and Entrepreneurship (33)", "PRE-Master for Master of Education"], "برنامجان مسعّران لا توجد لهما صفحة قبول بين الروابط الـ36", "إما إضافة صفحتي قبول أو حذف السطرين إن لم يكونا متاحين", "F-25"),
   ("L", "conflict", ["Master of Science in Human Development\tSAR 50,000", "Master of Science in Education and Human Development\t1,191 SAR /Credit hour"], "البرنامج نفسه باسمين مختلفين في الجدولين", "اسم رسمي واحد", "F-25"),
 ], verified=["تحقق حسابي: السعر الإجمالي = سعر الساعة × عدد الساعات لـ EMBA (33) و MBA (36) و PhD (72) و MSME/MSEE/MSCE/MSID (30) و EMGMS (30) و M.Eng (33) و MA IBL (36) — متسق"]),
 "C22": dict(purpose="تواصل الدراسات العليا", data=["منسق القبول للدراسات العليا، مكتب G-017، بريد graduateadm@pmu.edu.sa"], issues=[
   ("L", "gap", [], "بريد ومكتب فقط؛ لا هاتف ولا ساعات عمل", "مكوّن تواصل موحّد", "F-11"),
 ]),
 "C23": dict(purpose="الصفحة الرئيسية لقبول البكالوريوس", data=["معدل 80% + قدرات 60% (أو SAT 1)", "المعادلة 60/40 لمن هم أقل", "رسوم الطلب 950 شاملة الضريبة", "صباحي 20 ساعة / مسائي 12"], issues=[
   ("M", "gap", ["PMU offers various degrees under the College of Architecture and Design, College of Computer Engineering and Science, College of Business Administration, College of Law and College of Engineering."],
    "تذكر 5 كليات فقط وتُسقط كلية الطب (المذكورة في الصفحة نفسها) وكلية العلوم والدراسات الإنسانية", "قائمة الكليات من السجل الموحّد", "F-25"),
   ("L", "wording", ["College of Medical Admissions"], "«College of Medical» خطأ (College of Medicine)", "تصحيح", "F-17"),
   ("M", "conflict", ["Visiting students are students registered in other local or international recognized universities"], "هنا الزائر من جامعات «محلية أو دولية»، وفي C07 «international» فقط — يحتاج توضيح هل الزائر المحلي مقبول", "توحيد التعريف", "NEW"),
 ]),
 "C24": dict(purpose="القبول في كلية الطب", data=["برنامج 7 سنوات", "المعادلة: (20% ثانوي + 40% قدرات + 40% تحصيلي) × 60% + مقابلة 40%، والحد الأدنى 86", "الحد الأدنى: ثانوي 95%، قدرات 80، تحصيلي 80", "رسوم الطلب 1000 شاملة الضريبة"], issues=[
   ("H", "conflict", ["20% high school + 40% Qudrat + 40% Tahseely were 86 is the minimum acceptable score", "Copy of secondary school certificate or equivalent (95%)"], "من يحقق الحدود الدنيا المنشورة (95/80/80) يحصل على 83 فقط وهو أقل من 86", "نشر حدود متسقة أو مثال محسوب", "F-20"),
   ("H", "conflict", ["The PMU College of Medical curriculum is based on a 7-year hybrid model"], "البرنامج «7 سنوات» لكن الخطة المعروضة تتوقف عند السنة السادسة (Year 6)، وصفحة الكلية الأكاديمية تقول 6 سنوات", "اعتماد المدة الصحيحة من الكلية ونشر التكلفة الإجمالية", "F-23"),
   ("H", "wording", ["the process typically involves understanding the weighting and criteria that the medical college uses to evaluate applicants", "Population Health (to be developed in launch phase)"], "نص مسودة غير محرّر (أسلوب شرح عام) وعبارات «to be developed»", "إعادة كتابة الصفحة", "F-07"),
   ("M", "wording", ["Biology: One full year (2 courses) of general biology with laboratory."], "وصف السنتين 1–2 مكتوب كقائمة «متطلبات سابقة» على النمط الأمريكي، لا كخطة دراسية في PMU", "صياغة الخطة كما تُدرّس فعليًا", "NEW"),
   ("M", "gap", [], "لا تذكر الصفحة شرط اللغة الإنجليزية ولا دفعة حجز المقعد (20,000 غير مستردة) ولا تكلفة البرنامج", "بطاقة تكلفة وشروط كاملة", "F-07"),
   ("M", "conflict", ["Pay a non-refundable application fee of SAR 1000 (incl. VAT)"], "رسوم طلب الطب 1000 هنا، و1,150 في صفحة رسوم الطب", "قيمة واحدة من المالية", "F-03"),
 ]),
 "C25": dict(purpose="القبول في السنة التحضيرية", data=["معدل 80% + قدرات 60%", "اختبار Aptis + مقابلة", "رسوم 950 شاملة الضريبة", "مقررات مهارات التعلّم حسب المستوى"], issues=[
   ("L", "gap", ["If employed, a letter of no objection from the employer is required"], "الصفحة سليمة المحتوى عمومًا؛ لا تذكر مدة التحضيرية ولا تكلفتها", "إضافة المدة والتكلفة", "NEW"),
 ]),
 "C26": dict(purpose="القبول المباشر من الثانوية", data=["معدل 80% + قدرات 60% + IELTS 6.0/5.5 كتابة", "المعادلة 60/40"], issues=[
   ("M", "gap", ["Copy of Saudi ID"], "يطلب «الهوية السعودية» فقط دون «الإقامة»، بينما التحضيرية والتحويل تقبل الإقامة — المقيم غير السعودي لا يجد نفسه", "«هوية وطنية أو إقامة»", "F-13"),
   ("M", "gap", ["equivalent TOEFL iBT (Learn more)"], "لا يذكر درجة TOEFL المطلوبة في الصفحة (موجودة في C35: 83/19)", "ذكر الرقم مباشرة", "F-09"),
 ]),
 "C27": dict(purpose="القبول بالتحويل من جامعة أخرى", data=["معدل تراكمي 2.0/4.0", "آخر مقرر خلال 5 سنوات", "مراجعة المعادلة 5 أسابيع على الأقل", "رسوم 950 شاملة الضريبة"], issues=[
   ("H", "conflict", ["Pay a non-refundable application fee of SAR 950 (incl. VAT) upon submission of documents"], "رسوم المحوّل 950 شاملة الضريبة هنا، و500 غير شاملة في صفحة الدوليين (C07)", "قيمة واحدة لكل فئة", "NEW"),
   ("L", "wording", ["In order to be consider as a transfer candidate"], "خطأ لغوي (considered)", "تصحيح", "F-17"),
 ]),
 "C28": dict(purpose="قبول الطالب الزائر", data=["موافقة الجامعة الأم + موافقة الكلية", "رسوم 950 شاملة الضريبة"], issues=[
   ("H", "conflict", ["Pay a non-refundable application fee of SAR 950 (incl. VAT) upon submission of documents"], "رسوم الزائر 950 شاملة هنا، و500 غير شاملة في C07", "قيمة واحدة لكل فئة", "NEW"),
   ("L", "gap", ["Copy of secondary school certificate or equivalent", "Copy of General Aptitude Test score report (Qudrat) or equivalent (SAT 1) - if available"], "يطلب من طالب جامعي زائر شهادة الثانوية واختبار القدرات — يحتاج تأكيد الضرورة", "مراجعة قائمة المستندات", "NEW"),
 ]),
 "C29": dict(purpose="الانتقال من التحضيرية إلى البكالوريوس", data=["إكمال التحضيرية + اجتياز EXIT exam + شروط الكلية", "جدول مقررات الرياضيات حسب الكلية"], issues=[
   ("M", "error", ["* Department of Information Technology is excluded from PRPM 0022", "** Department of Architecture is excluded from PRPM 0012"], "علامات الحواشي معكوسة: (*) موضوعة على الهندسة والعمارة لكنها تخص تقنية المعلومات، و(**) على كلية الحاسب لكنها تخص العمارة", "تصحيح الحواشي", "F-28"),
   ("M", "gap", ["Successfully pass the EXIT exam"], "«EXIT exam» غير معرّف (محتواه ودرجة النجاح)", "تعريف الاختبار", "F-28"),
 ]),
 "C30": dict(purpose="شروط تخصصات الحاسب والهندسة", data=["عام: ثانوي ≥80 (60%) + قدرات ≥60 (40%)", "تخصصي: ثانوي ≥85 (40%) + قدرات ≥65 (30%) + تحصيلي ≥65 (30%)", "SAT 1 (1200) بديل التحصيلي"], issues=[
   ("M", "conflict", ["These majors are Architecture, Computer Science, Computer Engineering, Software Engineering, Mechanical Engineering, Electrical Engineering and Civil Engineering."], "قائمة التخصصات ذات الشروط الخاصة هنا 7 تخصصات؛ صفحة SAT (C36) تضيف «Artificial Intelligence … etc.»، وقائمة البرامج (C02) فيها الهندسة الكيميائية والأمن السيبراني دون ذكر شروطهما", "قائمة مغلقة واحدة للتخصصات ذات الشروط الخاصة", "NEW"),
   ("M", "gap", ["the minimum weighted total, defined by the Admissions Office, should be met."], "الحد الأدنى للمجموع الموزون غير منشور", "نشر الرقم أو توضيح أنه يتغير كل دورة", "F-09"),
   ("M", "conflict", ["Copy of Standard Achievement Admission Test score report (SAAT – Tahseely) or SAT 1 (1200)"], "بديل التحصيلي SAT 1200 هنا، و1300 في صفحة الطب", "تحديد المعادلة الرسمية", "F-05"),
   ("L", "wording", ["may wave one or more"], "«wave» خطأ (waive)", "تصحيح", "F-17"),
 ]),
 "C31": dict(purpose="رسوم البكالوريوس (فهرس)", data=["روابط لـ: رسوم الطب، Fall 2026/2027، Fall 2025/2026، المستمرون 2024–2025"], issues=[
   ("M", "stale", ["Fall Semester 2025/2026", "Continuing Students 2024–2025"], "ثلاثة أجيال من جداول الرسوم معروضة بلا تمييز للجدول الساري", "جدول ساري واحد + أرشيف واضح", "F-10"),
 ]),
 "C32": dict(purpose="نظرة عامة على اختبارات اللغة", data=["Aptis للتسكين، و IELTS/TOEFL للإعفاء"], issues=[
   ("L", "gap", ["Candidates with PMU recognized proficiency English language test certificates"], "عبارة «PMU recognized» غير معرّفة؛ الصفحة تذكر IELTS و TOEFL فقط بينما C19 يقبل PTE", "قائمة الاختبارات المعتمدة", "NEW"),
 ]),
 "C33": dict(purpose="اختبار Aptis للتسكين", data=["مدة الاختبار ~4 ساعات", "4 مستويات"], issues=[
   ("M", "gap", ["Based on candidates overall and writing scores, they will be placed on one of the following levels:"], "لا توجد درجات Aptis لكل مستوى، بينما IELTS و TOEFL لهما جدول درجات منشور", "نشر جدول درجات Aptis", "F-09"),
   ("L", "wording", ["direct entry into the Core Program"], "مصطلح «Core Program» غير معرّف (باقي الصفحات: degree program)", "توحيد المصطلح", "F-15"),
 ]),
 "C34": dict(purpose="متطلبات IELTS", data=["Core 6.0/5.5، Advanced 5.0/4.5، Intermediate 4.5/4.0، Beginner 4.0/3.5", "صلاحية سنتان حتى بدء الفصل"], issues=[], verified=["متسق مع C26 و C07 (6.0 / 5.5 كتابة للقبول المباشر)"]),
 "C35": dict(purpose="متطلبات TOEFL iBT", data=["Core 83/19، Advanced 63/15، Intermediate 54/13، Beginner 42/11", "رمز المؤسسة 6993"], issues=[
   ("M", "stale", ["TOEFL iBT Overall"], "الجدول بمقياس 0–120 فقط؛ منذ 21 يناير 2026 تُصدر ETS نتائج TOEFL iBT بمقياس 1–6، ويُعرض المقياس المقارن 0–120 مؤقتًا حتى يناير 2028 فقط، ولا تذكر الصفحة حدودًا بالمقياس الجديد", "إضافة عمود المقياس الجديد بعد اعتماد المعادلة", "F-04"),
 ], verified=["رمز ETS (6993) لم يُتحقق منه من مصدر ETS — يُنصح بتأكيده"]),
 "C36": dict(purpose="متطلبات SAT", data=["SAT 1200 بدلًا من القدرات والتحصيلي لخريجي الشهادات الدولية", "إعفاء من مقررات الرياضيات حسب درجة الرياضيات", "رمز College Board 7647"], issues=[
   ("M", "conflict", ["These majors are Architecture, Computer Science, Computer Engineering, Software Engineering, Artificial Intelligence, Mechanical Engineering, Electrical Engineering and Civil Engineering etc."], "قائمة مفتوحة («etc.») وتختلف عن C30", "قائمة مغلقة واحدة", "NEW"),
   ("M", "conflict", ["Students with international high school certificate might submit SAT with minimum score of 1200 instead of Qudrat and Tahseely tests."], "1200 هنا بديل للاختبارين معًا، وفي صفحة الطب 1300 بديل للتحصيلي، وفي C07 يُطلب SAT I و SAT II", "قاعدة SAT واحدة لكل فئة", "F-05"),
   ("L", "wording", ["Introductory Algebra\tWave\tWave"], "«Wave» خطأ (Waive)", "تصحيح", "F-17"),
 ]),
}

# Cross-page data points: the same fact stated differently across the 36 links
MATRIX = [
 ("رسوم طلب القبول", [("C23,C25,C26,C27,C28,C30", "SAR 950 (incl. VAT)"), ("C24 (الطب)", "SAR 1000 (incl. VAT)"), ("C07 (محوّل/زائر دولي)", "SAR 500 (excl. VAT)")], "H", "F-31 + F-03"),
 ("وصف «Very Good» للمعدل", [("C12,C13,C15,C16,C17,C18", "2.50 / 4.00"), ("C10", "3.00 / 4.00"), ("C20", "بلا رقم")], "M", "F-27"),
 ("اللغة الإنجليزية — الدراسات العليا", [("9 برامج", "IELTS 6.0 (5.5 لكل مهارة) أو TOEFL 83 (19)"), ("C20 MA IBL", "IELTS 6.5 أو TOEFL 83"), ("C19 EMGMS", "IELTS 7 أو TOEFL 79 أو PTE 60 أو CESL")], "H", "F-21 + F-33"),
 ("بديل SAT", [("C36", "1200 بدل القدرات والتحصيلي"), ("C30", "SAT 1 (1200) بدل التحصيلي"), ("C24", "SAT 1 1300 بدل التحصيلي"), ("C07", "SAT I + SAT II")], "H", "F-05"),
 ("مستند الهوية", [("C26,C30", "Saudi ID فقط"), ("C24,C25,C27,C28", "Saudi ID أو Iqama"), ("C07", "National ID لطالب بلا إقامة")], "M", "F-13"),
 ("التخصصات ذات الشروط الخاصة", [("C30", "7 تخصصات"), ("C36", "8 + «etc.»"), ("C02", "الهندسة الكيميائية والأمن السيبراني دون شروط")], "M", "F-34"),
 ("قناة التقديم", [("C03", "قبول (سعوديون) / ادرس في السعودية — Closed (غير سعوديين)"), ("C06,C08", "بوابة PMU للجميع"), ("C07", "«completed entirely online»")], "H", "F-02"),
 ("أسماء برامج الدراسات العليا", [("C09", "Master of Human Development · Doctorate in ME"), ("C14", "Master of Science in Human Development"), ("C21", "…Education and Human Development · Doctoral program")], "M", "F-25"),
 ("قائمة برامج الدراسات العليا", [("الصفحة الرئيسية", "11 رابطًا"), ("C09", "10 — دون EMGMS"), ("C21", "12 + Pre-Master"), ("C07", "3 للدوليين")], "M", "F-25"),
]

# Correction to the existing register, found while re-reading
CORRECTIONS = [
 ("F-26", "لم تُعَد إنتاجها في 2026-09-28: أقسام «Educational Background» و«Personal Interview» في EMBA (C12)، و«Personal Interview» في PhD-BA (C11)، و«Educational Background» في MSME (C15) و MA IBL (C20)، وقائمة معايير وإجراءات التحضيرية (C25) — كلها موجودة الآن وظاهرة للزائر وفي HTML الخادم. لا يمكن من هنا تحديد إن كانت PMU أضافتها بعد 2026-09-27 أم أن القراءة السابقة أخطأت. الجزء الذي ما زال قائمًا: «30% for the written test» غير موصوف (C20)، وعنوان «Work Experience» الفارغ في MSHD (C14) جديد."),
]

# 2026-09-28 — the owner approved adding the new observations to the findings register.
# The 31 "NEW" observations are consolidated into 15 register findings (F-31–F-45); the MSHD
# empty "Work Experience" heading joins F-26 (same defect type). Applied here so every output
# (HTML, MD, JSON, EN report) cites the register ID.
REGISTER_MAP = {
 ("C07", 1): "F-31", ("C27", 1): "F-31", ("C28", 1): "F-31",
 ("C20", 1): "F-32",
 ("C20", 3): "F-33", ("C32", 1): "F-33",
 ("C30", 1): "F-34", ("C36", 1): "F-34",
 ("C23", 3): "F-35", ("C28", 2): "F-35",
 ("C11", 1): "F-36",
 ("C11", 2): "F-37", ("C01", 1): "F-37",
 ("C07", 5): "F-38", ("C09", 3): "F-38",
 ("C24", 4): "F-39",
 ("C10", 2): "F-40", ("C14", 2): "F-40", ("C25", 1): "F-40",
 ("C16", 1): "F-41", ("C17", 1): "F-41", ("C18", 1): "F-41", ("C20", 5): "F-41",
 ("C12", 2): "F-42", ("C13", 2): "F-42",
 ("C07", 6): "F-43", ("C03", 4): "F-43",
 ("C02", 2): "F-44", ("C07", 7): "F-44",
 ("C05", 2): "F-45",
 ("C14", 1): "F-26",
}
_left = []
for _k, _p in PAGES.items():
    for _n, _i in enumerate(_p["issues"], 1):
        if _i[5] == "NEW":
            if (_k, _n) not in REGISTER_MAP:
                _left.append((_k, _n))
            else:
                _p["issues"][_n - 1] = _i[:5] + (REGISTER_MAP[(_k, _n)],)
assert not _left, f"unmapped NEW observations: {_left}"
assert len(REGISTER_MAP) == 31
