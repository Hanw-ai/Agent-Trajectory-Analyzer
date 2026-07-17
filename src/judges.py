"""Deterministic rule-based judge for agent trajectories."""

from __future__ import annotations

from typing import Any, Dict


VALID_FAILURE_TYPES = {
    "success",
    "retrieval_error",
    "tool_selection_error",
    "tool_execution_error",
    "reasoning_error",
    "context_loss",
    "hallucination",
    "incomplete_execution",
    "verification_failure",
    "recovery_failure",
    "unknown_failure",
}


FAILURE_SCORE_MAP = {
    "retrieval_error": 2,
    "tool_selection_error": 2,
    "tool_execution_error": 2,
    "reasoning_error": 2,
    "context_loss": 1,
    "hallucination": 1,
    "incomplete_execution": 2,
    "verification_failure": 2,
    "recovery_failure": 2,
    "unknown_failure": 1,
}


class RuleBasedJudge:
    """Evaluate trajectories using deterministic success and failure signals."""

    name = "rule_based"

    def evaluate(self, trajectory: Dict[str, Any]) -> Dict[str, Any]:
        self._validate_trajectory(trajectory)

        success = bool(trajectory.get("success", False))
        failure_type = trajectory.get("failure_reason") or "unknown_failure"
        steps = trajectory.get("steps", [])

        if success:
            score = self._score_successful_trajectory(trajectory)

            return {
                "task_id": trajectory["task_id"],
                "judge": self.name,
                "score": score,
                "label": "pass",
                "failure_type": "success",
                "reasoning_summary": (
                    "The trajectory completed the task successfully using "
                    f"{len(steps)} recorded steps."
                ),
                "improvement_suggestion": (
                    "No critical correction required. Review trajectory length "
                    "for possible efficiency improvements."
                ),
            }

        if failure_type not in VALID_FAILURE_TYPES:
            failure_type = "unknown_failure"

        return {
            "task_id": trajectory["task_id"],
            "judge": self.name,
            "score": FAILURE_SCORE_MAP.get(failure_type, 1),
            "label": "fail",
            "failure_type": failure_type,
            "reasoning_summary": (
                f"The trajectory did not complete the task. "
                f"Recorded failure type: {failure_type}."
            ),
            "improvement_suggestion": self._suggest_improvement(failure_type),
        }

    @staticmethod
    def _score_successful_trajectory(trajectory: Dict[str, Any]) -> int:
        """Score successful trajectories from 3 to 5."""

        steps = trajectory.get("steps", [])
        expected_tools = set(trajectory.get("expected_tools", []))
        used_tools = {
            step.get("tool")
            for step in steps
            if step.get("tool")
        }

        if expected_tools and not expected_tools.issubset(used_tools):
            return 3

        if len(steps) > 8:
            return 4

        return 5

    @staticmethod
    def _suggest_improvement(failure_type: str) -> str:
        suggestions = {
            "retrieval_error": (
                "Improve query formulation, retrieval recall, and evidence selection."
            ),
            "tool_selection_error": (
                "Improve tool routing and add tool-selection validation."
            ),
            "tool_execution_error": (
                "Validate tool arguments and implement retry or recovery logic."
            ),
            "reasoning_error": (
                "Add explicit planning, intermediate checks, and decomposition."
            ),
            "context_loss": (
                "Preserve relevant state and summarize long-running context."
            ),
            "hallucination": (
                "Require evidence grounding and block unsupported final claims."
            ),
            "incomplete_execution": (
                "Add completion checks before allowing the agent to terminate."
            ),
            "verification_failure": (
                "Require explicit validation of outputs before final response."
            ),
            "recovery_failure": (
                "Add retry policies and alternate actions after tool failure."
            ),
            "unknown_failure": (
                "Add more detailed trajectory logging and failure annotations."
            ),
        }

        return suggestions.get(
            failure_type,
            "Inspect the trajectory and improve execution safeguards.",
        )

    @staticmethod
    def _validate_trajectory(trajectory: Dict[str, Any]) -> None:
        required_fields = {"task_id", "task", "success", "steps"}
        missing_fields = required_fields - trajectory.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Trajectory is missing required fields: {missing}")

        if not isinstance(trajectory["steps"], list):
            raise TypeError("trajectory['steps'] must be a list")


def rule_based_judge(trajectory: Dict[str, Any]) -> Dict[str, Any]:
    """Backward-compatible function wrapper."""

    return RuleBasedJudge().evaluate(trajectory)
