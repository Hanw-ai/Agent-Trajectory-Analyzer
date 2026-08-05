"""Deterministic metrics for agent trajectories."""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


Trajectory = Dict[str, Any]


def compute_success_rate(
    trajectories: List[Trajectory],
) -> float:
    """Return the proportion of successful trajectories."""

    total = len(trajectories)

    if total == 0:
        return 0.0

    successful = sum(
        1
        for trajectory in trajectories
        if trajectory.get("success", False)
    )

    return successful / total


def compute_avg_trajectory_length(
    trajectories: List[Trajectory],
) -> float:
    """Return the average number of steps per trajectory."""

    if not trajectories:
        return 0.0

    total_steps = sum(
        len(trajectory.get("steps", []))
        for trajectory in trajectories
    )

    return total_steps / len(trajectories)


def compute_tool_usage(
    trajectories: List[Trajectory],
) -> Dict[str, int]:
    """Count how often each tool appears in trajectory steps."""

    tools = []

    for trajectory in trajectories:
        for step in trajectory.get("steps", []):
            tool = step.get("tool")

            if tool:
                tools.append(tool)

    return dict(Counter(tools))


def compute_failure_breakdown(
    trajectories: List[Trajectory],
) -> Dict[str, int]:
    """Count failed trajectories by failure reason."""

    failures = [
        trajectory.get("failure_reason")
        for trajectory in trajectories
        if (
            not trajectory.get("success", False)
            and trajectory.get("failure_reason")
        )
    ]

    return dict(Counter(failures))


def compute_tool_error_rate(
    trajectories: List[Trajectory],
) -> float:
    """Return the rate of tool-related failures."""

    total = len(trajectories)

    if total == 0:
        return 0.0

    tool_failure_types = {
        "tool_selection_error",
        "tool_execution_error",
    }

    tool_errors = sum(
        1
        for trajectory in trajectories
        if trajectory.get("failure_reason")
        in tool_failure_types
    )

    return tool_errors / total


def compute_trajectory_score(
    success_rate: float,
    tool_error_rate: float,
) -> float:
    """Compute a simple aggregate score from 0 to 100."""

    score = (
        success_rate * 100
        - tool_error_rate * 50
    )

    return round(
        max(0.0, min(100.0, score)),
        2,
    )


def compute_dominant_failure_mode(
    failure_breakdown: Dict[str, int],
) -> str:
    """Return the most common failure category."""

    if not failure_breakdown:
        return "none"

    return max(
        failure_breakdown,
        key=failure_breakdown.get,
    )
