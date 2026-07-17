"""Main orchestration layer for trajectory analysis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from src.judge_agreement import (
    compute_agreement_metrics,
    compute_disagreement_breakdown,
    evaluate_with_judges,
    export_agreement_outputs,
    find_disagreements,
)
from src.metrics import (
    compute_avg_trajectory_length,
    compute_dominant_failure_mode,
    compute_failure_breakdown,
    compute_success_rate,
    compute_tool_error_rate,
    compute_tool_usage,
    compute_trajectory_score,
)


class TrajectoryAnalyzer:
    """Load, validate, and analyze agent trajectory records."""

    def __init__(
        self,
        data_path: str,
        model: str | None = None,
    ) -> None:
        self.data_path = Path(data_path)
        self.model = model
        self.trajectories = self.load_data()

    def load_data(self) -> List[Dict[str, Any]]:
        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Trajectory data not found: {self.data_path}"
            )

        with self.data_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise TypeError(
                "Trajectory data must be a JSON array."
            )

        self._validate_unique_task_ids(data)

        return data

    def analyze(
        self,
        export_csv: bool = True,
    ) -> Dict[str, Any]:
        success_rate = compute_success_rate(self.trajectories)
        tool_error_rate = compute_tool_error_rate(self.trajectories)
        failure_breakdown = compute_failure_breakdown(
            self.trajectories
        )

        judge_results = evaluate_with_judges(
            self.trajectories,
            model=self.model,
        )

        agreement_metrics = compute_agreement_metrics(
            judge_results
        )

        if export_csv:
            export_agreement_outputs(judge_results)

        return {
            "total_tasks": len(self.trajectories),
            "success_rate": success_rate,
            "avg_trajectory_length": (
                compute_avg_trajectory_length(
                    self.trajectories
                )
            ),
            "tool_usage": compute_tool_usage(
                self.trajectories
            ),
            "failure_breakdown": failure_breakdown,
            "tool_error_rate": tool_error_rate,
            "trajectory_score": compute_trajectory_score(
                success_rate,
                tool_error_rate,
            ),
            "dominant_failure_mode": (
                compute_dominant_failure_mode(
                    failure_breakdown
                )
            ),
            "agreement_metrics": agreement_metrics,
            "disagreement_breakdown": (
                compute_disagreement_breakdown(
                    judge_results
                )
            ),
            "disagreements": find_disagreements(
                judge_results
            ),
            "judge_results": judge_results,
        }

    @staticmethod
    def _validate_unique_task_ids(
        trajectories: List[Dict[str, Any]],
    ) -> None:
        task_ids = [
            trajectory.get("task_id")
            for trajectory in trajectories
        ]

        duplicates = {
            task_id
            for task_id in task_ids
            if task_ids.count(task_id) > 1
        }

        if duplicates:
            duplicate_list = ", ".join(
                sorted(str(item) for item in duplicates)
            )
            raise ValueError(
                f"Duplicate task IDs found: {duplicate_list}"
            )
