"""Tests for deterministic trajectory metrics."""

from src.metrics import (
    compute_avg_trajectory_length,
    compute_dominant_failure_mode,
    compute_failure_breakdown,
    compute_success_rate,
    compute_tool_error_rate,
    compute_tool_usage,
    compute_trajectory_score,
)


def sample_trajectories():
    return [
        {
            "task_id": "task_001",
            "task": "Retrieve documentation.",
            "success": True,
            "steps": [
                {
                    "tool": "search",
                    "status": "success",
                },
                {
                    "tool": "browser",
                    "status": "success",
                },
            ],
            "failure_reason": None,
        },
        {
            "task_id": "task_002",
            "task": "Run a calculation.",
            "success": False,
            "steps": [
                {
                    "tool": "search",
                    "status": "success",
                }
            ],
            "failure_reason": "tool_selection_error",
        },
    ]


def test_compute_success_rate():
    result = compute_success_rate(
        sample_trajectories()
    )

    assert result == 0.5


def test_compute_average_trajectory_length():
    result = compute_avg_trajectory_length(
        sample_trajectories()
    )

    assert result == 1.5


def test_compute_tool_usage():
    result = compute_tool_usage(
        sample_trajectories()
    )

    assert result == {
        "search": 2,
        "browser": 1,
    }


def test_compute_failure_breakdown():
    result = compute_failure_breakdown(
        sample_trajectories()
    )

    assert result == {
        "tool_selection_error": 1,
    }


def test_compute_tool_error_rate():
    result = compute_tool_error_rate(
        sample_trajectories()
    )

    assert result == 0.5


def test_compute_trajectory_score():
    result = compute_trajectory_score(
        success_rate=0.5,
        tool_error_rate=0.5,
    )

    assert result == 25.0


def test_compute_dominant_failure_mode():
    result = compute_dominant_failure_mode(
        {
            "retrieval_error": 1,
            "tool_selection_error": 3,
        }
    )

    assert result == "tool_selection_error"


def test_empty_dataset_metrics():
    assert compute_success_rate([]) == 0.0
    assert compute_avg_trajectory_length([]) == 0.0
    assert compute_tool_error_rate([]) == 0.0
    assert compute_tool_usage([]) == {}
    assert compute_failure_breakdown([]) == {}
