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
        for step in trajectory["steps"]:
            tools.append(step["tool"])

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
    tool_errors = sum(
        1 for t in trajectories
        if t["failure_reason"] == "tool_selection_error"
    )

    return tool_errors / total if total else 0
