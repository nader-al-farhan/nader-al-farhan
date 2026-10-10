# التدقيق السطري صفحة بصفحة — نطاق `pmu.edu.sa/admission/admission`

**تاريخ التدقيق:** 2026-10-10 · **الطريقة:** Chromium/Playwright (محاكاة موبايل 390px)، قراءة فقط، نص مُصيَّر كامل (يشمل الأكورديون/التبويبات)، قراءة سطرية بشرية لكل صفحة هدف، وتحقق حسابي وخارجي حيث لزم.

## 1. تعريف النطاق (مُقيَّد حسب طلبك)
- **العنصر 0:** الصفحة نفسها `https://pmu.edu.sa/admission/admission` بمحتوياتها.
- **العناصر 1–37:** الأهداف الفريدة الـ37 للروابط الموجودة في منطقة المحتوى (38 رابطاً، `Apply Now` و`Apply` يشيران إلى هدف واحد).
- **العنصر 38:** وجهة زر التقديم النهائية `admissions.pmu.edu.sa/welcome` (عرض فقط).
- **روابط الترويسة (61) والتذييل (32):** قوائم الموقع العامة (about/academics/research…) — **خارج النطاق** ولا تُدقَّق محتوىً؛ حالتها ضمن فحص الـ84 رابطاً (كلها 200 بعد التحويل).
- **ما بعد المستوى الأول** (صفحات الرسوم الفرعية، التقاويم الأكاديمية، المساعدات المالية، النماذج…): **مستبعد** ويظهر فقط كدليل مُدعِّم أو كملاحظات "ملاصقة" (ADJ).

## 2. الصفحة الرئيسية بمحتوياتها (العنصر 0)

| البند | القياس |
|---|---|
| العنوان | Admissions Office :: Study at PMU :: PMU :: Prince Mohammad Bin Fahd University |
| `lang` | فارغ (WCAG 3.1.1) |
| العناوين | `H1 Admissions Office`؛ `H2`: Future Students · International Students’ Office · Graduate Admissions · Undergraduate Admissions · Undergraduate Placement Tests |
| روابط المحتوى / الترويسة / التذييل | 39 / 61 / 32 |
| نص فقرات تعريفية | **لا يوجد** (قوائم روابط فقط) |
| الصور | 6 (4 بلا `alt`) |
| نماذج / iframe | نموذج 1 (بحث) · iframe بحث بلا عنوان |
| `meta description` / canonical | غير موجودين |
| `<main>` | غير موجود |
| تحميل الصفحة | 200 على `pmu.edu.sa` بلا تحويل إلى `www` |

