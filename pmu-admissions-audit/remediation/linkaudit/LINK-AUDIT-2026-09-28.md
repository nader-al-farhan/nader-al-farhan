# تدقيق روابط صفحة Admissions Office — 2026-09-28

**الصفحة:** https://pmu.edu.sa/admission/admission · **وقت التشغيل:** 2026-09-28T04:36:14+00:00 UTC · **الطريقة:** قراءة فقط (لا نقر، لا نماذج، لا تسجيل دخول).

- روابط `<a>` في الصفحة: **133** (رأس 62، مسار تنقّل 2، محتوى 36، تذييل 32، ورابط فارغ بلا href)
- عناوين فريدة: **114** — اختُبر 107؛ أعاد 200 نهائيًا 106؛ مرّ بتحويل 84؛ لم يُختبر 7 (خارج النطاق المتاح).
- روابط «#»: 6

## ملاحظات على مستوى الصفحة

| الخطورة | الملاحظة | المعالجة |
|---|---|---|
| عالية | لا توجد سمة lang على وسم <html> (F-29)، ولا رابط لنسخة عربية من الصفحة في HTML | إضافة lang ونسخة عربية مكافئة (G5) |
| متوسطة | 33 من 36 رابط محتوى تمر بتحويل واحد على الأقل، و32 منها بسلسلة من خطوتين أو أكثر (مثال: Upper-case .aspx → lower-case .aspx → بدون امتداد) | ربط كل رابط بعنوانه النهائي مباشرة (أداء + SEO) |
| متوسطة | ثلاث نقاط تقديم مختلفة في الصفحة نفسها: C06/C08 (www.pmu.edu.sa/apply) + قائمة الرأس «Apply to PMU» (apply.aspx) — كلها تنتهي عند البوابة | زر تقديم واحد مع مُوجِّه أهلية |
| منخفضة | قائمة «Research Centers» مكررة في الرأس (نسختان: 9 و10 روابط؛ «Additive Manufacturing…» في الثانية فقط) | مصدر واحد للقائمة |
| منخفضة | رابط فارغ بلا href داخل مجموعة «Undergraduate Placement Tests» ورابط مخفي «#sidebar» | حذف العناصر الفارغة |
| متوسطة | «Objectives» في قائمة About بالرأس رابطه «#» (لا يعمل) | ربطه بصفحة الأهداف أو حذفه |
| منخفضة | «SIGN IN» في الرأس href=«javascript:void(0);» — غير قابل للوصول بلوحة المفاتيح كرابط | استخدام <button> لقائمة منسدلة |

## الروابط رابطًا رابطًا

