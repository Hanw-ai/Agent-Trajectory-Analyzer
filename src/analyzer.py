import json
from src.metrics import (
    compute_success_rate,
    compute_avg_trajectory_length,
    compute_tool_usage,
    compute_failure_breakdown,
    compute_tool_error_rate,
)


class TrajectoryAnalyzer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.trajectories = self.load_data()

    def load_data(self):
        with open(self.data_path, "r") as file:
            return json.load(file)

    def analyze(self):
        results = {
            "total_tasks": len(self.trajectories),
            "success_rate": compute_success_rate(self.trajectories),
            "avg_trajectory_length": compute_avg_trajectory_length(self.trajectories),
            "tool_usage": compute_tool_usage(self.trajectories),
            "failure_breakdown": compute_failure_breakdown(self.trajectories),
            "tool_error_rate": compute_tool_error_rate(self.trajectories),
        }

        return results