### سطراً بسطر: محتوى الصفحة وروابطها
| # | النص الظاهر | الوجهة (كما في HTML) | الهدف المطبّع | HTTP | ملاحظات |
|---|---|---|---|---|---|
| 1 | Home | `../Default.aspx` | `/default` | 200 (فحص حالة) | تسمية مكررة F-37 |
| 2 | Study @ PMU | `Admission-Registration.aspx` | `/admission/admission-registration` | 200 |  |
| — | *(رابط فارغ)* | `#sidebar` | — | — | F-38 رابط بلا نص |
| 3 | Overview | `../Admission/Future_Students_RO.aspx` | `/admission/future_students_ro` | 200 |  |
| 4 | Degrees & Programs | `../Admission/Degrees_Programs_FS_RO.aspx` | `/admission/degrees_programs_fs_ro` | 200 |  |
| 5 | Admissions Calendar | `../Admission/Admission_Calendar_FS_RO.aspx` | `/admission/admission_calendar_fs_ro` | 200 |  |
| 6 | Contact Us | `../Staff_Profile/Staff_List.aspx?&DEpt=4&Name=Staff%20Name` | `/staff_profile/staff_list` | 200 (فحص حالة) | دليل الموظفين؛ URL به معامل `Name=Staff Name` placeholder |
| 7 | Admission Query | `../Admission/admissions_queries` | `/admission/admissions_queries` | 200 |  |
| 8 | Apply Now | `https://www.pmu.edu.sa/apply` | `/apply` | 200 | رابط مطلق بينما البقية نسبية `../Admission/X.aspx` |
| 9 | International Students without Saudi Residence | `../Admission/International_Students.aspx` | `/admission/international_students` | 200 |  |
| 10 | Apply | `https://www.pmu.edu.sa/apply` | `/apply` | 200 | رابط مطلق بينما البقية نسبية `../Admission/X.aspx` |
| 11 | Home | `../Admission/Admission_Graduate_Degree_Programs.aspx` | `/admission/admission_graduate_degree_programs` | 200 | تسمية مكررة F-37 |
| 12 | Admissions to the PhD in Mechanical Engineering Program | `../Admission/application_form_deme_gdp.aspx` | `/admission/application_form_deme_gdp` | 200 |  |
| 13 | Admissions to the PhD in Business Administration Program | `../Admission/Admissions_Requirements_phdba_gdp.aspx` | `/admission/admissions_requirements_phdba_gdp` | 200 |  |
| 14 | Admissions to the EMBA Program | `../Admission/Admissions_Requirements_EMBA_GDP.aspx` | `/admission/admissions_requirements_emba_gdp` | 200 |  |
| 15 | Admissions to the MBA Program | `../Admission/Admissions_Requirements_MBA_GDP.aspx` | `/admission/admissions_requirements_mba_gdp` | 200 |  |
| 16 | Admissions to the MSHD Program | `../Admission/Admissions_Requirements_MSEHD_GDP.aspx` | `/admission/admissions_requirements_msehd_gdp` | 200 |  |
| 17 | Admissions to the MSME Program | `../Admission/Admissions_Requirements_MSME_GDP.aspx` | `/admission/admissions_requirements_msme_gdp` | 200 |  |
| 18 | Admissions to the MSEE Program | `../Admission/application_form_msee_gdp.aspx` | `/admission/application_form_msee_gdp` | 200 |  |
| 19 | Admissions to the MSCE Program | `../Admission/application_form_MSCE_GDP.aspx` | `/admission/application_form_msce_gdp` | 200 |  |
| 20 | Admissions to the MSID Program | `../Admission/application_form_MSID_GDP.aspx` | `/admission/application_form_msid_gdp` | 200 |  |
| 21 | Admissions to the EMGMS Program | `../Admission/Admissions_Requirements_emgms_GDP.aspx` | `/admission/admissions_requirements_emgms_gdp` | 200 |  |
| 22 | Admissions to the MIBL | `../Admission/Admissions_Requirements_MIlBL_GDP.aspx` | `/admission/admissions_requirements_milbl_gdp` | 200 |  |
| 23 | Tuition & Fees | `../Admission/Post_Graduate_Fees_TF_RO.aspx` | `/admission/post_graduate_fees_tf_ro` | 200 | تسمية مكررة F-37 |
| 24 | Contact Info | `../Admission/Admission_Contact_GDP.aspx` | `/admission/admission_contact_gdp` | 200 |  |
| 25 | Home | `../Admission/Undergraduate_Programs_Admission.aspx` | `/admission/undergraduate_programs_admission` | 200 | تسمية مكررة F-37 |
| 26 | Admission to the College of Medicine | `../admission/college_of_medicine_admission` | `/admission/college_of_medicine_admission` | 200 |  |
| 27 | Admissions to the Preparatory Program | `../Admission/Admission-to-the-Preparatory-Program.aspx` | `/admission/admission-to-the-preparatory-program` | 200 |  |
| 28 | Direct Admissions from Secondary School | `../Admission/Direct-Admissions-from-Secondary-School.aspx` | `/admission/direct-admissions-from-secondary-school` | 200 |  |
| 29 | Admissions from Other Universities | `../Admission/Admission-from-Other-Universities.aspx` | `/admission/admission-from-other-universities` | 200 |  |
| 30 | Visting Students | `../Admission/Visiting-Student-Admission.aspx` | `/admission/visiting-student-admission` | 200 | خطأ إملائي F-14 |
| 31 | Admissions from the Preparatory Program | `../Admission/Admission-from-the-Prep-to-UG-Programs.aspx` | `/admission/admission-from-the-prep-to-ug-programs` | 200 |  |
| 32 | Computer Science and Engineering Majors Admission Requirem | `../Admission/Admissions_Requirements_CS_Eng_Majors.aspx` | `/admission/admissions_requirements_cs_eng_majors` | 200 |  |
| 33 | Tuition & Fees | `../Admission/Fees_TF_RO.aspx` | `/admission/fees_tf_ro` | 200 | تسمية مكررة F-37 |
| 34 | Overview | `../Admission/Overview-Undergraduate-Placement-Tests.aspx` | `/admission/overview-undergraduate-placement-tests` | 200 |  |
| 35 | Aptis | `../Admission/Aptis-Placement-Test.aspx` | `/admission/aptis-placement-test` | 200 |  |
| 36 | IELTS | `../Admission/IELTS-Admission.aspx` | `/admission/ielts-admission` | 200 |  |
| 37 | TOEFL | `../Admission/TOEFL-Admission.aspx` | `/admission/toefl-admission` | 200 |  |
| 38 | Scholastic Aptitude Test (SAT) | `../Admission/SAT-Admission.aspx` | `/admission/sat-admission` | 200 |  |

