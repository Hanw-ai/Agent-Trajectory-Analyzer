"""LLM-as-Judge implementation for evaluating agent trajectories."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field


class JudgeOutput(BaseModel):
    """Structured output returned by the LLM judge."""

    score: int = Field(ge=1, le=5)
    label: Literal["pass", "fail"]
    failure_type: Literal[
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
    ]
    reasoning_summary: str
    improvement_suggestion: str


SYSTEM_PROMPT = """
You are an expert evaluator of tool-using LLM agents.

Evaluate the full trajectory, not only the final answer.

Use the following criteria:

1. Task completion
2. Planning quality
3. Tool selection
4. Tool execution
5. Evidence grounding
6. Context retention
7. Verification and recovery
8. Execution efficiency

Score rubric:
5 = Correct, grounded, efficient, and fully completed
4 = Successful with minor inefficiency or weakness
3 = Partially successful or weakly verified
2 = Major failure, but some useful progress
1 = Fundamentally incorrect, unsupported, or incomplete

Allowed failure types:
- success
- retrieval_error
- tool_selection_error
- tool_execution_error
- reasoning_error
- context_loss
- hallucination
- incomplete_execution
- verification_failure
- recovery_failure
- unknown_failure

Return a concise assessment.
Do not trust the trajectory's existing success or failure label blindly.
Judge from the task, steps, tool outputs, and final answer.
""".strip()


class LLMJudge:
    """Evaluate trajectories with an OpenAI model or deterministic fallback."""

    name = "llm_judge"

    def __init__(
        self,
        model: str | None = None,
        use_fallback: bool = True,
    ) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.use_fallback = use_fallback
        self.api_key = os.getenv("OPENAI_API_KEY")

    def evaluate(self, trajectory: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            if not self.use_fallback:
                raise RuntimeError(
                    "OPENAI_API_KEY is not set and fallback mode is disabled."
                )

            return self._fallback_evaluate(trajectory)

        try:
            result = self._evaluate_with_model(trajectory)
        except Exception as exc:
            if not self.use_fallback:
                raise

            result = self._fallback_evaluate(trajectory)
            result["reasoning_summary"] = (
                f"{result['reasoning_summary']} "
                f"Fallback used after model error: {type(exc).__name__}."
            )

        return result

    def _evaluate_with_model(
        self,
        trajectory: Dict[str, Any],
    ) -> Dict[str, Any]:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)

        response = client.responses.parse(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=json.dumps(
                trajectory,
                ensure_ascii=False,
                indent=2,
            ),
            text_format=JudgeOutput,
        )

        parsed = response.output_parsed

        if parsed is None:
            raise ValueError("LLM judge returned no parsed output.")

        result = parsed.model_dump()
        result["task_id"] = trajectory["task_id"]
        result["judge"] = self.name
        result["evaluation_mode"] = "model"

        return result

    def _fallback_evaluate(
        self,
        trajectory: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Deterministic offline approximation used for CI and demos."""

        success = bool(trajectory.get("success", False))
        failure_type = trajectory.get("failure_reason") or "unknown_failure"
        steps = trajectory.get("steps", [])
        final_answer = str(trajectory.get("final_answer", "")).strip()

        if success:
            if not final_answer:
                return self._build_result(
                    trajectory=trajectory,
                    score=3,
                    label="fail",
                    failure_type="verification_failure",
                    reasoning_summary=(
                        "The trajectory is marked successful, but no final answer "
                        "was recorded for verification."
                    ),
                    improvement_suggestion=(
                        "Store and verify the final answer before marking success."
                    ),
                )

            score = 5 if len(steps) <= 6 else 4

            return self._build_result(
                trajectory=trajectory,
                score=score,
                label="pass",
                failure_type="success",
                reasoning_summary=(
                    "The offline judge found a completed trajectory with a "
                    "recorded final answer."
                ),
                improvement_suggestion=(
                    "Retain explicit evidence and verification signals."
                ),
            )

        valid_failure_types = {
            "retrieval_error",
            "tool_selection_error",
            "tool_execution_error",
            "reasoning_error",
            "context_loss",
            "hallucination",
            "incomplete_execution",
            "verification_failure",
            "recovery_failure",
        }

        if failure_type not in valid_failure_types:
            failure_type = "unknown_failure"

        score = 1 if failure_type in {
            "hallucination",
            "context_loss",
        } else 2

        return self._build_result(
            trajectory=trajectory,
            score=score,
            label="fail",
            failure_type=failure_type,
            reasoning_summary=(
                f"The trajectory failed with the primary issue "
                f"'{failure_type}'."
            ),
            improvement_suggestion=self._fallback_suggestion(failure_type),
        )

    def _build_result(
        self,
        trajectory: Dict[str, Any],
        score: int,
        label: str,
        failure_type: str,
        reasoning_summary: str,
        improvement_suggestion: str,
    ) -> Dict[str, Any]:
        return {
            "task_id": trajectory["task_id"],
            "judge": self.name,
            "score": score,
            "label": label,
            "failure_type": failure_type,
            "reasoning_summary": reasoning_summary,
            "improvement_suggestion": improvement_suggestion,
            "evaluation_mode": "fallback",
        }

    @staticmethod
    def _fallback_suggestion(failure_type: str) -> str:
        suggestions = {
            "retrieval_error": "Improve query formulation and retrieval recall.",
            "tool_selection_error": "Improve tool routing and tool descriptions.",
            "tool_execution_error": "Validate tool arguments and retry failed calls.",
            "reasoning_error": "Use explicit planning and intermediate checks.",
            "context_loss": "Preserve relevant state across trajectory steps.",
            "hallucination": "Require evidence before generating final claims.",
            "incomplete_execution": "Add task-completion validation.",
            "verification_failure": "Verify outputs before finalizing the task.",
            "recovery_failure": "Add retry and alternative-action policies.",
            "unknown_failure": "Add richer logs and failure annotations.",
        }

        return suggestions[failure_type]


def llm_based_judge(
    trajectory: Dict[str, Any],
    model: str | None = None,
) -> Dict[str, Any]:
    """Convenience wrapper for evaluating one trajectory."""

    return LLMJudge(model=model).evaluate(trajectory)
