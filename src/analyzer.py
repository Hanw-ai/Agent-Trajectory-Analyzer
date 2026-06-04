import json

from src.judges import compute_judge_agreement, evaluate_with_judges

from src.metrics import (
    compute_success_rate,
    compute_avg_trajectory_length,
    compute_tool_usage,
    compute_failure_breakdown,
    compute_tool_error_rate,
    compute_trajectory_score,
    compute_dominant_failure_mode,
)


class TrajectoryAnalyzer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.trajectories = self.load_data()

    def load_data(self):
        with open(self.data_path, "r") as file:
            return json.load(file)

    def analyze(self):
        success_rate = compute_success_rate(self.trajectories)
        tool_error_rate = compute_tool_error_rate(self.trajectories)
        failure_breakdown = compute_failure_breakdown(self.trajectories)

        results = {
            "total_tasks": len(self.trajectories),
            "success_rate": success_rate,
            "avg_trajectory_length": compute_avg_trajectory_length(self.trajectories),
            "tool_usage": compute_tool_usage(self.trajectories),
            "failure_breakdown": failure_breakdown,
            "tool_error_rate": tool_error_rate,
            "trajectory_score": compute_trajectory_score(success_rate, tool_error_rate),
            "dominant_failure_mode": compute_dominant_failure_mode(failure_breakdown),
            "judge_agreement": compute_judge_agreement(self.trajectories),
            "judge_results": evaluate_with_judges(self.trajectories),
        }

        return results