| # | المنطقة / المجموعة | النص | الحالة | الملاحظات | المعالجة | الخطورة | لقطة |
|---|---|---|---|---|---|---|---|
| B1 | مسار التنقّل /  | [Home](https://pmu.edu.sa/Default.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://faculty.pmu.edu.sa/pmufaculties/» | الربط بالعنوان النهائي مباشرة<br>تحويلها إلى https | متوسطة | [B1](shots/B1.jpg) |
| B2 | مسار التنقّل /  | [Study @ PMU](https://pmu.edu.sa/admission/Admission-Registration.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://faculty.pmu.edu.sa/PMUStaffs/DepartmentStaffList/4» | الربط بالعنوان النهائي مباشرة<br>تحويلها إلى https | متوسطة | [B2](shots/B2.jpg) |
| C01 | محتوى الصفحة / Future Students | [Overview](https://pmu.edu.sa/Admission/Future_Students_RO.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C01](shots/C01.jpg) |
| C02 | محتوى الصفحة / Future Students | [Degrees & Programs](https://pmu.edu.sa/Admission/Degrees_Programs_FS_RO.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C02](shots/C02.jpg) |
| C03 | محتوى الصفحة / Future Students | [Admissions Calendar](https://pmu.edu.sa/Admission/Admission_Calendar_FS_RO.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>عنوان الصفحة H1 «ADMISSIONS CALENDARS» (جمع) بينما الرابط «Admissions Calendar» | الربط بالعنوان النهائي مباشرة<br>توحيد التسمية | منخفضة | [C03](shots/C03.jpg) |
| C04 | محتوى الصفحة / Future Students | [Contact Us](https://pmu.edu.sa/Staff_Profile/Staff_List.aspx?&DEpt=4&Name=Staff%20Name) | 200 (3 تحويل) | سلسلة تحويل (3): 301 → 301 → 302 → 200<br>«Contact Us» ينتهي بقائمة موظفين على faculty.pmu.edu.sa (أسماء شخصية) بدل قناة تواصل موحّدة للقبول، والسلسلة تمرّ بخطوة http:// غير مشفّرة (https→http→https) | الربط بالعنوان النهائي مباشرة<br>ربط «تواصل معنا» بصفحة تواصل موحّدة للقبول (بريد/هاتف/ساعات عمل) عبر https مباشرة؛ لم تُلتقط صورة لأن الصفحة تعرض أسماء | عالية | لم تُلتقط: الصفحة تعرض أسماء موظفين |
| C05 | محتوى الصفحة / Future Students | [Admission Query](https://pmu.edu.sa/Admission/admissions_queries) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200<br>يظهر بلون برتقالي وبإزاحة مختلفة عن بقية روابط المجموعة (مع C24) — عدم اتساق بصري | الربط بالعنوان النهائي مباشرة<br>توحيد نمط الروابط في القائمة | منخفضة | [C05](shots/C05.jpg) |
| C06 | محتوى الصفحة / Future Students | [Apply Now](https://www.pmu.edu.sa/apply) | 200 (0 تحويل) | «Apply Now» و C08 «Apply» يذهبان لنفس البوابة (admissions.pmu.edu.sa/welcome) بتسميتين مختلفتين، وهي إحدى 5 نقاط تقديم متعارضة (P14 يوجّه السعوديين إلى «قبول» وغير السعوديين إلى «ادرس في السعودية») | نقطة تقديم واحدة مع مُوجِّه أهلية (انظر مخطط الـ Blueprint: R1–R6) | عالية | البوابة تطبيق JavaScript لم يُعرض بطريقة الالتقاط هذه |
| C07 | محتوى الصفحة / International Students’ Office | [International Students without Saudi Residence](https://pmu.edu.sa/Admission/International_Students.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>نص «SAT II» (اختبار أُلغي دوليًا) موجود في HTML الصفحة (F-05) ولم يظهر في الجزء المرئي عند الالتقاط | الربط بالعنوان النهائي مباشرة<br>حذف مرجع SAT II وتحديث متطلبات الطلاب الدوليين | متوسطة | [C07](shots/C07.jpg) |
| C08 | محتوى الصفحة / International Students’ Office | [Apply](https://www.pmu.edu.sa/apply) | 200 (0 تحويل) | رابط التقديم للطلاب الدوليين يذهب للبوابة العامة نفسها دون توضيح القناة الخاصة بغير المقيمين | توجيه حسب الأهلية بدل رابط عام | عالية | البوابة تطبيق JavaScript لم يُعرض بطريقة الالتقاط هذه |
| C09 | محتوى الصفحة / Graduate Admissions | [Home](https://pmu.edu.sa/Admission/Admission_Graduate_Degree_Programs.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C09](shots/C09.jpg) |
| C10 | محتوى الصفحة / Graduate Admissions | [Admissions to the PhD in Mechanical Engineering Program](https://pmu.edu.sa/Admission/application_form_deme_gdp.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الرابط «PhD in Mechanical Engineering» يفتح عنوان URL «application_form_deme_gdp» وعنوان تبويب <title> «Application Form for MSDH» — عنوان برنامج آخر<br>خطأ إملائي في H1: «ADMISSSIONS» (ثلاث S) | الربط بالعنوان النهائي مباشرة<br>تصحيح <title> والـ URL للبرنامج الصحيح<br>تصحيح الإملاء | عالية | [C10](shots/C10.jpg) |
| C11 | محتوى الصفحة / Graduate Admissions | [Admissions to the PhD in Business Administration Program](https://pmu.edu.sa/Admission/Admissions_Requirements_phdba_gdp.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C11](shots/C11.jpg) |
| C12 | محتوى الصفحة / Graduate Admissions | [Admissions to the EMBA Program](https://pmu.edu.sa/Admission/Admissions_Requirements_EMBA_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C12](shots/C12.jpg) |
| C13 | محتوى الصفحة / Graduate Admissions | [Admissions to the MBA Program](https://pmu.edu.sa/Admission/Admissions_Requirements_MBA_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C13](shots/C13.jpg) |
| C14 | محتوى الصفحة / Graduate Admissions | [Admissions to the MSHD Program](https://pmu.edu.sa/Admission/Admissions_Requirements_MSEHD_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الرابط «MSHD» بينما الـ URL «msehd» وعنوان H1 عام «ADMISSIONS REQUIREMENTS» دون اسم البرنامج | الربط بالعنوان النهائي مباشرة<br>توحيد اختصار البرنامج وإضافة اسمه للعنوان | متوسطة | [C14](shots/C14.jpg) |
| C15 | محتوى الصفحة / Graduate Admissions | [Admissions to the MSME Program](https://pmu.edu.sa/Admission/Admissions_Requirements_MSME_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>خطأ إملائي في H1: «MSME ADMISSSIONS REQUIREMENTS» | الربط بالعنوان النهائي مباشرة<br>تصحيح الإملاء | متوسطة | [C15](shots/C15.jpg) |
| C16 | محتوى الصفحة / Graduate Admissions | [Admissions to the MSEE Program](https://pmu.edu.sa/Admission/application_form_msee_gdp.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>خطأ إملائي في H1 «MSEE ADMISSSIONS REQUIREMENTS»؛ والـ URL «application_form_…» لصفحة متطلبات وليست نموذجًا | الربط بالعنوان النهائي مباشرة<br>تصحيح الإملاء والمسار | متوسطة | [C16](shots/C16.jpg) |
| C17 | محتوى الصفحة / Graduate Admissions | [Admissions to the MSCE Program](https://pmu.edu.sa/Admission/application_form_MSCE_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>خطأ إملائي في H1 «MSCE ADMISSSIONS REQUIREMENTS»؛ الـ URL «application_form_…» | الربط بالعنوان النهائي مباشرة<br>تصحيح الإملاء والمسار | متوسطة | [C17](shots/C17.jpg) |
| C18 | محتوى الصفحة / Graduate Admissions | [Admissions to the MSID Program](https://pmu.edu.sa/Admission/application_form_MSID_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>خطأ إملائي في H1 «MSID ADMISSSIONS REQUIREMENTS»؛ الـ URL «application_form_…» | الربط بالعنوان النهائي مباشرة<br>تصحيح الإملاء والمسار | متوسطة | [C18](shots/C18.jpg) |
| C19 | محتوى الصفحة / Graduate Admissions | [Admissions to the EMGMS Program](https://pmu.edu.sa/Admission/Admissions_Requirements_emgms_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>نص معيب موثّق في الصفحة المستهدفة: «CESL» (F-21) | الربط بالعنوان النهائي مباشرة<br>تصحيح المحتوى وفق سجل الملاحظات | عالية | [C19](shots/C19.jpg) |
| C20 | محتوى الصفحة / Graduate Admissions | [Admissions to the MIBL](https://pmu.edu.sa/Admission/Admissions_Requirements_MIlBL_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الـ URL يحوي «MIlBL» (حرف l صغير زائد)؛ H1 «MIBL ADMISSSIONS REQUIREMENTS»؛ نص الرابط بلا كلمة «Program» خلافًا لبقية المجموعة | الربط بالعنوان النهائي مباشرة<br>تصحيح المسار والإملاء والتسمية | متوسطة | [C20](shots/C20.jpg) |
| C21 | محتوى الصفحة / Graduate Admissions | [Tuition & Fees](https://pmu.edu.sa/Admission/Post_Graduate_Fees_TF_RO.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>صفحة الرسوم تنتقل بالزائر لقسم «Registration Office» (تتغير القائمة الجانبية)، فيفقد سياق القبول | الربط بالعنوان النهائي مباشرة<br>إبقاء الرسوم ضمن رحلة القبول أو إضافة مسار عودة واضح | منخفضة | [C21](shots/C21.jpg) |
| C22 | محتوى الصفحة / Graduate Admissions | [Contact Info](https://pmu.edu.sa/Admission/Admission_Contact_GDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C22](shots/C22.jpg) |
| C23 | محتوى الصفحة / Undergraduate Admissions | [Home](https://pmu.edu.sa/Admission/Undergraduate_Programs_Admission.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>نص معيب موثّق في الصفحة المستهدفة: «College of Medical» (F-17) | الربط بالعنوان النهائي مباشرة<br>تصحيح المحتوى وفق سجل الملاحظات | متوسطة | [C23](shots/C23.jpg) |
| C24 | محتوى الصفحة / Undergraduate Admissions | [Admission to the College of Medicine](https://pmu.edu.sa/admission/college_of_medicine_admission) | 200 (0 تحويل) | نص معيب موثّق في الصفحة المستهدفة: «the process typically involves» (F-07)<br>نص معيب موثّق في الصفحة المستهدفة: «to be developed in launch phase» (F-07)<br>نص معيب موثّق في الصفحة المستهدفة: «College of Medical» (F-17)<br>بلون/إزاحة مختلفة عن بقية المجموعة (مع C05) | تصحيح المحتوى وفق سجل الملاحظات<br>توحيد النمط | عالية | [C24](shots/C24.jpg) |
| C25 | محتوى الصفحة / Undergraduate Admissions | [Admissions to the Preparatory Program](https://pmu.edu.sa/Admission/Admission-to-the-Preparatory-Program.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C25](shots/C25.jpg) |
| C26 | محتوى الصفحة / Undergraduate Admissions | [Direct Admissions from Secondary School](https://pmu.edu.sa/Admission/Direct-Admissions-from-Secondary-School.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://www.pmu.edu.sa/Admission/Admission_Calendar_FS_RO.aspx» | الربط بالعنوان النهائي مباشرة<br>تحويلها إلى https | متوسطة | [C26](shots/C26.jpg) |
| C27 | محتوى الصفحة / Undergraduate Admissions | [Admissions from Other Universities](https://pmu.edu.sa/Admission/Admission-from-Other-Universities.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>نص معيب موثّق في الصفحة المستهدفة: «http://admissions.pmu.edu.sa» (F-16)<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://admissions.pmu.edu.sa/»، «http://www.pmu.edu.sa/Admission/Admission_Calendar_FS_RO.aspx» | الربط بالعنوان النهائي مباشرة<br>تصحيح المحتوى وفق سجل الملاحظات<br>تحويلها إلى https | متوسطة | [C27](shots/C27.jpg) |
| C28 | محتوى الصفحة / Undergraduate Admissions | [Visting Students](https://pmu.edu.sa/Admission/Visiting-Student-Admission.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>نص معيب موثّق في الصفحة المستهدفة: «http://admissions.pmu.edu.sa» (F-16)<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://admissions.pmu.edu.sa/»<br>خطأ إملائي في نص الرابط: «Visting Students» (F-17) | الربط بالعنوان النهائي مباشرة<br>تصحيح المحتوى وفق سجل الملاحظات<br>تحويلها إلى https<br>تصحيحه إلى «Visiting Students» | متوسطة | [C28](shots/C28.jpg) |
| C29 | محتوى الصفحة / Undergraduate Admissions | [Admissions from the Preparatory Program](https://pmu.edu.sa/Admission/Admission-from-the-Prep-to-UG-Programs.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C29](shots/C29.jpg) |
| C30 | محتوى الصفحة / Undergraduate Admissions | [Computer Science and Engineering Majors Admission Requirements](https://pmu.edu.sa/Admission/Admissions_Requirements_CS_Eng_Majors.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>نص معيب موثّق في الصفحة المستهدفة: «http://admissions.pmu.edu.sa» (F-16)<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://admissions.pmu.edu.sa/»، «http://www.pmu.edu.sa/Admission/Admission_Calendar_FS_RO.aspx»، «http://pmu.edu.sa/Admission/Overview-Undergraduate-Placement-Tests.aspx» | الربط بالعنوان النهائي مباشرة<br>تصحيح المحتوى وفق سجل الملاحظات<br>تحويلها إلى https | متوسطة | [C30](shots/C30.jpg) |
| C31 | محتوى الصفحة / Undergraduate Admissions | [Tuition & Fees](https://pmu.edu.sa/Admission/Fees_TF_RO.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>كما في C21: الصفحة ضمن قسم «Registration Office» | الربط بالعنوان النهائي مباشرة<br>كما في C21 | منخفضة | [C31](shots/C31.jpg) |
| C32 | محتوى الصفحة / Undergraduate Placement Tests | [Overview](https://pmu.edu.sa/Admission/Overview-Undergraduate-Placement-Tests.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C32](shots/C32.jpg) |
| C33 | محتوى الصفحة / Undergraduate Placement Tests | [Aptis](https://pmu.edu.sa/Admission/Aptis-Placement-Test.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C33](shots/C33.jpg) |
| C34 | محتوى الصفحة / Undergraduate Placement Tests | [IELTS](https://pmu.edu.sa/Admission/IELTS-Admission.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة تربط بمركز اختبار IELTS عبر http:// (يُحوَّل إلى https) | الربط بالعنوان النهائي مباشرة<br>استخدام https مباشرة | منخفضة | [C34](shots/C34.jpg) |
| C35 | محتوى الصفحة / Undergraduate Placement Tests | [TOEFL](https://pmu.edu.sa/Admission/TOEFL-Admission.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C35](shots/C35.jpg) |
| C36 | محتوى الصفحة / Undergraduate Placement Tests | [Scholastic Aptitude Test (SAT)](https://pmu.edu.sa/Admission/SAT-Admission.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [C36](shots/C36.jpg) |
| F01 | التذييل / STAY CONNECTED | [(أيقونة)](https://twitter.com/PMU_KSA) | لم يُختبر | لم يُختبر: نطاق خارج pmu.edu.sa غير متاح من بيئة التدقيق<br>حسابان مختلفان على Twitter/X في التذييل (F01 «PMU_KSA» و F02 «pmuofficial») — أيهما الرسمي غير موضّح | إبقاء الحساب الرسمي فقط وتحديث العلامة إلى X | منخفضة | — |
| F02 | التذييل / STAY CONNECTED | [(أيقونة)](https://twitter.com/pmuofficial) | لم يُختبر | لم يُختبر: نطاق خارج pmu.edu.sa غير متاح من بيئة التدقيق | — | — | — |
| F03 | التذييل / STAY CONNECTED | [(أيقونة)](https://www.facebook.com/pmuofficial) | لم يُختبر | لم يُختبر: نطاق خارج pmu.edu.sa غير متاح من بيئة التدقيق | — | — | — |
| F04 | التذييل / STAY CONNECTED | [(أيقونة)](https://www.linkedin.com/school/prince-mohammad-bin-fahd-university) | لم يُختبر | لم يُختبر: نطاق خارج pmu.edu.sa غير متاح من بيئة التدقيق | — | — | — |
| F05 | التذييل / STAY CONNECTED | [(أيقونة)](https://www.youtube.com/user/PMUOfficial) | لم يُختبر | لم يُختبر: نطاق خارج pmu.edu.sa غير متاح من بيئة التدقيق | — | — | — |
| F06 | التذييل / STAY CONNECTED | [(أيقونة)](https://www.instagram.com/pmu_official/) | لم يُختبر | لم يُختبر: نطاق خارج pmu.edu.sa غير متاح من بيئة التدقيق | — | — | — |
| F07 | التذييل / STAY CONNECTED | [(أيقونة)](https://pmu.edu.sa/admission/admission#) | 200 (0 تحويل) | «#» يعيد تحميل الصفحة نفسها<br>أيقونة RSS برابط «#» (لا تؤدي لشيء) | إزالتها أو ربطها بموجز فعلي | متوسطة | [F07](shots/F07.jpg) |
| F08 | التذييل / FIND @ PMU | [Academic Calendar](https://pmu.edu.sa/Admission/academic_calendar_2021_2022_ro.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>«Academic Calendar» في التذييل يفتح «ACADEMIC CALENDAR 2021 / 2022» — تقويم منتهٍ منذ 4 سنوات (F-12)<br>الصفحة المستهدفة تحوي رابطًا إلى خادم داخلي (http://web1:8066/…) لا يعمل للجمهور | الربط بالعنوان النهائي مباشرة<br>ربطه بالتقويم الحالي<br>إزالة الرابط الداخلي | عالية | [F08](shots/F08.jpg) |
| F09 | التذييل / FIND @ PMU | [Careers](https://pmu.taleo.net/careersection/ex/jobsearch.ftl) | لم يُختبر | لم يُختبر: نطاق خارج pmu.edu.sa غير متاح من بيئة التدقيق | — | — | — |
| F10 | التذييل / FIND @ PMU | [Global Engagement](https://pmu.edu.sa/global-engagement/) | 200 (0 تحويل) | — | — | — | [F10](shots/F10.jpg) |
| F11 | التذييل / FIND @ PMU | [Sports Center Schedule](https://pmu.edu.sa/life_pmu/sportscenterschedule.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200<br>عنوان التبويب «SportsSports Center Schedule For 2024» — كلمة مكررة وسنة سابقة؛ 38 صورة بلا alt | الربط بالعنوان النهائي مباشرة<br>تحديث العنوان والسنة ونص alt | منخفضة | [F11](shots/F11.jpg) |
| F12 | التذييل / FIND @ PMU | [President's Office](https://pmu.edu.sa/About/Welcome_Rector.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>يُحوَّل عبر JavaScript من welcome_rector إلى welcome_president (تحويل من جهة المتصفح) | الربط بالعنوان النهائي مباشرة | منخفضة | [F12](shots/F12.jpg) |
| F13 | التذييل / FIND @ PMU | [Dining](https://pmu.edu.sa/Life_Pmu/Dining_CL.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F13](shots/F13.jpg) |
| F14 | التذييل / FIND @ PMU | [News](https://pmu.edu.sa/news/more_news.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F14](shots/F14.jpg) |
| F15 | التذييل / FIND @ PMU | [Events](https://pmu.edu.sa/news/more_events.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F15](shots/F15.jpg) |
| F16 | التذييل / FIND @ PMU | [PMU Album](https://pmu.edu.sa/gallary.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200<br>خطأ إملائي في عنوان الصفحة والمسار: «PMU Gallary» / gallary | الربط بالعنوان النهائي مباشرة<br>تصحيحه إلى Gallery مع تحويل 301 | منخفضة | [F16](shots/F16.jpg) |
| F17 | التذييل / COLLEGES / PROGRAMS | [College of Engineering](https://pmu.edu.sa/Academics/College_of_Engineering_UDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>قائمة الكليات في التذييل (7 روابط) لا تتضمن كلية الطب، بينما قائمة الرأس تتضمنها | الربط بالعنوان النهائي مباشرة<br>إضافة كلية الطب للتذييل | متوسطة | [F17](shots/F17.jpg) |
| F18 | التذييل / COLLEGES / PROGRAMS | [College of Computer Engineering & Sciences](https://pmu.edu.sa/Academics/College_Computer_Engineering_Science_UDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://faculty.pmu.edu.sa/PMUFaculties/CollegeFacultyList/3» | الربط بالعنوان النهائي مباشرة<br>تحويلها إلى https | متوسطة | [F18](shots/F18.jpg) |
| F19 | التذييل / COLLEGES / PROGRAMS | [College of Business](https://pmu.edu.sa/Academics/College_Business_Administration_UDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://faculty.pmu.edu.sa/PMUFaculties/CollegeFacultyList/1»<br>التسمية «College of Business» بينما الرأس والصفحة «College of Business Administration» | الربط بالعنوان النهائي مباشرة<br>تحويلها إلى https<br>توحيد الاسم | متوسطة | [F19](shots/F19.jpg) |
| F20 | التذييل / COLLEGES / PROGRAMS | [College of Law](https://pmu.edu.sa/Academics/law_dept_cshs_udp.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://faculty.pmu.edu.sa/PMUFaculties/CollegeFacultyList/14» | الربط بالعنوان النهائي مباشرة<br>تحويلها إلى https | متوسطة | [F20](shots/F20.jpg) |
| F21 | التذييل / COLLEGES / PROGRAMS | [College of Architecture and Design](https://pmu.edu.sa/Academics/College_of_Architecture_Design_UDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F21](shots/F21.jpg) |
| F22 | التذييل / COLLEGES / PROGRAMS | [College of Sciences and Human Studies](https://pmu.edu.sa/Academics/College_Sciences_Human_Studies_UDP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://faculty.pmu.edu.sa/PMUFaculties/CollegeFacultyList/4» | الربط بالعنوان النهائي مباشرة<br>تحويلها إلى https | متوسطة | [F22](shots/F22.jpg) |
| F23 | التذييل / COLLEGES / PROGRAMS | [Preparatory Program](https://pmu.edu.sa/Academics/Overview_PP.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>الصفحة المستهدفة تحوي روابط http:// غير مشفّرة: «http://faculty.pmu.edu.sa/PMUFaculties/CollegeFacultyList/5» | الربط بالعنوان النهائي مباشرة<br>تحويلها إلى https | متوسطة | [F23](shots/F23.jpg) |
| F24 | التذييل / RESOURCES | [Campus Map](https://pmu.edu.sa/Life_PMU/Campus_Life.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200<br>«Campus Map» يفتح صفحة «Campus Life» (نظرة عامة) وليس خريطة؛ الخريطة الفعلية على about/maps (F31) | الربط بالعنوان النهائي مباشرة<br>ربطه بصفحة الخرائط | متوسطة | [F24](shots/F24.jpg) |
| F25 | التذييل / RESOURCES | [Directory](https://pmu.edu.sa/admission/admission#) | 200 (0 تحويل) | نص معيب موثّق في الصفحة المستهدفة: «Visting» (F-17)<br>«Directory» برابط «#» (لا يعمل) | تصحيح المحتوى وفق سجل الملاحظات<br>ربطه بدليل فعلي أو إزالته | متوسطة | — |
| F26 | التذييل / RESOURCES | [EAIP](https://pmu.edu.sa/resources_services/engineering_technical_affairs.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F26](shots/F26.jpg) |
| F27 | التذييل / RESOURCES | [IT Services](https://pmu.edu.sa/resources_services/sections_it_dept.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F27](shots/F27.jpg) |
| F28 | التذييل / RESOURCES | [Library Services](https://pmu.edu.sa/resources_services/library_services_lrc.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F28](shots/F28.jpg) |
| F29 | التذييل / RESOURCES | [SiteMap](https://pmu.edu.sa/admission/admission#) | 200 (0 تحويل) | نص معيب موثّق في الصفحة المستهدفة: «Visting» (F-17)<br>«SiteMap» برابط «#» (لا يعمل) | تصحيح المحتوى وفق سجل الملاحظات<br>نشر خريطة موقع فعلية | متوسطة | — |
| F30 | التذييل / GET IN TOUCH | [EMPLOYMENT](https://pmu.edu.sa/hr/hr.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F30](shots/F30.jpg) |
| F31 | التذييل / GET IN TOUCH | [MAPS & LOCATIONS](https://pmu.edu.sa/about/maps.aspx) | 200 (1 تحويل) | سلسلة تحويل (1): 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F31](shots/F31.jpg) |
| F32 | التذييل / GET IN TOUCH | [CONTACT](https://pmu.edu.sa/About/Contact_Us.aspx) | 200 (2 تحويل) | سلسلة تحويل (2): 301 → 301 → 200 | الربط بالعنوان النهائي مباشرة | منخفضة | [F32](shots/F32.jpg) |

## روابط الرأس (قوائم منسدلة مشتركة في الموقع كله)

| # | النص | href | الحالة |
|---|---|---|---|
| H01 | (أيقونة) | `https://www.pmu.edu.sa/` | 200 |
| H02 | (أيقونة) | `` | 200 |
| H03 | PMU | `/` | 200 |
| H04 | (أيقونة) | `#` | 200 |
| H05 | (أيقونة) | `#` | 200 |
| H06 | ABOUT | `../about/about.aspx` | 200 |
| H07 | Vision & Mission | `../about/uni-vision-mission.aspx` | 200 |
| H08 | Objectives | `#` | 200 |
| H09 | Values | `../about/uni-values.aspx` | 200 |
| H10 | Governance | `../about/Governance.aspx` | 200 |
| H11 | Deanships | `../about/deanships.aspx` | 200 |
| H12 | Publications & Presentations | `../about/puplications_presntations.aspx` | 200 |
| H13 | STUDY AT PMU | `../admission/admission-registration.aspx` | 200 |
| H14 | Admission Office | `../admission/Admission.aspx` | 200 |
| H15 | Apply to PMU | `../apply.aspx` | 200 |
| H16 | Financial Aid | `../admission/financial_aid_ro.aspx` | 200 |
| H17 | Registration | `../admission/registration_office.aspx` | 200 |
| H18 | Tuition & Fees | `../admission/tuition_fees_ro.aspx` | 200 |
| H19 | ACADEMICS | `../academics/academics.aspx` | 200 |
| H20 | College of Engineering | `../academics/college_of_engineering_udp.aspx` | 200 |
| H21 | College of Computer Engineering & Sciences | `../academics/college_computer_engineering_science_udp.aspx` | 200 |
| H22 | College of Business Administration | `../academics/college_business_administration_udp.aspx` | 200 |
| H23 | College of LAW | `../academics/law_dept_cshs_udp.aspx` | 200 |
| H24 | College of Architecture and Design | `../Academics/College_of_Architecture_Design_UDP.aspx` | 200 |
| H25 | College of Sciences & Human Studies | `../academics/college_sciences_human_studies_udp.aspx` | 200 |
| H26 | College of Medicine | `../academics/college_of_medicine_udp.aspx` | 200 |
| H27 | Preparatory Program | `../academics/overview_pp.aspx` | 200 |
| H28 | PMU Logo | `/` | 200 |
| H29 | RESEARCH | `https://pmu.edu.sa/research/` | 200 |
| H30 | Research Centers | `https://pmu.edu.sa/research/research_center` | 200 |
| H31 | Center for Future Studies | `https://pmfcfs.pmu.edu.sa/Default.aspx` | 200 |
| H32 | Center for Artificial Intelligence | `https://pmu.edu.sa/ai/default` | 200 |
| H33 | Center for Cyber Security | `https://pmu.edu.sa/cybersecurity/` | 200 |
| H34 | Patent Center | `https://pmu.edu.sa/Patent-Center/` | 200 |
| H35 | Center of Environment & Water Solutions | `https://pmu.edu.sa/cews/` | 200 |
| H36 | Space Research Center | `https://pmu.edu.sa/sarc/` | 200 |
| H37 | Centre for Sustainable Business & Innovation | `https://pmu.edu.sa/csbi/` | 200 |
| H38 | Centre for Sustainable Infrastructure Materials | `https://pmu.edu.sa/sim/` | 200 |
| H39 | Research Centers | `https://pmu.edu.sa/research/research_center` | 200 |
| H40 | Center for Future Studies | `https://pmfcfs.pmu.edu.sa/Default.aspx` | 200 |
| H41 | Center for Artificial Intelligence | `https://pmu.edu.sa/ai/default` | 200 |
| H42 | Center for Cyber Security | `https://pmu.edu.sa/cybersecurity/` | 200 |
| H43 | Patent Center | `https://pmu.edu.sa/Patent-Center/` | 200 |
| H44 | Center of Environment & Water Solutions | `https://pmu.edu.sa/cews/` | 200 |
| H45 | Space Research Center | `https://pmu.edu.sa/sarc/` | 200 |
| H46 | Additive Manufacturing Research & Innovation Center | `https://pmu.edu.sa/amric/` | 200 |
| H47 | Centre for Sustainable Business & Innovation | `https://pmu.edu.sa/csbi/` | 200 |
| H48 | Centre for Sustainable Infrastructure Materials | `https://pmu.edu.sa/sim/` | 200 |
| H49 | STUDENTS LIFE | `../life_pmu/life_pmu.aspx` | 200 |
| H50 | Campus Life | `../life_pmu/campus_life.aspx` | 200 |
| H51 | Health Care & Counseling Services | `../life_pmu/health_care_counseling_services.aspx` | 200 |
| H52 | Office of Special Needs | `../life_pmu/office_special_needs.aspx` | 200 |
| H53 | SIGN IN | `javascript:void(0);` | — |
| H54 | BlackBoard | `https://blackboard.pmu.edu.sa` | 200 |
| H55 | Banner Self Service | `https://www.pmu.edu.sa/login/banner-login.html` | 200 |
| H56 | Finance TicketingSystem | `https://financehelpdesk.pmu.edu.sa/login` | 200 |
| H57 | Web Mail | `https://www.pmu.edu.sa/login/index?Login=Login+Portal` | 200 |
| H58 | Library | `../resources_services/e_resources_lrc.aspx` | 200 |
| H59 | Employee Self Services | `https://iconnect.pmu.edu.sa/?login=Login+Portal` | 200 |
| H60 | Banner Workflow | `https://workflow.pmu.edu.sa/wfprod` | 200 |
| H61 | On Campus IT HelpDesk | `https://ithelpdesk.pmu.edu.sa/` | 0 |
| H62 | (أيقونة) | `#sidebar` | 200 |

## حدود الطريقة (حقيقة مقابل افتراض)

- الصفحات عُرضت في Chromium مع جلب كل طلب بـ curl (تحقق TLS كامل)؛ المتصفح لم يتصل بالشبكة مباشرة. البوابة (C06/C08) تطبيق JavaScript لم يُعرض بهذه الطريقة، فلا لقطة لها هنا (الدليل السابق F-08 قائم).
- النطاقات خارج pmu.edu.sa (Twitter/X، Facebook، LinkedIn، YouTube، Instagram، Taleo) غير متاحة من بيئة التدقيق فلم تُختبر.
- `http://admissions.pmu.edu.sa` أعاد 503 بنص «upstream connect error … connection timeout» ثلاث مرات — النص صادر عن وكيل البيئة لا عن PMU، لذلك **غير مؤكَّد** إن كان الخلل في الخادم.
- `ithelpdesk.pmu.edu.sa` رُفض بـ 502 عند CONNECT من وكيل البيئة — غير مختبر.
- صفحة قائمة الموظفين (C04) لم تُلتقط لأنها تعرض أسماء شخصية.
