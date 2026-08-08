"""Validation tests for the V2 trajectory benchmark."""

import json
from collections import Counter
from pathlib import Path


DATA_PATH = Path(
    "data/trajectories_v2.json"
)

ALLOWED_CATEGORIES = {
    "tool_use",
    "retrieval",
    "coding",
    "planning",
    "verification",
    "recovery",
    "multi_step_reasoning",
}

ALLOWED_DIFFICULTIES = {
    "easy",
    "medium",
    "hard",
}

ALLOWED_FAILURE_TYPES = {
    None,
    "retrieval_error",
    "tool_selection_error",
    "tool_execution_error",
    "reasoning_error",
    "planning_error",
    "hallucination",
    "verification_failure",
    "recovery_failure",
    "overlong_trajectory",
    "incomplete_execution",
    "context_loss",
}


def load_dataset():
    with DATA_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_dataset_is_non_empty_list():
    trajectories = load_dataset()

    assert isinstance(trajectories, list)
    assert trajectories


def test_task_ids_are_unique():
    trajectories = load_dataset()

    task_ids = [
        item["task_id"]
        for item in trajectories
    ]

    assert len(task_ids) == len(set(task_ids))


def test_required_fields_exist():
    trajectories = load_dataset()

    required_fields = {
        "task_id",
        "category",
        "difficulty",
        "task",
        "expected_tools",
        "success",
        "steps",
        "final_answer",
        "failure_reason",
        "expected_failure_type",
    }

    for trajectory in trajectories:
        assert required_fields.issubset(
            trajectory
        )


def test_categories_are_valid():
    trajectories = load_dataset()

    for trajectory in trajectories:
        assert (
            trajectory["category"]
            in ALLOWED_CATEGORIES
        )


def test_difficulties_are_valid():
    trajectories = load_dataset()

    for trajectory in trajectories:
        assert (
            trajectory["difficulty"]
            in ALLOWED_DIFFICULTIES
        )


def test_failure_types_are_valid():
    trajectories = load_dataset()

    for trajectory in trajectories:
        assert (
            trajectory["failure_reason"]
            in ALLOWED_FAILURE_TYPES
        )


def test_success_and_failure_labels_match():
    trajectories = load_dataset()

    for trajectory in trajectories:
        if trajectory["success"]:
            assert (
                trajectory["failure_reason"]
                is None
            )
            assert (
                trajectory[
                    "expected_failure_type"
                ]
                == "success"
            )
        else:
            assert (
                trajectory["failure_reason"]
                is not None
            )


def test_steps_are_valid():
    trajectories = load_dataset()

    for trajectory in trajectories:
        steps = trajectory["steps"]

        assert isinstance(steps, list)
        assert steps

        for step in steps:
            assert "step" in step
            assert "action" in step
            assert "tool" in step
            assert "input" in step
            assert "output" in step
            assert "status" in step

def test_dataset_contains_multiple_categories():
    trajectories = load_dataset()

    category_counts = Counter(
        item["category"]
        for item in trajectories
    )

    assert len(category_counts) >= 3
