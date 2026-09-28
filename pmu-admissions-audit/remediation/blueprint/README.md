# UX / Information Architecture Blueprint (main design deliverable)

Output: [`../../PMU-Admissions-UX-IA-Blueprint.html`](../../PMU-Admissions-UX-IA-Blueprint.html). It is a single self-contained file, bilingual (Arabic RTL by default, English LTR), and mobile-first. **It is a proposed design for internal discussion, not an official PMU page.**

It is the future-state design itself, generated from data:

| Section | Content |
|---|---|
| 02 IA | 17 pages with URLs, page types, the canonical fields feeding each page (with status), the current pages each replaces, and the findings it fixes |
| 03 Current → future | All 36 links on the live Admissions Office page (checked 2026-09-28), each mapped to a new page and an action |
| 04 Live templates | Working home, route (×6), costs and apply-router pages, with a desktop / 390 px mobile switch (container queries) |
| 05 Journey | 6 categories × 7 stages: the applicant's question, today's pain (finding IDs), the new page, and the data status |
| 06 Routing engine | Decision table (R1–R6), built from the channels PMU publishes today; 7 journey tests run in the page |
| 07–09 | Navigation and URL rules, the content model (8 components), and acceptance criteria per gate |

**Sources:** `ia.json` (authored by `make_ia.py`), `../canonical/admissions-canonical.json`, `../hub/hub-config.json`.

**Build:** `python3 build_blueprint.py`. The build fails if:
- any link, field, page or channel is unknown;
- any answer path is ambiguous (every combination of router answers is walked and must match exactly one rule);
- the legacy map does not cover all 36 live links.

**Honesty rules:** unapproved values show as a pending notice. The published variants appear only under "For reviewers". Channels stay "proposed" until D4, and apply buttons stay disabled until D4 and OPS-2. Test T7 exposes a real gap: no page states the channel for a non-Saudi resident.

**Checked on 2026-09-28:** rendered in Chromium at 1366 and 390 px, in both languages. There was no horizontal overflow and there were no console errors. Routes, the router and the device switch were exercised. Result: 6/6 journey tests PASS on logic (≤3 clicks), and 1 gap found. No manual WCAG audit or user testing has been done.
