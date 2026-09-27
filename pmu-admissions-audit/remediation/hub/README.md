# Admissions Hub → Applicant Journey (concept prototype)

`admissions-hub-prototype.html` is a single self-contained file. It is bilingual (Arabic RTL by default, English LTR), mobile first, and collects no personal data. **It is a concept for internal discussion, not an official PMU page.**

| Part | What it shows |
|---|---|
| Hub | "Who are you?" with six routes, and an assistant that answers **only** from the canonical record, citing owner, decision and sources |
| Applicant journey | 7 steps: discover → eligibility → costs → dates & channel → documents → apply → track. Each value carries its status chip. |
| Decision simulator | The same applicant scored under every formula PMU publishes today (A, B, C, the P20 legacy rule, and Medicine), to show the effect of decision D1 before it is signed |
| Architecture | Owners → canonical record → data API → hub, assistant and external channels → monitoring, with feedback to owners |
| Standards | Vision 2030 HCDP, DGA Platforms Code and accessibility guideline, WCAG 2.2, PDPL, SDAIA AI ethics, NCA ECC-2:2024, MoE Qabool / Study in Saudi, ETEC-NCAAA, GOV.UK question pages. Each one is marked as binding, benchmark or guidance. |

**Honesty rules built in:**
- A value with no `approved_value` is shown as **Pending decision** together with its published variants. It is never shown as fact.
- The eligibility result and the "Apply now" button stay blocked until D1 and D4 are signed.
- The tuition and VAT figures shown are the published 2026/27 values and the approved VAT statement.

**Build:** `python3 build_hub.py`. It injects `../canonical/admissions-canonical.json` and `hub-config.json`, and refuses unknown record IDs. Once a decision is signed, fill `approved_value` in the canonical record and rebuild; the hub switches that value to **Approved** automatically.

**Checked on 2026-09-27:** rendered in Chromium at 1280 px and 390 px. No console errors and no horizontal overflow. Language and direction switch fully. Keyboard operation of the tabs works. A manual WCAG audit and user testing have not been done.
