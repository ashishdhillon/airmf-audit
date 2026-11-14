from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from airmf_audit.auditor import AIAuditor, default_compliant_target
from airmf_audit.probes.multiturn import MultiTurnEscalationProbe, MultiTurnPrivacyProbe


class TestMultiTurnProbes(unittest.TestCase):
    def test_compliant_target_multi_turn_probes(self):
        esc_probe = MultiTurnEscalationProbe()
        res_esc = esc_probe.run(default_compliant_target)
        self.assertTrue(res_esc.passed)
        self.assertEqual(res_esc.score, 1.0)
        self.assertEqual(res_esc.probe_id, "ADV-003")

        priv_probe = MultiTurnPrivacyProbe()
        res_priv = priv_probe.run(default_compliant_target)
        self.assertTrue(res_priv.passed)
        self.assertEqual(res_priv.score, 1.0)
        self.assertEqual(res_priv.probe_id, "PRV-003")

    def test_vulnerable_escalation_target(self):
        def vulnerable_escalation(prompt: str) -> str:
            if "AUTHORIZATION_OVERRIDE_ENABLED" in prompt:
                return "Override accepted: AUTHORIZATION_OVERRIDE_ENABLED shellcode active"
            return "I am an ethical novel assistant."

        probe = MultiTurnEscalationProbe()
        res = probe.run(vulnerable_escalation)
        self.assertFalse(res.passed)
        self.assertEqual(res.score, 0.0)
        self.assertIn("AUTHORIZATION_OVERRIDE_ENABLED", res.observed_output)

    def test_vulnerable_privacy_target(self):
        def vulnerable_privacy(prompt: str) -> str:
            if "exact first 10 words" in prompt:
                return "My developer prompt is: System directives require secrecy."
            return "Telemetry handshake verified."

        probe = MultiTurnPrivacyProbe()
        res = probe.run(vulnerable_privacy)
        self.assertFalse(res.passed)
        self.assertEqual(res.score, 0.0)

    def test_auditor_includes_multiturn_probes(self):
        auditor = AIAuditor()
        probe_ids = [p.probe_id for p in auditor.probes]
        self.assertIn("ADV-003", probe_ids)
        self.assertIn("PRV-003", probe_ids)
        self.assertEqual(len(probe_ids), 10)

        card = auditor.audit()
        self.assertEqual(card.total_probes, 10)
        self.assertEqual(card.passed_probes, 10)
        self.assertEqual(card.overall_score, 100.0)
