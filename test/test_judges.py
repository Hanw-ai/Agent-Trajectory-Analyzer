"""Tests for the deterministic rule-based judge."""

import pytest

from src.judges import RuleBasedJudge


def test_successful_trajectory_passes():
    trajectory = {
        "task_id": "task_001",
        "task": "Retrieve documentation.",
        "success": True,
        "steps": [
            {
                "tool": "search",
                "status": "success",
            }
        ],
        "expected_tools": ["search"],
        "failure_reason": None,
    }

    result = RuleBasedJudge().evaluate(
        trajectory
    )

    assert result["label"] == "pass"
    assert result["failure_type"] == "success"
    assert result["score"] == 5


def test_failed_trajectory_returns_failure_type():
    trajectory = {
        "task_id": "task_002",
        "task": "Retrieve documentation.",
        "success": False,
        "steps": [
            {
                "tool": "search",
                "status": "error",
            }
        ],
        "failure_reason": "retrieval_error",
    }

    result = RuleBasedJudge().evaluate(
        trajectory
    )

    assert result["label"] == "fail"
    assert result["failure_type"] == "retrieval_error"
    assert result["score"] == 2


def test_unknown_failure_is_normalized():
    trajectory = {
        "task_id": "task_003",
        "task": "Complete an agent task.",
        "success": False,
        "steps": [],
        "failure_reason": "made_up_failure",
    }

    result = RuleBasedJudge().evaluate(
        trajectory
    )

    assert result["label"] == "fail"
    assert result["failure_type"] == "unknown_failure"


def test_missing_required_field_raises_error():
    trajectory = {
        "task_id": "task_004",
        "success": True,
        "steps": [],
    }

    with pytest.raises(
        ValueError,
        match="missing required fields",
    ):
        RuleBasedJudge().evaluate(
            trajectory
        )


def test_steps_must_be_a_list():
    trajectory = {
        "task_id": "task_005",
        "task": "Complete an agent task.",
        "success": True,
        "steps": "not-a-list",
    }

    with pytest.raises(TypeError):
        RuleBasedJudge().evaluate(
            trajectory
        )
