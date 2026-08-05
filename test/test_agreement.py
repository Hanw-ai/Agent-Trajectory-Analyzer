"""Tests for judge agreement calculations."""

from src.judge_agreement import (
    build_confusion_matrix,
    compute_agreement_metrics,
    compute_disagreement_breakdown,
    find_disagreements,
)


def sample_judge_results():
    return [
        {
            "task_id": "task_001",
            "rule_label": "pass",
            "llm_label": "pass",
            "rule_failure_type": "success",
            "llm_failure_type": "success",
            "label_agreement": True,
            "failure_type_agreement": True,
            "score_difference": 0,
        },
        {
            "task_id": "task_002",
            "rule_label": "fail",
            "llm_label": "pass",
            "rule_failure_type": "retrieval_error",
            "llm_failure_type": "success",
            "label_agreement": False,
            "failure_type_agreement": False,
            "score_difference": 2,
        },
    ]


def test_compute_agreement_metrics():
    metrics = compute_agreement_metrics(
        sample_judge_results()
    )

    assert metrics["total_evaluated"] == 2
    assert metrics["label_agreement_rate"] == 0.5
    assert (
        metrics["failure_type_agreement_rate"]
        == 0.5
    )
    assert metrics["mean_score_difference"] == 1.0
    assert metrics["disagreement_count"] == 1


def test_find_disagreements():
    disagreements = find_disagreements(
        sample_judge_results()
    )

    assert len(disagreements) == 1
    assert disagreements[0]["task_id"] == "task_002"


def test_compute_disagreement_breakdown():
    breakdown = compute_disagreement_breakdown(
        sample_judge_results()
    )

    assert breakdown == {
        "retrieval_error -> success": 1,
    }


def test_build_confusion_matrix():
    matrix = build_confusion_matrix(
        sample_judge_results()
    )

    assert matrix.loc["pass", "pass"] == 1
    assert matrix.loc["fail", "pass"] == 1
    assert matrix.loc["fail", "fail"] == 0


def test_empty_agreement_metrics():
    metrics = compute_agreement_metrics([])

    assert metrics["total_evaluated"] == 0
    assert metrics["label_agreement_rate"] == 0.0
    assert metrics["disagreement_count"] == 0
