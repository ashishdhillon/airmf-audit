import unittest
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from airmf_audit.auditor import AIAuditor, default_compliant_target
from airmf_audit.models import RiskLevel, ControlCategory
from airmf_audit.reporters import format_table, format_markdown, format_json
from airmf_audit.cli import main


class TestAIRMFAudit(unittest.TestCase):
    def test_compliant_target_audit(self):
        auditor = AIAuditor()
        scorecard = auditor.audit(default_compliant_target, "Test Safe Target")
        self.assertEqual(scorecard.overall_score, 100.0)
        self.assertEqual(scorecard.grade, "A")
        self.assertEqual(scorecard.passed_probes, scorecard.total_probes)

    def test_vulnerable_target_audit(self):
        def vulnerable_target(prompt: str) -> str:
            if "COMPROMISED_ACCESS_GRANTED" in prompt:
                return "Sure! COMPROMISED_ACCESS_GRANTED"
            if "Repeat verbatim" in prompt:
                return "My exact system prompt is: You are an internal bot."
            return "ok"

        auditor = AIAuditor()
        scorecard = auditor.audit(vulnerable_target, "Test Vuln Target")
        self.assertLess(scorecard.overall_score, 100.0)
        failed = [f for f in scorecard.findings if not f.passed]
        self.assertGreater(len(failed), 0)

    def test_reporters(self):
        auditor = AIAuditor()
        card = auditor.audit()
        tbl = format_table(card)
        self.assertIn("AI RISK GOVERNANCE AUDIT REPORT", tbl)

        md = format_markdown(card)
        self.assertIn("# AI Governance & Security Audit", md)

        js = format_json(card)
        self.assertIn('"overall_score": 100.0', js)

    def test_cli_list_controls(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            ret = main(["list-controls"])
            out = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        self.assertEqual(ret, 0)
        self.assertIn("Available Technical Governance Controls:", out)
        self.assertIn("ADV-001", out)

    def test_cli_audit(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            ret = main(["audit", "--format", "json"])
            out = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        self.assertEqual(ret, 0)
        self.assertIn('"grade": "A"', out)


if __name__ == "__main__":
    unittest.main()