## 3. تدقيق كل صفحة هدف (العناصر 1–38)
| ID | الصفحة | HTTP | أسطر نصية قُرئت | الحكم | ملاحظات (F-xx) | ما تحقق وما وُجد |
|---|---|---|---|---|---|---|
| T01 | `/default` | 200 | — | N/A | — | الصفحة الرئيسية للجامعة (chrome) — HTTP 200 فقط؛ لم تُدقَّق محتوىً (خارج /admission). |
| T02 | `/admission/admission-registration` | 200 | 40 | PASS مع تحفظات | F-18,F-19 | قائمة روابط "Study at PMU" (Registration/Grading/GPA Calculator…) — تقع خارج نطاق القبول؛ فحصت الصفحة كعنصر وصلة فقط. رابط GPA Calculator = 404 (ملاصق F-30). |
| T03 | `/admission/future_students_ro` | 200 | 58 | PASS مع تحفظات | F-18,F-19 | نص تعريفي: ادعاءات "Texas International Education Consortium (TIEC), … 32 universities" و"around 70 multinational academic and industrial experts" بلا مصدر/تاريخ (غير موثقة). لا قواعد قبول. |
| T04 | `/admission/degrees_programs_fs_ro` | 200 | 160 | FAIL | F-25,F-35,F-11 | 10 جداول مُصيَّرة عبر JavaScript (31 برنامجاً)؛ يخلو من الطب وEMGMS؛ يضم Chemical Eng/AI/Cybersecurity/IT/Graphic Design التي لا ذكر لقاعدتها في صفحة CS/Eng. |
| T05 | `/admission/admission_calendar_fs_ro` | 200 | 98 | FAIL | F-04,F-31,F-22,F-24,F-49 | تقويم الخريف 2026/27 للبكالوريوس والدراسات العليا. ✔ أيام الأسبوع صحيحة (9 يوليو خميس). ✖ تعارضات F-04/F-31. تقويم الدراسات العليا: التسلسل (التقديم 07-16 → المستندات 07-19 → المقابلات 07-23 → النتائج 08-02) منطقي ✔. |
| T06 | `/staff_profile/staff_list` | 200 | — | PASS مع تحفظات | F-45 | دليل الموظفين (HTTP 200، 1170 حرفاً)؛ يحوي بيانات أشخاص لم تُحفظ. |
| T07 | `/admission/admissions_queries` | 200 | 12 | PASS مع تحفظات | F-45,F-14 | نموذج استفسار ثنائي اللغة: Name/Email/Mobile/Query/Preferred way/Verification Code؛ لا إشعار خصوصية ظاهر؛ أخطاء "Verifaction" و"الإللكتروني". |
| T08 | `/apply` | 200 | 1 | FAIL | F-23,F-22,F-24 | تحويل فوري إلى admissions.pmu.edu.sa/welcome (Student Login / New Student? Register! / Admission Calendar: No events). لم يُنقر أي زر. |
| T09 | `/admission/international_students` | 200 | 196 | FAIL | F-01,F-02,F-48,F-46,F-10 | أطول صفحة قواعد (8.7 ألف حرف): Freshman/Transfer/Visitor/Graduate/Housing… ✔ GPA 2.0 وآخر مقرر ≤5 سنوات متسقان مع المحلي. ✖ F-01/F-02/F-48/F-46. |
| T10 | `/admission/admission_graduate_degree_programs` | 200 | 46 | PASS مع تحفظات | F-37,F-11 | قائمة 10 برامج × (Application Form / Admissions Requirements)؛ لا EMGMS؛ 5 روابط بنص "Application Form" مكرر. |
| T11 | `/admission/application_form_deme_gdp` | 200 | 30 | PASS مع تحفظات | F-39,F-14 | PhD-ME: GPA 3.00 (بكالوريوس+ماجستير) ✔ IELTS 6.0/5.5, TOEFL 83/19 ✔. عنوان "ADMISSSIONS". لا رسم/وثائق. |
| T12 | `/admission/admissions_requirements_phdba_gdp` | 200 | 31 | FAIL | F-47,F-39 | GPA: "3.00 … or … 3.20" مبهم؛ ادعاء AACSB top 6% غير موثق؛ IELTS/TOEFL ✔. |
| T13 | `/admission/admissions_requirements_emba_gdp` | 200 | 31 | PASS مع تحفظات | F-39 | EMBA 33 ساعة ✔ GPA 2.50 ✔ خبرة 3–5 سنوات ✔ IELTS/TOEFL ✔ (الحساب 33×1,818.18=60,000 ✔ في صفحة الرسوم). |
| T14 | `/admission/admissions_requirements_mba_gdp` | 200 | 26 | PASS مع تحفظات | F-39 | MBA 36 ساعة ✔ GPA 2.50 ✔ IELTS/TOEFL ✔؛ بلا وثائق داعمة. |
| T15 | `/admission/admissions_requirements_msehd_gdp` | 200 | 30 | PASS مع تحفظات | F-39,F-11 | MSHD: عنوان "Work Experience" يتبعه Personal Data Sheet (بلا شرط خبرة)؛ GPA 2.50 ✔ IELTS/TOEFL ✔. |
| T16 | `/admission/admissions_requirements_msme_gdp` | 200 | 30 | PASS مع تحفظات | F-39,F-14 | MSME: 30 ساعة ✔ GPA 2.50 ✔ IELTS/TOEFL ✔؛ "Admisssions". |
| T17 | `/admission/application_form_msee_gdp` | 200 | 31 | PASS مع تحفظات | F-39,F-14 | MSEE: GPA 2.50 ✔ IELTS/TOEFL ✔؛ "ADMISSSIONS"؛ حاشية * بلا نجمة مقابلة. |
| T18 | `/admission/application_form_msce_gdp` | 200 | 31 | PASS مع تحفظات | F-39,F-14 | MSCE: GPA 2.50 ✔ IELTS/TOEFL ✔؛ "ADMISSSIONS". |
| T19 | `/admission/application_form_msid_gdp` | 200 | 30 | PASS مع تحفظات | F-39,F-14 | MSID: GPA 2.50 ✔ IELTS/TOEFL ✔؛ "ADMISSSIONS"؛ حاشية * بلا نجمة مقابلة. |
| T20 | `/admission/admissions_requirements_emgms_gdp` | 200 | 34 | FAIL | F-16,F-39,F-11 | نص University of Arizona CESL؛ لا مقابلة ولا TOEFL iBT 83؛ GPA 3.00. |
| T21 | `/admission/admissions_requirements_milbl_gdp` | 200 | 30 | FAIL | F-29,F-43,F-39,F-14 | IELTS 6.5/5.5 ؛ "A minimum (Very Good)" بلا رقم؛ أوزان 50/30/20 ✔ مجموعها 100. |
| T22 | `/admission/post_graduate_fees_tf_ro` | 200 | 99 | PASS مع تحفظات | F-32,F-11 | جدول الرسوم الدراسية للدراسات العليا: ✔ حسابات الساعة×الرصيد صحيحة (EMBA 33×1,818.18=60,000؛ MBA 36×1,805.55≈65,000؛ MIBL 36×2,222.22=80,000). ✖ F-32. |
| T23 | `/admission/admission_contact_gdp` | 200 | 51 | PASS مع تحفظات | F-45 | "Office: G-017 Admin Bld; Email: graduateadm@pmu.edu.sa" فقط. |
| T24 | `/admission/undergraduate_programs_admission` | 200 | 31 | PASS مع تحفظات | F-07,F-10,F-18 | 80% / Qudrat 60 / 60-40 ✔ متسقة مع 3 صفحات. "Day students may register up to 20 credits" بينما الرسوم تغطي 12–18 وما فوق يُحتسب إضافياً (غير مذكور). |
| T25 | `/admission/college_of_medicine_admission` | 200 | 156 | FAIL | F-03,F-06,F-40,F-14 | الطب 7 سنوات: 60% مجموع موزون + 40% مقابلة؛ مكونات 95/80/80؛ رسم 1000؛ لا شرط لغة؛ صياغة "typically involves". |
| T26 | `/admission/admission-to-the-preparatory-program` | 200 | 94 | PASS مع تحفظات | F-07,F-14 | ✔ 80/60-40؛ جدول PRPL ✔؛ رسم 950 شامل ✔. |
| T27 | `/admission/direct-admissions-from-secondary-school` | 200 | 76 | PASS مع تحفظات | F-10,F-41 | ✔ IELTS 6.0/5.5؛ "equivalent TOEFL iBT (Learn more)" بلا أرقام؛ رسم 950 ✔. |
| T28 | `/admission/admission-from-other-universities` | 200 | 80 | FAIL | F-02,F-10 | ✔ GPA 2.0؛ رسم 950 شامل ✔ (يعارض 500 في الدوليين). |
| T29 | `/admission/visiting-student-admission` | 200 | 78 | FAIL | F-02 | ✔ شرط اللغة مشروط بلغة التدريس؛ رسم 950 (يعارض 500). |
| T30 | `/admission/admission-from-the-prep-to-ug-programs` | 200 | 121 | FAIL | F-42 | مصفوفة PRPM/PRPL وحواشٍ متناقضة. |
| T31 | `/admission/admissions_requirements_cs_eng_majors` | 200 | 95 | FAIL | F-01,F-07,F-35,F-14 | 85/65/65 وأوزان 40/30/30 ✔ حسابياً مجموعها 100؛ 0.4×85+0.3×65+0.3×65=73 دون حد كلي منشور. |
| T32 | `/admission/fees_tf_ro` | 200 | 27 | PASS مع تحفظات | F-36 | صفحة فهرس رسوم دون أي مبلغ (المبالغ في صفحات فرعية خارج النطاق). |
| T33 | `/admission/overview-undergraduate-placement-tests` | 200 | 50 | PASS مع تحفظات | F-44 | فقرة تعريفية قصيرة. |
| T34 | `/admission/aptis-placement-test` | 200 | 73 | PASS مع تحفظات | F-13,F-44,F-21 | جلسة 4 ساعات ✔ متسقة مع next-steps؛ مستويات بلا حدود درجات؛ 6 روابط British Council كنص. |
| T35 | `/admission/ielts-admission` | 200 | 73 | PASS مع تحفظات | F-08,F-41 | ✔ الجدول 6.0/5.5 → 4.0/3.5 متدرج؛ صلاحية سنتان ✔ متسقة مع TOEFL. |
| T36 | `/admission/toefl-admission` | 200 | 76 | PASS مع تحفظات | F-08,F-41 | ✔ 83/19 → 42/11؛ "online or home edition is not accepted"؛ DI code 6993 (غير مُتحقَّق منه مع ETS). |
| T37 | `/admission/sat-admission` | 200 | 66 | PASS مع تحفظات | F-35,F-14 | "SAT … minimum score of 1200 instead of Qudrat and Tahseely"؛ جدول إعفاء الرياضيات 400–499/500+؛ "wave". |
| T38 | `admissions.pmu.edu.sa/welcome` | 200 | — | FAIL | F-22,F-23 | Student Login / New Student? Register! / "Admission Calendar — No events are currently published."؛ لا متطلبات؛ تذييل "2022 ©" |

