"""Run the Agent Trajectory Analyzer V2 demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.analyzer import TrajectoryAnalyzer
from src.report import generate_markdown_report
from src.visualization import plot_failure_breakdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze tool-using agent trajectories."
    )

    parser.add_argument(
        "--data",
        default="data/trajectories_v2.json",
        help="Path to the trajectory dataset.",
    )

    parser.add_argument(
        "--report",
        default="reports/v2_report.md",
        help="Path for the generated Markdown report.",
    )

    parser.add_argument(
        "--model",
        default=None,
        help="Optional OpenAI judge model.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    Path("reports").mkdir(
        parents=True,
        exist_ok=True,
    )

    analyzer = TrajectoryAnalyzer(
        data_path=args.data,
        model=args.model,
    )

    results = analyzer.analyze(
        export_csv=True,
    )

    print("\nAgent Trajectory Analyzer V2")
    print("=" * 40)

    summary = {
        "total_tasks": results["total_tasks"],
        "success_rate": results["success_rate"],
        "trajectory_score": results["trajectory_score"],
        "dominant_failure_mode": (
            results["dominant_failure_mode"]
        ),
        "agreement_metrics": (
            results["agreement_metrics"]
        ),
    }

    print(
        json.dumps(
            summary,
            indent=2,
        )
    )

    generate_markdown_report(
        results,
        args.report,
    )

    plot_failure_breakdown(
        results["failure_breakdown"]
    )

    print(f"\nReport generated: {args.report}")
    print(
        "Judge results generated: "
        "reports/judge_results.csv"
    )
    print(
        "Disagreements generated: "
        "reports/disagreements.csv"
    )
    print(
        "Confusion matrix generated: "
        "reports/confusion_matrix.csv"
    )
    print(
        "Chart generated: "
        "reports/failure_breakdown.png"
    )


if __name__ == "__main__":
    main()
