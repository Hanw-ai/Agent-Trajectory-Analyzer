"""Agreement analysis between deterministic and model-based judges."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd

from src.judges import RuleBasedJudge
from src.llm_judge import LLMJudge


def evaluate_with_judges(
    trajectories: Iterable[Dict[str, Any]],
    model: str | None = None,
) -> List[Dict[str, Any]]:
    """Evaluate each trajectory with both judges."""

    rule_judge = RuleBasedJudge()
    llm_judge = LLMJudge(model=model)

    results: List[Dict[str, Any]] = []

    for trajectory in trajectories:
        rule_result = rule_judge.evaluate(trajectory)
        llm_result = llm_judge.evaluate(trajectory)

        results.append(
            {
                "task_id": trajectory["task_id"],
                "task": trajectory["task"],
                "ground_truth_success": trajectory.get("success"),
                "ground_truth_failure": (
                    trajectory.get("failure_reason") or "success"
                ),
                "rule_label": rule_result["label"],
                "rule_score": rule_result["score"],
                "rule_failure_type": rule_result["failure_type"],
                "llm_label": llm_result["label"],
                "llm_score": llm_result["score"],
                "llm_failure_type": llm_result["failure_type"],
                "llm_reasoning": llm_result["reasoning_summary"],
                "llm_suggestion": llm_result["improvement_suggestion"],
                "evaluation_mode": llm_result.get(
                    "evaluation_mode",
                    "unknown",
                ),
                "label_agreement": (
                    rule_result["label"] == llm_result["label"]
                ),
                "failure_type_agreement": (
                    rule_result["failure_type"]
                    == llm_result["failure_type"]
                ),
                "score_difference": abs(
                    rule_result["score"] - llm_result["score"]
                ),
            }
        )

    return results


def compute_agreement_metrics(
    judge_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Compute label and failure-type agreement statistics."""

    total = len(judge_results)

    if total == 0:
        return {
            "total_evaluated": 0,
            "label_agreement_rate": 0.0,
            "failure_type_agreement_rate": 0.0,
            "mean_score_difference": 0.0,
            "disagreement_count": 0,
        }

    label_agreements = sum(
        int(result["label_agreement"])
        for result in judge_results
    )

    failure_agreements = sum(
        int(result["failure_type_agreement"])
        for result in judge_results
    )

    mean_score_difference = sum(
        result["score_difference"]
        for result in judge_results
    ) / total

    disagreement_count = sum(
        int(
            not result["label_agreement"]
            or not result["failure_type_agreement"]
        )
        for result in judge_results
    )

    return {
        "total_evaluated": total,
        "label_agreement_rate": round(
            label_agreements / total,
            4,
        ),
        "failure_type_agreement_rate": round(
            failure_agreements / total,
            4,
        ),
        "mean_score_difference": round(
            mean_score_difference,
            4,
        ),
        "disagreement_count": disagreement_count,
    }


def build_confusion_matrix(
    judge_results: List[Dict[str, Any]],
) -> pd.DataFrame:
    """Create a pass/fail confusion matrix."""

    if not judge_results:
        return pd.DataFrame(
            0,
            index=["rule_fail", "rule_pass"],
            columns=["llm_fail", "llm_pass"],
        )

    frame = pd.DataFrame(judge_results)

    matrix = pd.crosstab(
        frame["rule_label"],
        frame["llm_label"],
        rownames=["rule_judge"],
        colnames=["llm_judge"],
        dropna=False,
    )

    return matrix.reindex(
        index=["fail", "pass"],
        columns=["fail", "pass"],
        fill_value=0,
    )


def find_disagreements(
    judge_results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Return trajectories where judges disagree."""

    return [
        result
        for result in judge_results
        if (
            not result["label_agreement"]
            or not result["failure_type_agreement"]
        )
    ]


def compute_disagreement_breakdown(
    judge_results: List[Dict[str, Any]],
) -> Dict[str, int]:
    """Count common rule-to-LLM failure-type disagreement pairs."""

    counter = Counter()

    for result in find_disagreements(judge_results):
        pair = (
            f"{result['rule_failure_type']}"
            f" -> {result['llm_failure_type']}"
        )
        counter[pair] += 1

    return dict(counter.most_common())


def export_agreement_outputs(
    judge_results: List[Dict[str, Any]],
    output_dir: str = "reports",
) -> None:
    """Write full results, disagreements, and confusion matrix to CSV."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    results_frame = pd.DataFrame(judge_results)
    results_frame.to_csv(
        output_path / "judge_results.csv",
        index=False,
    )

    disagreement_frame = pd.DataFrame(
        find_disagreements(judge_results)
    )
    disagreement_frame.to_csv(
        output_path / "disagreements.csv",
        index=False,
    )

    confusion_matrix = build_confusion_matrix(judge_results)
    confusion_matrix.to_csv(
        output_path / "confusion_matrix.csv"
    )