## 4. سجل الملاحظات داخل النطاق الصارم (39)
> `IN` = الدليل كله في الصفحة الرئيسية أو أهدافها المباشرة · `IN*` = الادعاء داخل النطاق ويدعمه دليل من صفحة ملاصقة.

| ID | الخطورة | النطاق | الصفحة | الملاحظة | الدليل الحرفي | الإجراء/صاحب القرار |
|---|---|---|---|---|---|---|
| **F-01** | High | IN | international_students ↔ admissions_requirements_cs_eng_majors | معيار CS/Eng للدوليين يعتمد SAT II الموقوف | Intl: "Computer Science & Engineering Majors: Secondary School 40% / SAT I 30% / SAT II 30%" vs local "HS GPA ≥85 40% / Qudrat ≥65 30% / Tahseely ≥65 30%"; College Board ended Subject Tests (Jan 2021) | قرار الكليات/القبول بمعيار بديل |
| **F-02** | High | IN | international_students ↔ admission-from-other-universities, visiting-student-admission | رسم التحويل/الزائر 500 بلا ضريبة مقابل 950 شامل | Intl: "SAR 500 (excl. VAT)"; local: "SAR 950 (incl. VAT)" | قرار المالية |
| **F-03** | High | IN* | college_of_medicine_admission (+ medical_program_studies_fees_tf_ro) | رسم الطب: 1000 "شامل" مقابل 1,150 شامل | Medicine: "SAR 1000 (incl. VAT)"; fees page: "Medical Application Fee SAR 1,150 (VAT inclusive)"; 1000×1.15=1150 | قرار المالية |
| **F-04** | High | IN | admission_calendar_fs_ro | النتائج تُعلن قبل إغلاق مواعيد التسليم والتقويم منتهٍ | "From July 19 to July 21, 2026" vs "Last day to submit IELTS or TOEFL iBT 2026-07-20"; all dates ≤ 2026-08-30; today 2026-10-10 | تقويم بفصول وتواريخ نفاذ |
| **F-50** | High | IN* | admission_calendar_fs_ro ↔ email 19ef49d2f90660a6 | إجراءات دورة 2026 الفعلية (ترشيح مسبق + نافذة 4 ساعات + مقابلات) غير منشورة | Email (Enrolment, 23 Jun 2026): "you have been shortlisted to apply … submit your application tomorrow, June 24, 2026, from 8:00 am to 12:00 pm (4 hours only)"; "interview … week of 28 June 2026"; site calendar shows only "Last day for Freshman … Apply Online 2026-06-24" and "Apply online through Qabool platform" | نشر الخطوات والنوافذ الحقيقية |
| **F-16** | High | IN | admissions_requirements_emgms_gdp | نص جامعة أخرى (University of Arizona CESL) في صفحة EMGMS | "Graduate English Language Endorsement from UA Center for English as Second Language (CESL)"; "IELTS – minimum composite score of 7, with no subject area below a 6"; "TOEFL – minimum of 79 iBT" | قرار الدراسات العليا/الهندسة |
| **F-06** | Medium | IN | college_of_medicine_admission | الحد الأدنى للمكونات لا يبلغ الحد الكلي | "(95%)","(80)","(80)" with "20% high school + 40% Qudrat + 40% Tahseely … 86 is the minimum": 0.2×95+0.4×80+0.4×80=83 | توضيح كلية الطب |
| **F-07** | Medium | IN | undergraduate_programs_admission, admissions_requirements_cs_eng_majors | الحد الكلي للمفاضلة غير منشور | "the minimum weighted total, defined by the Admissions Office, should be met" | قرار بنشره |
| **F-08** | Medium | IN | toefl-admission, ielts-admission | TOEFL منشور بمقياس 0–120 فقط | Core 83/19; ETS moved to 1–6 scale on 21 Jan 2026 (secondary source) | جدول تكافؤ معتمد |
| **F-10** | Medium | IN | direct-admissions…, admission-from-other-universities, cs_eng vs graduate pages | درجة TOEFL المكافئة غير معرّفة في صفحات البكالوريوس | "or equivalent TOEFL iBT (Learn more)" / "with acceptable scores" vs graduate "83 overall and 19 in each skill" | رابط/جدول موحد |
| **F-11** | Medium | IN | admission (menu) ↔ admission_graduate_degree_programs ↔ degrees_programs_fs_ro | قوائم برامج الدراسات العليا غير متطابقة وتسميات MSHD/MSEHD | Menu lists EMGMS & MIBL; graduate home omits EMGMS; Degrees list omits EMGMS; labels "MSHD"/"MSEHD"/"Master of Human Development" | كتالوج برامج واحد |
| **F-13** | Medium | IN* | aptis-placement-test (+ student_fees_tf_ro) | رسم Aptis غير مذكور في صفحة القرار | Aptis page: "they will be scheduled to take Aptis test"; fees page: "APTIS Exam Fees SAR 575" | توضيح القبول |
| **F-18** | Medium | IN | all 39 scope items | html[lang] فارغ | document.documentElement.lang === "" on every www.pmu.edu.sa page probed (WCAG 3.1.1) | إضافة lang |
| **F-19** | Medium | IN | all (main page: 4 of 6 images) | صور بلا alt | main page images logo-name.png ×2, logo-PMU-1.png, logo_new_r.png have no alt attribute (WCAG 1.1.1) | إضافة alt |
| **F-22** | Medium | IN | apply → admissions.pmu.edu.sa/welcome ↔ admission_calendar_fs_ro | تقويمان متعارضان: البوابة "No events" | Portal: "No events are currently published. Please check back later."; site publishes dates; footer "2022 ©" | تقويم واحد |
| **F-23** | Medium | IN | apply | نص /apply الثنائي اللغة غير مرئي للمستخدم (تحويل فوري) | Static HTML of /apply has AR/EN IELTS/TOEFL text; browser lands on admissions.pmu.edu.sa/welcome with no requirements | نشر المتطلبات في مسار مرئي |
| **F-25** | Medium | IN | degrees_programs_fs_ro ↔ college_of_medicine_admission, emgms | قائمة البرامج لا تضم الطب ولا EMGMS | Rendered Degrees & Programs (10 tables) lacks Medicine & EMGMS; both have admission pages | تحديث الكتالوج |
| **F-29** | Medium | IN | admissions_requirements_milbl_gdp vs 21 graduate pages | IELTS 6.5 في MIBL مقابل 6.0 | MIBL: "6.5 overall and 5.5 in each skill" vs others "6.0 overall and 5.5 in each skill" | تأكيد المالك |
| **F-31** | Medium | IN* | admission_calendar_fs_ro (+ academic_calendar_2026_2027_ro) | "Orientation … TBA" وغياب نافذة الربيع | "Orientation for new applicants TBA" vs academic calendar "Orientation for the new students August 27, 2026"/"January 14, 2027" | تقويم قبول موحد |
| **F-32** | Medium | IN* | post_graduate_fees_tf_ro ↔ degrees_programs_fs_ro | برامج مسعّرة بلا صفحة قبول/كتالوج | Fees list "Master of Engineering in Innovation, Sustainability, and Entrepreneurship (33)" and "PRE-Master for Master of Education"; no admission page or Degrees row | كتالوج واحد |
| **F-36** | Medium | IN | admission (main page) | محتوى الصفحة الرئيسية قوائم روابط فقط | Body = H1 "Admissions Office" + 4 H2 link lists; no intro, no intake status, no dates, no fees, no CTA hierarchy | إعادة تصميم المعلومات |
| **F-39** | Medium | IN | 11 graduate menu targets | صفحات الهبوط للدراسات العليا بلا رسم التقديم ولا قائمة الوثائق | 0 of 11 target pages contains "application fee" or "How to Apply"; these are on separate "Application Form" pages not linked from the main page | ربط/دمج |
| **F-40** | Medium | IN | college_of_medicine_admission | صياغة غير معيارية ولا شرط لغة في صفحة الطب | "the process typically involves understanding the weighting and criteria that the medical college uses…"; no IELTS/TOEFL/English requirement on page | نص معتمد |
| **F-41** | Medium | IN | direct-admissions…, graduate pages, toefl-admission, ielts-admission | "IELTS 6.0 أو TOEFL 83" ليسا متكافئين | PMU: "6.0 overall … or equivalent TOEFL iBT 83"; ETS: 6.0≈60–78 (67 newer table), 6.5≈79–93 (81) | مراجعة جدول التكافؤ |
| **F-42** | Medium | IN | admission-from-the-prep-to-ug-programs ↔ preparatory-program-study-plan | مصفوفة رياضيات الإعداد: حواشٍ متناقضة بين صفحتين | "** Department of Architecture is excluded from PRPM 0012" yet Architecture row = PRPM 0012 "Yes"; IT footnote attached to Engineering/Architecture rows; study-plan page has different rows/footnotes | مصفوفة واحدة |
| **F-43** | Medium | IN | admissions_requirements_milbl_gdp | MIBL: GPA بلا رقم و"written test" غير معرّف | "A minimum (Very Good) in Bachelor’s Degree"; "30% for the written test" | استكمال النص |
| **F-45** | Medium | IN | admissions_queries, admission_contact_gdp | قنوات الاتصال: نموذج بلا إشعار خصوصية ظاهر وبلا هاتف | Query form collects Name/Email/Mobile with no privacy text on page; graduate contact = "Office: G-017 Admin Bld; Email" only; undergrad "Contact Us" → staff directory | إشعار PDPL وقناة هاتف |
| **F-47** | Medium | IN | admissions_requirements_phdba_gdp | قاعدة GPA مبهمة وادعاء اعتماد AACSB غير موثق | "minimum cumulative GPA of 3.00 … or … 3.20"; "internationally accredited by AACSB as top 6%" (sources confirm membership, not full accreditation) | دليل رسمي/توضيح |
| **F-48** | High | IN* | international_students ↔ admission_calendar_fs_ro (+ email 19f1347de) | مسار تقديم غير السعوديين متعارض: منصتان إلزاميتان وموعد 30 يونيو (بريد) مقابل "Closed" و24 يونيو (موقع) | Site calendar: non-Saudi "Apply online through Study in Saudi platform … Closed"; Intl page: "application process can be completed entirely online". Email (Intl Office, 29 Jun 2026): "application deadline is 30th June at 4pm … you must also submit application through the study in Saudi portal … opens on 1st of July 2026 … To be eligible for admission, you must apply through both platforms." | نشر المسارين والمواعيد في صفحة الدوليين والتقويم |
| **F-14** | Low | IN | multiple | أخطاء إملائية/صياغة | "Visting Students","wave one or more","Verifaction Code","College of Medical","ADMISSSIONS"×4,"Admisssions"×2 | تدقيق لغوي |
| **F-20** | Low | IN | all | لا meta description ولا canonical؛ مضيفان وصيغ URL متعددة | Main page served at pmu.edu.sa without redirect to www; links use "../Admission/X.aspx" (legacy case/extension) | canonical وتوحيد الروابط |
| **F-24** | Low | IN* | admission_calendar_fs_ro | زر Apply Now بصيغة javascript:__doPostBack | href="javascript:WebForm_DoPostBackWithOptions(… Apply_Now_ADS …)"; 7 URL forms reach the same portal | رابط عادي |
| **F-26** | Low | IN | undergraduate_programs_admission, international_students, calendar | ترتيب العناوين مختل | H2 before H1; H1→H3→H4 then H3; H2→H4 | تصحيح الترتيب |
| **F-35** | Low | IN | sat-admission ↔ admissions_requirements_cs_eng_majors | قائمة التخصصات الخاصة مختلفة | SAT page lists "Artificial Intelligence … etc."; CS/Eng page omits AI & Cybersecurity | قائمة واحدة |
| **F-37** | Low | IN | admission; admission_graduate_degree_programs | تسميات روابط غامضة ومكررة | "Home"×3 (3 different targets); "Tuition & Fees"×2 (different targets); "Application Form"/"Admissions Requirements"×5 identical | تسميات فريدة |
| **F-38** | Low | IN | admission (main page) | إمكانية وصول هيكلية | No <main> landmark (HEADER,NAV,HEADER,NAV,FOOTER,FOOTER); empty anchor href="#sidebar"; iframe search/new-search.html has no title; logo-PMU-1.png 301 (case) | معالجة هيكلية |
| **F-44** | Low | IN | aptis-placement-test | حدود درجات Aptis غير منشورة وتعبير "Core Program" | Levels listed (Pre Beginner…Advanced) without score bands; "direct entry into the Core Program" | نشر الحدود |
| **F-46** | Low | IN | international_students | قسم Transportation فارغ و"Acceptable SAT I" بلا حد | "Transportation" heading with no text; "Acceptable SAT I" (no threshold) vs 1200/1300 elsewhere | استكمال |
| **F-49** | Low | IN | admission_calendar_fs_ro | كتل التقويم مكررة في DOM مرتين | Rendered text repeats Undergraduate and Graduate calendar blocks twice | إزالة التكرار |

