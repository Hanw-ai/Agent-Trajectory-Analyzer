from collections import Counter


def compute_success_rate(trajectories):
    total = len(trajectories)
    successful = sum(1 for t in trajectories if t["success"])
    return successful / total if total else 0


def compute_avg_trajectory_length(trajectories):
    total_steps = sum(len(t["steps"]) for t in trajectories)
    return total_steps / len(trajectories) if trajectories else 0


def compute_tool_usage(trajectories):
    tools = []

    for trajectory in trajectories:
        for step in trajectory.get("steps", []):
            tool = step.get("tool")

            if tool:
                tools.append(tool)

    return dict(Counter(tools))


def compute_failure_breakdown(trajectories):
    failures = [
        t["failure_reason"]
        for t in trajectories
        if not t["success"] and t["failure_reason"] is not None
    ]

    return dict(Counter(failures))


def compute_tool_error_rate(trajectories):
    total = len(trajectories)

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

    return tool_errors / total if total else 0


def compute_trajectory_score(success_rate, tool_error_rate):
    return success_rate * 100 - tool_error_rate * 50


def compute_dominant_failure_mode(failure_breakdown):
    if not failure_breakdown:
        return "none"

    return max(failure_breakdown, key=failure_breakdown.get)
