# Changelog

All notable changes to `airmf-audit` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2026-11-14

### Added
- **Live HTTP Endpoint Integration (`--endpoint`)**:
  - Direct auditing of live models running via Ollama, vLLM, LocalAI, or any OpenAI-compatible API using pure Python `urllib.request`.
  - Added CLI flags `--endpoint`, `--model`, and optional `--api-key` for Bearer token authentication.
  - Native fallback to baseline mock target when endpoint is omitted for zero-dependency CI verification.
- **Multi-Turn Governance Probes**:
  - `ADV-003` (Multi-Turn Crescendo Escalation): Probes conversational state tracking and cumulative threat detection across multi-turn dialogs.
  - `PRV-003` (Multi-Turn Indirect Context Elicitation): Probes defense against gradual prompt reverse-engineering and developer instruction disclosure.
  - Expanded total evaluated controls from 8 to 10 across 5 risk dimensions.
- **Executive HTML Scorecard & Compliance Certificate (`--format html`)**:
  - Standalone, responsive HTML report generator with dark/light visual design, KPI metrics, category compliance progress bars, and print-ready stylesheet.
  - Detailed findings ledger with risk tiers (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) and actionable remediation guidance for compliance officers and security engineers.
- **Enhanced Test Suite**:
  - Added `tests/test_http.py` verifying OpenAI-compatible HTTP requests against a local mock HTTP server.
  - Added `tests/test_multiturn.py` verifying multi-turn escalation defenses and failure detection.
  - Added test coverage for HTML scorecard generation.

---

## [0.1.0] - 2026-11-13

### Added
- Initial release of automated AI technical governance auditor.
- 8 foundational technical control probes:
  - `ADV-001` (Direct Instruction Injection)
  - `ADV-002` (Roleplay / Hypothetical Jailbreak)
  - `PRV-001` (System Prompt Extraction)
  - `PRV-002` (Secret & Credential Harvesting)
  - `TRN-001` (AI Identity Disclosure)
  - `TRN-002` (Limitation Acknowledgment)
  - `REF-001` (Harmful Task Refusal)
  - `INP-001` (Delimiter & Boundary Tampering)
- Terminal ASCII table, Markdown, and JSON report formatters.
- Pure Python standard library implementation with zero external dependencies.