## 5. ملاحظات ملاصقة للنطاق (10) — خارج النطاق الصارم، محفوظة للإحاطة فقط
| ID | الخطورة | الصفحة | الملاحظة | الدليل |
|---|---|---|---|---|
| F-17 | High | freshman_admission (orphan) | أوزان وإعفاءات قديمة | "High school 30% / Aptitude Test 50% / Personal Interview 20%"; "TOEFL … 513 (CBT 183, iBT 65)" |
| F-27 | High | payment_schedule_tf_ro_fall; faq_tf_ro | جدول الأقساط والأسئلة الشائعة على رسوم 2025/26 | 10,000+10,000+9,000=29,000 vs 2026/27 "SAR 30,000 / semester" |
| F-05 | Medium | transfer-student-admission (orphan) | IELTS 5.0 لكل مهارة (صفحة يتيمة) | "minimum score of 5.0 on each test component" |
| F-09 | Medium | ielts_course (orphan) | صفحة دورة 2019 متاحة | "From July 14, 2019 to August 02, 2019" |
| F-21 | Medium | next-steps | تمرير أفقي 440>390 | scrollWidth 440 vs 390 |
| F-28 | Medium | payment_method_tf_ro | تناقض سياسة الاسترداد | "All tuition payments are non-refundable." + 25%/50%/75% deductions |
| F-30 | Medium | sidebar targets (scholarships, GPA calculator) | 4 روابط 404 وصفحة مساعدات فارغة | 404 - File or directory not found |
| F-15 | Low | news/2010; news?ID=1115 | أخبار قديمة | "العام الجامعي 1436/1435هـ" |
| F-33 | Low | 13 academic calendars; PDFs | تراكم أجيال وثائق | calendars 2014/15→2026/27; Aptis guide PDF created 2017 |
| F-34 | Low | registration_office | رابط لمضيف داخلي | http://web1:8066/Online_Room_Reservation_Form.aspx |

