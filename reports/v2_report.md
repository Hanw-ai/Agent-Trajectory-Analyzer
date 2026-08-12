# Agent Trajectory Evaluation Report

## Executive Summary

Evaluated **36** agent trajectories across task completion, tool use, failure modes, and evaluator agreement.

## Core Metrics

| Metric | Value |
|---|---:|
| Total Tasks | 36 |
| Success Rate | 44.44% |
| Average Trajectory Length | 2.50 |
| Tool Error Rate | 5.56% |
| Trajectory Score | 41.67 |
| Dominant Failure Mode | verification_failure |

## Judge Agreement

| Metric | Value |
|---|---:|
| Pass/Fail Agreement | 100.00% |
| Failure-Type Agreement | 100.00% |
| Mean Score Difference | 0.06 |
| Disagreement Count | 0 |

## Tool Usage

- `calculator`: 6
- `code_editor`: 8
- `file_reader`: 12
- `retriever`: 11
- `test_runner`: 6

## Failure Breakdown

- `context_loss`: 2
- `hallucination`: 3
- `incomplete_execution`: 2
- `planning_error`: 2
- `reasoning_error`: 2
- `recovery_failure`: 2
- `retrieval_error`: 2
- `tool_execution_error`: 1
- `tool_selection_error`: 1
- `verification_failure`: 3

## Judge Disagreement Patterns

- No judge disagreements detected.

## Artifact Files

- `reports/judge_results.csv`
- `reports/disagreements.csv`
- `reports/confusion_matrix.csv`
- `reports/failure_breakdown.png`

## Interpretation

The framework compares deterministic evaluation with an LLM-based evaluator to identify both agent failures and evaluator uncertainty.

Disagreement cases should be manually reviewed because they may reveal ambiguous task definitions, weak ground-truth labels, or insufficient trajectory evidence.