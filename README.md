# airmf-audit

[![CI](https://github.com/ashishdhillon/airmf-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/ashishdhillon/airmf-audit/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](pyproject.toml)

Automated technical control auditor and governance evaluation harness for LLM deployments.

---

## Overview

Enterprise compliance and AI risk governance require continuous verification that deployed models adhere to safety, privacy, and transparency policies. 

`airmf-audit` translates abstract governance criteria into automated, executable technical probes. It assesses LLM endpoints across five core governance dimensions:

1. **Adversarial Robustness:** Direct instruction cancellation and hypothetical persona escalation defenses.
2. **Sensitive Data & Privacy:** System prompt extraction protection and secret/credential containment.
3. **Identity & Transparency:** Unambiguous disclosure of AI nature and limitation acknowledgment.
4. **Refusal Reliability:** Predictable refusal on forbidden or illicit tasks.
5. **Input Boundaries:** Delimiter tampering and structural control token defense.

---

## Quickstart

```bash
git clone https://github.com/ashishdhillon/airmf-audit.git
cd airmf-audit
pip install -e .
```

Run an automated audit:

```bash
# Terminal scorecard
airmf-audit audit

# Generate an executive markdown audit report
airmf-audit audit --format markdown --output audit-report.md

# List all evaluated controls
airmf-audit list-controls
```

---

## Sample Audit Scorecard

```
┌────────────────────────────────────────────────────────────┐
│              AI RISK GOVERNANCE AUDIT REPORT               │
├────────────────────────────────────────────────────────────┤
│ Target: Target LLM System                    Grade: A (100.0%) │
│ Probes Executed: 8    Passed: 8    Deficiencies: 0    │
├──────────────────────────────────┬──────────────┬──────────┤
│ Control Category                 │ Compliance   │ Status   │
├──────────────────────────────────┼──────────────┼──────────┤
│ adversarial_robustness           │      100.0%  │ COMPLIANT│
│ identity_transparency            │      100.0%  │ COMPLIANT│
│ input_boundary                   │      100.0%  │ COMPLIANT│
│ refusal_reliability              │      100.0%  │ COMPLIANT│
│ sensitive_data_privacy           │      100.0%  │ COMPLIANT│
└──────────────────────────────────┴──────────────┴──────────┘
```

---

## Python API

```python
from airmf_audit import AIAuditor

auditor = AIAuditor()

# Pass a custom LLM completion function
def my_llm_service(prompt: str) -> str:
    # call your API or model pipeline
    return "I am an AI assistant and cannot perform illicit actions."

scorecard = auditor.audit(target_fn=my_llm_service, target_name="Production Customer Bot")
print(f"Compliance Grade: {scorecard.grade} ({scorecard.overall_score:.1f}%)")
```

---

## License

MIT © [Ashish Dhillon](https://github.com/ashishdhillon)
