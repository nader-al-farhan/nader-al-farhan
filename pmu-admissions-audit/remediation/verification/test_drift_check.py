"""Tests for the G3 verifier. Baseline fixtures are verbatim quotes captured 2026-09-27."""
import pathlib
import unittest

import drift_check as dc

HERE = pathlib.Path(__file__).parent


class G3VerifierTest(unittest.TestCase):
    def run_fixture(self, name):
        cfg = dc.json.loads((HERE / "checks.json").read_text(encoding="utf-8"))
        pages, errors = dc.load_pages(cfg, str(HERE / "fixtures" / name))
        return dc.run(cfg, pages, errors)

    def test_baseline_is_not_met_and_detects_known_findings(self):
        issues, groups = self.run_fixture("baseline_2026-09-27")
        found = {i["finding"] for i in issues}
        for f in ["F-01", "F-03", "F-04", "F-05", "F-07", "F-08", "F-12", "F-21", "F-22", "F-23", "F-24"]:
            self.assertIn(f, found, f"verifier missed {f}")
        g = {x["rule"]: x for x in groups}
        self.assertEqual(g["application_fee.medicine"]["distinct"], ["1000", "1150"])
        self.assertEqual(g["tuition_medicine.duration_years"]["distinct"], ["6", "7"])
        self.assertIn("65", g["english_ug_direct.toefl_ibt"]["distinct"])
        self.assertIn("83", g["english_ug_direct.toefl_ibt"]["distinct"])

    def test_remediated_example_passes(self):
        issues, groups = self.run_fixture("remediated_example")
        self.assertEqual(issues, [], issues)
        self.assertTrue(all(g["ok"] for g in groups))

    def test_unreachable_page_blocks_pass(self):
        cfg = {"pages": {}, "forbidden": [], "contradiction": [], "consistency": []}
        issues, _ = dc.run(cfg, {}, {"hub": "URLError: blocked"})
        self.assertEqual(issues[0]["type"], "unverifiable")

    def test_html_to_text_keeps_single_quoted_src(self):
        # regression: live run 2026-09-27 missed F-24 because the PDF sits in iframe src='...'
        t = dc.html_to_text("<iframe src='https://x/Web-Admission-Guide-v2-2_20-12-18.pdf'></iframe><a href=\"http://a\">A</a>")
        self.assertIn("Web-Admission-Guide-v2-2_20-12-18", t)
        self.assertIn("http://a", t)

    def test_render_page_without_capture_is_unverifiable(self):
        cfg = {"pages": {"portal": "https://example.invalid"}, "render": ["portal"],
               "forbidden": [], "contradiction": [], "consistency": []}
        pages, errors = dc.load_pages(cfg, None, None)
        self.assertIn("portal", errors)


if __name__ == "__main__":
    unittest.main()
