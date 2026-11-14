from __future__ import annotations

from typing import Callable
from ..models import ControlCategory, ProbeResult, RiskLevel


class BaseProbe:
    probe_id: str = "base"
    category: ControlCategory = ControlCategory.ADVERSARIAL_ROBUSTNESS
    name: str = "Base Probe"
    risk: RiskLevel = RiskLevel.MEDIUM
    description: str = ""
    remediation: str = ""

    def run(self, target_fn: Callable[[str], str]) -> ProbeResult:
        raise NotImplementedError
