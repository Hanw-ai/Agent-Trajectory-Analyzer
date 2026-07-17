"""Markdown report generation for trajectory evaluation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def _format_rate(value: float) -> str:
    return f"{value * 100:.1f}%"


def generate_markdown_report(
    results: Dict[str, Any],
    output_path: str,
) -> None:
    agreement = results["agreement_metrics"]
    disagreements = results["disagreements"]

    lines = [
        "# Agent Trajectory Analyzer V2 Report",
        "",
        "## Executive Summary",
        "",
        f"- Total trajectories: **{results['total_tasks']}**",
        f"- Task success rate: **{_format_rate(results['success_rate'])}**",
        f"- Tool error rate: **{_format_rate(results['tool_error_rate'])}**",
        f"- Average trajectory length: **{results['avg_trajectory_length']:.2f}**",
        f"- Overall trajectory score: **{results['trajectory_score']:.3f}**",
        f"- Dominant failure mode: **{results['dominant_failure_mode']}**",
        "",
        "## Judge Agreement",
        "",
        f"- Trajectories evaluated: **{agreement['total_evaluated']}**",
        (
            "- Pass/fail agreement: "
            f"**{_format_rate(agreement['label_agreement_rate'])}**"
        ),
        (
            "- Failure-type agreement: "
            f"**{_format_rate(agreement['failure_type_agreement_rate'])}**"
        ),
        (
            "- Mean score difference: "
            f"**{agreement['mean_score_difference']:.2f}**"
        ),
        (
            "- Disagreement cases: "
            f"**{agreement['disagreement_count']}**"
        ),
        "",
        "## Failure Breakdown",
        "",
        "| Failure type | Count |",
        "|---|---:|",
    ]

    for failure_type, count in sorted(
        results["failure_breakdown"].items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        lines.append(
            f"| {failure_type} | {count} |"
        )

    lines.extend(
        [
            "",
            "## Tool Usage",
            "",
            "| Tool | Calls |",
            "|---|---:|",
        ]
    )

    for tool, count in sorted(
        results["tool_usage"].items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        lines.append(f"| {tool} | {count} |")

    lines.extend(
        [
            "",
            "## Judge Disagreements",
            "",
        ]
    )

    if not disagreements:
        lines.append(
            "No judge disagreements were detected."
        )
    else:
        lines.extend(
            [
                "| Task | Rule judge | LLM judge | Rule failure | LLM failure |",
                "|---|---|---|---|---|",
            ]
        )

        for item in disagreements:
            lines.append(
                f"| {item['task_id']} "
                f"| {item['rule_label']} "
                f"| {item['llm_label']} "
                f"| {item['rule_failure_type']} "
                f"| {item['llm_failure_type']} |"
            )

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- `reports/judge_results.csv`",
            "- `reports/disagreements.csv`",
            "- `reports/confusion_matrix.csv`",
            "- `reports/failure_breakdown.png`",
            "",
            "## Interpretation",
            "",
            (
                "Judge disagreement is treated as a diagnostic signal rather "
                "than automatically as an error. Disagreement cases should be "
                "reviewed to identify rubric ambiguity, insufficient trajectory "
                "logging, or evaluator bias."
            ),
            "",
        ]
    )

    report_path = Path(output_path)
    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