**سُحبت/صُحِّحت:** F-12 (قائمة البرامج: خلل استخراج) · "3 روابط معطلة" (تأخر عابر) · "عناوين MIBL فارغة" (خلل استخراج ثابت) · "تكافؤ اللغتين في /apply" (انظر F-23) · ملاحظة F-03 صُحِّحت من "غياب الرسم" إلى "تضارب القيمة 1000 مقابل 1,150".

## 6. حساب التغطية (Coverage Mathematics) — النطاق الصارم
| المقياس | البسط / المقام | النسبة |
|---|---|---|
| عناصر النطاق المكتشفة | 39 (الصفحة + 37 هدفاً + وجهة التقديم) | — |
| عناصر جُلبت وحُفظت كأدلة (HTTP + نص مُصيَّر) | 39 / 39 | **100%** |
| عناصر دُققت سطراً بسطر بقراءة المدقق | 37 / 39 (استُثنيت الصفحة الرئيسية للموقع `/default` ودليل الموظفين لأنهما خارج `/admission`) | **94.9%** |
| روابط منطقة المحتوى بحالة HTTP مثبتة | 38 / 38 | 100% (0 أعطال؛ 100% تعمل) |
| روابط الترويسة/التذييل (93) | خارج النطاق؛ ضمن فحص الـ84 رابطاً | — |
| اختبارات متصفح منفَّذة | موبايل 390px فقط | سطح المكتب/لوحة المفاتيح/قارئ الشاشة/الأداء = **NOT TESTED** |
| Verified Closure Rate · Test Pass Rate · Evidence Completeness | لا معالجات منفَّذة | **غير قابلة للحساب** |
> المقام هو ما اكتُشف عبر الروابط فقط. "عدم إيجاد مشكلة" لا يُثبت عدم وجودها.

