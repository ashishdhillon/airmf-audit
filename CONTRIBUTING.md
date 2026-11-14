# Contributing to airmf-audit

Thank you for your interest in contributing to `airmf-audit`! We welcome contributions to expand control coverage, enhance reporting, and refine governance probe evaluators.

---

## Development Principles

1. **Zero External Runtime Dependencies:**
   All core probes, HTTP transports, reporters, and models must strictly use Python 3.9+ standard library modules (`urllib.request`, `json`, `re`, `html`, `argparse`, `dataclasses`).

2. **Standard Test Framework:**
   All test cases must use Python's built-in `unittest` module and pass deterministically without network access.

3. **Deterministic Evaluation:**
   Probes should have clear pass/fail criteria grounded in observable security control boundaries.

---

## Local Setup

```bash
git clone https://github.com/ashishdhillon/airmf-audit.git
cd airmf-audit
pip install -e .
```

Run test suite:

```bash
python3 -m unittest discover -s tests -v
```

---

## Adding a New Governance Probe

1. Inherit from `BaseProbe` in `src/airmf_audit/probes/base.py`.
2. Define the required attributes:
   - `probe_id`: Unique control identifier (e.g. `ADV-004`, `PRV-004`).
   - `category`: `ControlCategory` enum member.
   - `risk`: `RiskLevel` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
   - `name`: Concise control name.
   - `description`: What control requirement is evaluated.
   - `remediation`: Clear, actionable engineering advice for mitigating failure.
3. Implement `run(self, target_fn: Callable[[str], str]) -> ProbeResult`.
4. Register the new probe in `src/airmf_audit/probes/__init__.py`.
5. Add unit tests in `tests/` covering both compliant and vulnerable behaviors.

---

## Submitting a Pull Request

- Use conventional commit messages (`feat:`, `fix:`, `test:`, `docs:`).
- Keep changes scoped to a dedicated feature branch.
- Ensure all tests pass prior to submitting your PR.
