from __future__ import annotations

import json
from .models import AuditScorecard


def format_table(card: AuditScorecard) -> str:
    lines = []
    lines.append("┌────────────────────────────────────────────────────────────┐")
    lines.append("│              AI RISK GOVERNANCE AUDIT REPORT               │")
    lines.append("├────────────────────────────────────────────────────────────┤")
    lines.append(f"│ Target: {card.target_name:<36} Grade: {card.grade} ({card.overall_score:.1f}%) │")
    lines.append(f"│ Probes Executed: {card.total_probes:<4} Passed: {card.passed_probes:<4} Deficiencies: {card.total_probes - card.passed_probes:<4} │")
    lines.append("├──────────────────────────────────┬──────────────┬──────────┤")
    lines.append("│ Control Category                 │ Compliance   │ Status   │")
    lines.append("├──────────────────────────────────┼──────────────┼──────────┤")
    for cat, score in sorted(card.category_scores.items()):
        status = "COMPLIANT" if score >= 85.0 else "ATTENTION"
        lines.append(f"│ {cat:<32} │ {score:>10.1f}% │ {status:<8} │")
    lines.append("└──────────────────────────────────┴──────────────┴──────────┘")

    failed = [f for f in card.findings if not f.passed]
    if failed:
        lines.append("\nDeficiencies Identified:")
        for idx, f in enumerate(failed, 1):
            lines.append(f" {idx}. [{f.risk.value.upper()}] {f.probe_id} - {f.name}")
            lines.append(f"    Issue: {f.description}")
            lines.append(f"    Remediation: {f.remediation}")
    return "\n".join(lines)


def format_markdown(card: AuditScorecard) -> str:
    failed = [f for f in card.findings if not f.passed]
    lines = [
        f"# AI Governance & Security Audit: {card.target_name}",
        "",
        f"- **Audit Date (UTC):** `{card.timestamp}`",
        f"- **Overall Compliance Grade:** **`{card.grade}`** (`{card.overall_score:.1f}%`)",
        f"- **Probes Evaluated:** {card.total_probes} ({card.passed_probes} Passed, {len(failed)} Deficiencies)",
        "",
        "## Category Compliance Summary",
        "",
        "| Control Category | Compliance Score | Status |",
        "| :--- | :--- | :--- |",
    ]
    for cat, score in sorted(card.category_scores.items()):
        status = "✅ COMPLIANT" if score >= 85.0 else "⚠️ DEFICIENCY"
        lines.append(f"| `{cat}` | `{score:.1f}%` | {status} |")

    lines.append("")
    lines.append("## Findings & Remediation Ledger")
    lines.append("")
    if not failed:
        lines.append("All technical governance probes passed successfully. Target meets audit readiness baseline.")
    else:
        for f in failed:
            lines.extend([
                f"### [{f.risk.value.upper()}] {f.probe_id}: {f.name}",
                f"- **Category:** `{f.category.value}`",
                f"- **Description:** {f.description}",
                f"- **Observed Output:** `{f.observed_output}`",
                f"- **Recommended Remediation:** {f.remediation}",
                "",
            ])
    return "\n".join(lines)


def format_json(card: AuditScorecard) -> str:
    return json.dumps(card.to_dict(), indent=2)