## 7. بوابات الإغلاق (G0–G11) للنطاق الصارم
| البوابة | الحالة |
|---|---|
| G0 السلطة والنطاق | **PASS** — نطاق معرَّف، قراءة فقط، لا صلاحية نشر |
| G1 التغطية والأدلة | **PASS مشروط** — 39/39 مجلوب، 37/39 مقروء سطرياً؛ النصوص والـJSON والجرد في `evidence/` |
| G2 السياسات والقرارات | **FAIL** — F-01..F-04، F-16، F-29، F-41 وغيرها مفتوحة |
| G3 المعالجة الحرجة | **NOT STARTED** (لا صلاحية، تنتظر قرارات) |
| G4 الجودة وUAT | **PARTIAL** — موبايل منفَّذ؛ UAT/سطح مكتب/وصول يدوي غير منفَّذ |
| G5 تغييرات الإنتاج | **N/A** — لم تُنفَّذ تغييرات |
| G6 الأمن والخصوصية والامتثال | **NOT TESTED** — لوحظ غياب إشعار خصوصية في نموذج الاستفسار (F-45) |
| G7 الاستمرارية والتراجع | **NOT TESTED** — نقطة فشل مفردة: كل مسارات Apply → بوابة واحدة |
| G8 الحوكمة والتسليم | **NOT STARTED** |
| G9 المحفظة الاستراتيجية | **DELIVERED (مسودة)** في التقرير الرئيسي §9 |
| G10 تدقيق الإغلاق المستقل | **NOT MET** |
| G11 الاعتماد المؤسسي | **NOT OBTAINED** |

