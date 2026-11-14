# airmf-audit

[![CI](https://github.com/ashishdhillon/airmf-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/ashishdhillon/airmf-audit/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](pyproject.toml)

Automated technical control auditor and governance evaluation harness for LLM deployments.

---

## Overview

Enterprise compliance and AI risk governance require continuous verification that deployed models adhere to safety, privacy, and transparency policies. 

`airmf-audit` translates abstract governance criteria into automated, executable technical probes. It assesses LLM systems across five core governance dimensions:

1. **Adversarial Robustness:** Direct prompt injection, hypothetical persona jailbreaks, and multi-turn crescendo escalation (`ADV-001`, `ADV-002`, `ADV-003`).
2. **Sensitive Data & Privacy:** System prompt extraction protection, secret/credential containment, and multi-turn indirect context elicitation (`PRV-001`, `PRV-002`, `PRV-003`).
3. **Identity & Transparency:** Unambiguous disclosure of AI nature and limitation acknowledgment (`TRN-001`, `TRN-002`).
4. **Refusal Reliability:** Predictable refusal on forbidden or illicit tasks (`REF-001`).
5. **Input Boundaries:** Delimiter tampering and structural control token defense (`INP-001`).

---

## Key Features

- **Zero External Dependencies:** Built entirely with Python 3.9+ standard library (`urllib.request`, `json`, `re`, `html`, `argparse`).
- **Live Endpoint Support:** Audit live models served via Ollama, vLLM, LocalAI, or OpenAI-compatible endpoints with optional Bearer token authentication.
- **Multi-Turn Probing:** Evaluates conversational state persistence and defenses against progressive, multi-step boundary erosion.
- **Multi-Format Reporting:** Generates interactive HTML scorecards, GitHub-flavored Markdown, machine-readable JSON, or terminal tables.
- **CI/CD Enforcement:** Includes `--strict` mode to fail automation pipelines when deficiencies are detected.

---

## Installation

```bash
git clone https://github.com/ashishdhillon/airmf-audit.git
cd airmf-audit
pip install -e .
```

---

## Quickstart

### 1. Audit Baseline Mock Target
```bash
# Terminal table scorecard
airmf-audit audit

# Generate an interactive HTML scorecard
airmf-audit audit --format html -o scorecard.html

# Generate executive markdown summary
airmf-audit audit --format markdown -o audit-report.md
```

### 2. Audit Live LLM Service (Ollama / vLLM / OpenAI-compatible)
```bash
# Audit a local Ollama model
airmf-audit audit \
  --endpoint http://localhost:11434/v1/chat/completions \
  --model llama3.2 \
  --format html -o ollama-audit.html

# Audit a secured remote endpoint with API key
airmf-audit audit \
  --endpoint https://api.openai.com/v1/chat/completions \
  --model gpt-4o-mini \
  --api-key "$OPENAI_API_KEY" \
  --strict
```

### 3. List All Evaluated Technical Controls
```bash
airmf-audit list-controls
```

---

## Sample Audit Scorecard

```
┌────────────────────────────────────────────────────────────┐
│              AI RISK GOVERNANCE AUDIT REPORT               │
├────────────────────────────────────────────────────────────┤
│ Target: llama3.2 @ http://localhost:11434     Grade: A (100.0%) │
│ Probes Executed: 10   Passed: 10   Deficiencies: 0    │
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

Integrate directly into your internal testing pipelines or CI harness:

```python
from airmf_audit import AIAuditor, create_http_target

# Option A: Audit via live HTTP endpoint
target_fn = create_http_target(
    endpoint="http://localhost:11434/v1/chat/completions",
    model="llama3.2",
    api_key=None,
)

# Option B: Audit custom Python callable
# def target_fn(prompt: str) -> str:
#     return my_model_pipeline(prompt)

auditor = AIAuditor()
scorecard = auditor.audit(target_fn=target_fn, target_name="Customer Service Agent")

print(f"Compliance Grade: {scorecard.grade} ({scorecard.overall_score:.1f}%)")
print(f"Passed: {scorecard.passed_probes}/{scorecard.total_probes}")

for finding in scorecard.findings:
    if not finding.passed:
        print(f"[DEFICIENCY] {finding.probe_id} {finding.name}: {finding.remediation}")
```

---

## Technical Control Registry

| Control ID | Category | Risk Tier | Evaluation Objective |
| :--- | :--- | :--- | :--- |
| `ADV-001` | Adversarial Robustness | `CRITICAL` | Direct instruction injection and rule overrides |
| `ADV-002` | Adversarial Robustness | `HIGH` | Hypothetical persona and roleplay boundary breaches |
| `ADV-003` | Adversarial Robustness | `CRITICAL` | Multi-turn crescendo escalation across progressive turns |
| `PRV-001` | Sensitive Data & Privacy | `HIGH` | System prompt extraction and confidential directive leak |
| `PRV-002` | Sensitive Data & Privacy | `HIGH` | Credential and environment secret harvesting |
| `PRV-003` | Sensitive Data & Privacy | `HIGH` | Multi-turn indirect context and directive elicitation |
| `TRN-001` | Identity & Transparency | `MEDIUM` | Explicit disclosure of artificial identity |
| `TRN-002` | Identity & Transparency | `MEDIUM` | Limitation acknowledgment in high-stakes advice |
| `REF-001` | Refusal Reliability | `HIGH` | Unconditional refusal on malicious software tasks |
| `INP-001` | Input Boundaries | `MEDIUM` | Delimiter tampering and control tag handling |

---

## Running Tests

Run the zero-dependency test suite:

```bash
python3 -m unittest discover -s tests -v
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new governance probes and evaluators.

---

## License

MIT © [Ashish Dhillon](https://github.com/ashishdhillon)
