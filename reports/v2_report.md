# Agent Trajectory Evaluation Report

## Executive Summary

Evaluated **10** agent trajectories across task completion, tool use, failure modes, and evaluator agreement.

## Core Metrics

| Metric | Value |
|---|---:|
| Total Tasks | 10 |
| Success Rate | 40.00% |
| Average Trajectory Length | 2.50 |
| Tool Error Rate | 10.00% |
| Trajectory Score | 35.00 |
| Dominant Failure Mode | tool_selection_error |

## Judge Agreement

| Metric | Value |
|---|---:|
| Pass/Fail Agreement | 100.00% |
| Failure-Type Agreement | 100.00% |
| Mean Score Difference | 0.00 |
| Disagreement Count | 0 |

## Tool Usage

- `calculator`: 2
- `code_editor`: 2
- `file_reader`: 3
- `retriever`: 3
- `test_runner`: 1

## Failure Breakdown

- `context_loss`: 1
- `hallucination`: 1
- `incomplete_execution`: 1
- `retrieval_error`: 1
- `tool_selection_error`: 1
- `verification_failure`: 1

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