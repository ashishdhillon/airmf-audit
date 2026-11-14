from __future__ import annotations

import html
from .models import AuditScorecard


def generate_html_scorecard(card: AuditScorecard) -> str:
    """Generate a self-contained, standalone HTML audit report and compliance scorecard."""
    target_name = html.escape(card.target_name)
    grade = html.escape(card.grade)
    timestamp = html.escape(card.timestamp)
    overall_score = card.overall_score
    deficiencies = card.total_probes - card.passed_probes

    # Determine theme color based on grade
    if grade == "A":
        grade_color = "#10b981"  # Emerald
        grade_label = "FULLY COMPLIANT"
    elif grade == "B":
        grade_color = "#3b82f6"  # Blue
        grade_label = "SUBSTANTIALLY COMPLIANT"
    elif grade == "C":
        grade_color = "#f59e0b"  # Amber
        grade_label = "NEEDS ATTENTION"
    else:
        grade_color = "#ef4444"  # Rose
        grade_label = "NON-COMPLIANT"

    # Category progress bars
    category_cards_html = []
    for cat_name, cat_score in sorted(card.category_scores.items()):
        cat_escaped = html.escape(cat_name)
        bar_color = "#10b981" if cat_score >= 85.0 else ("#f59e0b" if cat_score >= 60.0 else "#ef4444")
        category_cards_html.append(f"""
        <div class="category-card">
            <div class="category-header">
                <span class="category-title">{cat_escaped}</span>
                <span class="category-score" style="color: {bar_color};">{cat_score:.1f}%</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {cat_score:.1f}%; background-color: {bar_color};"></div>
            </div>
        </div>
        """)

    # Findings rows
    findings_rows = []
    for f in card.findings:
        f_id = html.escape(f.probe_id)
        f_name = html.escape(f.name)
        f_cat = html.escape(f.category.value)
        f_risk = html.escape(f.risk.value.upper())
        status_badge = '<span class="badge pass">PASSED</span>' if f.passed else '<span class="badge fail">DEFICIENCY</span>'

        risk_color = {
            "CRITICAL": "#ef4444",
            "HIGH": "#f97316",
            "MEDIUM": "#f59e0b",
            "LOW": "#3b82f6",
        }.get(f_risk, "#6b7280")

        remediation_html = ""
        if not f.passed:
            rem_text = html.escape(f.remediation)
            obs_text = html.escape(f.observed_output)
            remediation_html = f"""
            <div class="deficiency-details">
                <strong>Observed Output:</strong> <code>{obs_text}</code><br/>
                <strong>Recommended Remediation:</strong> {rem_text}
            </div>
            """

        findings_rows.append(f"""
        <tr>
            <td><code>{f_id}</code></td>
            <td><strong>{f_name}</strong><br/><small class="text-muted">{f_cat}</small></td>
            <td><span class="risk-badge" style="background-color: {risk_color}20; color: {risk_color}; border: 1px solid {risk_color}50;">{f_risk}</span></td>
            <td>{status_badge}</td>
        </tr>
        {"<tr><td colspan='4'>" + remediation_html + "</td></tr>" if remediation_html else ""}
        """)

    categories_joined = "\n".join(category_cards_html)
    findings_joined = "\n".join(findings_rows)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Governance & Risk Scorecard: {target_name}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --surface: #1e293b;
            --surface-border: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg);
            color: var(--text-primary);
            font-family: var(--font-family);
            line-height: 1.5;
            padding: 2rem 1rem;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        .header {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
        }}
        .header-title h1 {{
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--text-primary);
        }}
        .header-title p {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }}
        .grade-badge-container {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .grade-badge {{
            width: 72px;
            height: 72px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.2rem;
            font-weight: 800;
            border: 3px solid {grade_color};
            color: {grade_color};
            background-color: {grade_color}15;
        }}
        .grade-status {{
            font-weight: 700;
            font-size: 1.1rem;
            color: {grade_color};
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }}
        .kpi-card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 10px;
            padding: 1.25rem;
        }}
        .kpi-label {{
            font-size: 0.82rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 0.4rem;
        }}
        .section-title {{
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}
        .categories-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .category-card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 8px;
            padding: 1rem;
        }}
        .category-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }}
        .category-title {{
            font-size: 0.9rem;
            font-weight: 600;
        }}
        .category-score {{
            font-weight: 700;
            font-size: 0.95rem;
        }}
        .progress-bar-bg {{
            background: #334155;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
        }}
        .progress-bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        .findings-table-card {{
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 2rem;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.92rem;
        }}
        th, td {{
            padding: 0.85rem 1.2rem;
            text-align: left;
        }}
        th {{
            background: #192237;
            color: var(--text-secondary);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid var(--surface-border);
        }}
        tr:not(:last-child) td {{
            border-bottom: 1px solid var(--surface-border);
        }}
        .badge {{
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
        }}
        .badge.pass {{
            background-color: #10b98125;
            color: #34d399;
            border: 1px solid #10b98140;
        }}
        .badge.fail {{
            background-color: #ef444425;
            color: #f87171;
            border: 1px solid #ef444440;
        }}
        .risk-badge {{
            display: inline-block;
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 600;
        }}
        .deficiency-details {{
            background: #29151b;
            border-left: 3px solid #ef4444;
            padding: 0.75rem 1rem;
            font-size: 0.85rem;
            margin: 0.25rem 0;
            color: #fca5a5;
        }}
        .deficiency-details code {{
            background: #1e1115;
            padding: 0.15rem 0.35rem;
            border-radius: 4px;
            color: #fecaca;
        }}
        .text-muted {{ color: var(--text-secondary); }}
        code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.85em; }}
        .footer {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.82rem;
            padding-top: 1rem;
            border-top: 1px solid var(--surface-border);
        }}
        @media print {{
            body {{ background: #ffffff; color: #000000; padding: 0; }}
            .header, .kpi-card, .category-card, .findings-table-card {{
                background: #ffffff; border-color: #e2e8f0; color: #000000; box-shadow: none;
            }}
            .header-title h1, .section-title {{ color: #000000; }}
            th {{ background: #f1f5f9; color: #334155; }}
            .progress-bar-bg {{ background: #e2e8f0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-title">
                <h1>AI Governance & Risk Scorecard</h1>
                <p>Audited Target: <strong>{target_name}</strong> &bull; Generated: {timestamp}</p>
            </div>
            <div class="grade-badge-container">
                <div class="grade-badge">{grade}</div>
                <div>
                    <div class="grade-status">{grade_label}</div>
                    <div style="font-size: 0.82rem; color: var(--text-secondary);">Technical Control Rating</div>
                </div>
            </div>
        </header>

        <section class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Overall Compliance</div>
                <div class="kpi-value" style="color: {grade_color};">{overall_score:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Controls Tested</div>
                <div class="kpi-value">{card.total_probes}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Passed Controls</div>
                <div class="kpi-value" style="color: #10b981;">{card.passed_probes}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Deficiencies Found</div>
                <div class="kpi-value" style="color: {'#ef4444' if deficiencies > 0 else '#10b981'};">{deficiencies}</div>
            </div>
        </section>

        <section>
            <h2 class="section-title">Category Compliance Breakdown</h2>
            <div class="categories-grid">
                {categories_joined}
            </div>
        </section>

        <section>
            <h2 class="section-title">Control Findings Ledger</h2>
            <div class="findings-table-card">
                <table>
                    <thead>
                        <tr>
                            <th>Control ID</th>
                            <th>Control Evaluation</th>
                            <th>Risk Tier</th>
                            <th>Audit Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {findings_joined}
                    </tbody>
                </table>
            </div>
        </section>

        <footer class="footer">
            <p>Generated by <strong>airmf-audit</strong> &bull; Zero-Dependency Automated AI Governance and Security Evaluation Harness</p>
        </footer>
    </div>
</body>
</html>
"""
