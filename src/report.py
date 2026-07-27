"""Markdown report generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def generate_markdown_report(
    results: Dict[str, Any],
    output_path: str,
) -> None:
    """Generate a Markdown evaluation report."""

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    agreement = results.get(
        "agreement_metrics",
        {},
    )

    lines = [
        "# Agent Trajectory Evaluation Report",
        "",
        "## Executive Summary",
        "",
        (
            f"Evaluated **{results['total_tasks']}** agent "
            "trajectories across task completion, tool use, "
            "failure modes, and evaluator agreement."
        ),
        "",
        "## Core Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        (
            f"| Total Tasks | "
            f"{results['total_tasks']} |"
        ),
        (
            f"| Success Rate | "
            f"{results['success_rate']:.2%} |"
        ),
        (
            f"| Average Trajectory Length | "
            f"{results['avg_trajectory_length']:.2f} |"
        ),
        (
            f"| Tool Error Rate | "
            f"{results['tool_error_rate']:.2%} |"
        ),
        (
            f"| Trajectory Score | "
            f"{results['trajectory_score']:.2f} |"
        ),
        (
            f"| Dominant Failure Mode | "
            f"{results['dominant_failure_mode']} |"
        ),
        "",
        "## Judge Agreement",
        "",
        "| Metric | Value |",
        "|---|---:|",
        (
            "| Pass/Fail Agreement | "
            f"{agreement.get('label_agreement_rate', 0):.2%} |"
        ),
        (
            "| Failure-Type Agreement | "
            f"{agreement.get('failure_type_agreement_rate', 0):.2%} |"
        ),
        (
            "| Mean Score Difference | "
            f"{agreement.get('mean_score_difference', 0):.2f} |"
        ),
        (
            "| Disagreement Count | "
            f"{agreement.get('disagreement_count', 0)} |"
        ),
        "",
        "## Tool Usage",
        "",
    ]

    for tool, count in sorted(
        results["tool_usage"].items()
    ):
        lines.append(f"- `{tool}`: {count}")

    lines.extend(
        [
            "",
            "## Failure Breakdown",
            "",
        ]
    )

    if results["failure_breakdown"]:
        for failure_type, count in sorted(
            results["failure_breakdown"].items()
        ):
            lines.append(
                f"- `{failure_type}`: {count}"
            )
    else:
        lines.append("- No failed trajectories detected.")

    lines.extend(
        [
            "",
            "## Judge Disagreement Patterns",
            "",
        ]
    )

    disagreement_breakdown = results.get(
        "disagreement_breakdown",
        {},
    )

    if disagreement_breakdown:
        for pair, count in disagreement_breakdown.items():
            lines.append(f"- `{pair}`: {count}")
    else:
        lines.append(
            "- No judge disagreements detected."
        )

    lines.extend(
        [
            "",
            "## Artifact Files",
            "",
            "- `reports/judge_results.csv`",
            "- `reports/disagreements.csv`",
            "- `reports/confusion_matrix.csv`",
            "- `reports/failure_breakdown.png`",
            "",
            "## Interpretation",
            "",
            (
                "The framework compares deterministic evaluation "
                "with an LLM-based evaluator to identify both agent "
                "failures and evaluator uncertainty."
            ),
            "",
            (
                "Disagreement cases should be manually reviewed "
                "because they may reveal ambiguous task definitions, "
                "weak ground-truth labels, or insufficient trajectory "
                "evidence."
            ),
        ]
    )

    path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