## 8. القرارات المطلوبة (مختصرة، حسب الجهة)
| القرار | الجهة | يحسم |
|---|---|---|
| معيار CS/Eng للدوليين بعد توقف SAT II | الكليات + القبول | F-01 |
| رسم التحويل/الزائر للدوليين (500 بلا ضريبة أم 950 شامل) | المالية | F-02 |
| رسم الطب: 1,000 أم 1,150 وتسمية الضريبة | المالية + كلية الطب | F-03 |
| تقويم قبول موحد بفصول (الخريف/الربيع) وتواريخ نفاذ ومصدر وحيد (موقع/بوابة) | القبول + التسجيل | F-04, F-22, F-31 |
| شروط لغة EMGMS الفعلية واستبدال نص جامعة أريزونا | الهندسة + الدراسات العليا | F-16 |
| IELTS في MIBL (6.5) وجدول تكافؤ TOEFL/IELTS | القانون + القبول | F-29, F-41, F-08 |
| الحد الكلي للمفاضلة (نشر أم لا) وحدود Aptis | القبول | F-07, F-44 |
| إلحاق رسم التقديم وقائمة الوثائق بصفحات هبوط الدراسات العليا | القبول + الويب | F-39 |
| الكتالوج الموحد للبرامج (Medicine/EMGMS/MEISE/Pre-Master) | التسجيل + الكليات | F-11, F-25, F-32 |
| إشعار الخصوصية وقناة الهاتف | الشؤون القانونية + القبول | F-45 |

## 9. القرار الختامي
# **NOT READY FOR CLOSURE**
- 39 ملاحظة مثبتة داخل النطاق الصارم (**7 High · 22 Medium · 10 Low**) + 7 مستمدة من البريد + 10 ملاصقة، منها قرارات مالية وأكاديمية مفتوحة.
- لا معالجة نُفِّذت (لا صلاحية نشر) → لا يمكن إعلان أي إغلاق تقني.
- بنود **INSUFFICIENT ACCESS OR EVIDENCE:** سطح المكتب، لوحة المفاتيح، قارئ الشاشة، الأداء، مسار التسجيل/الدفع داخل البوابة، PDF (28 ملفاً خارج النطاق الصارم).
- لا نسبة إنجاز أو نجاح تُعلن غير الواردة أعلاه.

---
**تحديث (ربط البريد):** انظر `EMAIL_CONTEXT_LINKAGE.md` — رُفعت F-48 إلى High، وأُضيفت F-50 (IN*) وسبع ملاحظات مستمدة من البريد (F-51..F-57).
