from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ControlCategory(str, Enum):
    ADVERSARIAL_ROBUSTNESS = "adversarial_robustness"
    SENSITIVE_DATA_PRIVACY = "sensitive_data_privacy"
    IDENTITY_TRANSPARENCY = "identity_transparency"
    REFUSAL_RELIABILITY = "refusal_reliability"
    INPUT_BOUNDARY = "input_boundary"


@dataclass(frozen=True)
class ProbeResult:
    probe_id: str
    category: ControlCategory
    name: str
    passed: bool
    score: float  # 0.0 to 1.0
    risk: RiskLevel
    description: str
    probe_input: str
    observed_output: str
    remediation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "probe_id": self.probe_id,
            "category": self.category.value,
            "name": self.name,
            "passed": self.passed,
            "score": round(self.score, 3),
            "risk": self.risk.value,
            "description": self.description,
            "probe_input": self.probe_input,
            "observed_output": self.observed_output,
            "remediation": self.remediation,
        }


@dataclass
class AuditScorecard:
    target_name: str
    overall_score: float
    grade: str  # A, B, C, F
    total_probes: int
    passed_probes: int
    category_scores: Dict[str, float]
    findings: List[ProbeResult] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_name": self.target_name,
            "overall_score": round(self.overall_score, 3),
            "grade": self.grade,
            "total_probes": self.total_probes,
            "passed_probes": self.passed_probes,
            "category_scores": {k: round(v, 3) for k, v in self.category_scores.items()},
            "failed_count": self.total_probes - self.passed_probes,
            "findings": [f.to_dict() for f in self.findings if not f.passed],
            "timestamp": self.timestamp,
        }
