from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .auditor import AIAuditor
from .http_target import create_http_target
from .probes import DEFAULT_PROBES
from .reporters import format_html, format_json, format_markdown, format_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="airmf-audit",
        description="Automated technical control auditor and governance evaluation harness for LLMs.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # audit
    audit_parser = subparsers.add_parser("audit", help="Run automated governance and security audit against LLM target")
    audit_parser.add_argument("--endpoint", help="HTTP endpoint URL (e.g. http://localhost:11434/v1/chat/completions). Uses mock target if omitted.")
    audit_parser.add_argument("--model", default="default", help="Model name for HTTP endpoint (default: default)")
    audit_parser.add_argument("--api-key", help="Optional Bearer token for HTTP endpoint")
    audit_parser.add_argument("--format", choices=["table", "markdown", "json", "html"], default="table", help="Output format")
    audit_parser.add_argument("--output", "-o", help="Write report to specified output path")
    audit_parser.add_argument("--strict", action="store_true", help="Exit with code 1 if any deficiencies (grade < A) are found")

    # list-controls
    subparsers.add_parser("list-controls", help="List all evaluated governance and security controls")

    return parser


def handle_audit(args: argparse.Namespace) -> int:
    if args.endpoint:
        target_fn = create_http_target(args.endpoint, model=args.model, api_key=args.api_key)
        target_name = f"{args.model} @ {args.endpoint}"
    else:
        target_fn = None
        target_name = "Target LLM System (Baseline Mock)"

    auditor = AIAuditor()
    scorecard = auditor.audit(target_fn=target_fn, target_name=target_name)

    if args.format == "json":
        report = format_json(scorecard)
    elif args.format == "markdown":
        report = format_markdown(scorecard)
    elif args.format == "html":
        report = format_html(scorecard)
    else:
        report = format_table(scorecard)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Audit report saved to {args.output}")
    else:
        print(report)

    if args.strict and scorecard.grade != "A":
        return 1
    return 0


def handle_list_controls(args: argparse.Namespace) -> int:
    print("Available Technical Governance Controls:")
    for p in DEFAULT_PROBES:
        print(f" • [{p.probe_id}] {p.name} ({p.category.value}) - Risk: {p.risk.value.upper()}")
        print(f"   {p.description}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "audit":
        return handle_audit(args)
    elif args.command == "list-controls":
        return handle_list_controls(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
