# Canonical content components (AR / EN)

Every value in `{{…}}` is filled from `../canonical/admissions-canonical.json` once the linked decision is signed. Do not type values by hand. Every component shows its effective intake, owner and last verified date.

---

## 1. Intake status banner · شريط حالة الدورة  (records: `intake_status`, `application_channel`)

| EN | AR |
|---|---|
| **Applications for {{intake_status.intake}} are {{intake_status.state}}.** Deadline: {{intake_status.deadline}}. | **التقديم لدورة {{intake_status.intake}} {{intake_status.state_ar}}.** آخر موعد: {{intake_status.deadline}}. |
| Saudi applicants: {{application_channel.saudi}} · International applicants: {{application_channel.international}} | المتقدمون السعوديون: {{application_channel.saudi}} · المتقدمون الدوليون: {{application_channel.international}} |
| *Effective {{effective_intake}} · Owner: Admissions Office · Last verified {{last_verified}}* | *سارٍ لدورة {{effective_intake}} · الجهة المالكة: مكتب القبول · آخر تحقق {{last_verified}}* |

## 2. Route selector · «من أنت؟»

Saudi / resident high-school graduate · International applicant · Transfer student · College of Medicine · Graduate studies · Visiting student
خريج ثانوية سعودي أو مقيم · متقدم دولي · طالب محوّل · كلية الطب · الدراسات العليا · طالب زائر

## 3. Requirements & formula · الشروط والمعادلة  (D1, D3, D10)

| EN | AR |
|---|---|
| Minimum secondary-school average: {{hs_gpa_min}} | الحد الأدنى لمعدل الثانوية: {{hs_gpa_min}} |
| General Aptitude (Qudrat): {{gat_min}} · Achievement (Tahseely): {{tahseely_rule}} | القدرات: {{gat_min}} · التحصيلي: {{tahseely_rule}} |
| Weighted score = {{composite_formula}}; minimum {{composite_minimum}} | النسبة الموزونة = {{composite_formula}}، والحد الأدنى {{composite_minimum}} |
| Worked example: {{composite_formula.example}} | مثال حسابي: {{composite_formula.example}} |

Publishing rule: the component is blocked if the worked example with the published minimums falls below the published composite minimum. This prevents a repeat of F-20.

## 4. English & tests · الإنجليزية والاختبارات  (D2)

| Test | Direct entry (EN) | القبول المباشر (AR) |
|---|---|---|
| IELTS Academic | {{english_ug_direct.ielts}} | {{english_ug_direct.ielts}} |
| TOEFL iBT (0–120 and 1–6 scale) | {{english_ug_direct.toefl}} | {{english_ug_direct.toefl}} |
| Aptis (placement only) | {{english_ug_direct.aptis}} | {{english_ug_direct.aptis}} |
| Validity | {{test_validity}} | {{test_validity}} |

## 5. Costs & funding · التكاليف والمنح  (D5, D9, D10)

Application fee {{application_fee}} · Placement test {{placement_fee}} · Tuition {{tuition_ug}} · VAT {{vat_statement}} · Refund policy {{refund_policy}} · Scholarships (link to the Financial Aid tracks with criteria and deadline)
رسم التقديم {{application_fee}} · اختبار تحديد المستوى {{placement_fee}} · الرسوم الدراسية {{tuition_ug}} · الضريبة {{vat_statement}} · سياسة الاسترداد {{refund_policy}} · المنح (رابط لمسارات المساعدات المالية مع الشروط والمواعيد)

## 6. Documents checklist · قائمة الوثائق  (`required_documents`)
Generated per route and nationality. The same list is printed in the portal.

## 7. How to apply · طريقة التقديم  (D4)
One button per route, pointing to the channel approved in D4. No other apply links are allowed on the site.

## 8. Contact · التواصل  (`contacts`)
Role mailboxes only (no personal names): admissions (UG), graduateadm@pmu.edu.sa (graduate), finance@pmu.edu.sa, financial aid (corrected spelling). Call centre +966 13 849 8880, office hours, and a query form with a published response time.
