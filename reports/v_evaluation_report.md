
# Agent Trajectory Evaluation Report

## Summary

| Metric | Value |
|----------|----------|
| Total Tasks | 5 |
| Success Rate | 40% |
| Average Trajectory Length | 2.4 |
| Tool Error Rate | 20% |

## Tool Usage

- search: 3
- browser: 4
- summarizer: 5

## Failure Breakdown

- retrieval_error: 1
- tool_selection_error: 1
- hallucination: 1

## Root Cause Analysis

The majority of failures originate from:

1. Retrieval failures
2. Incorrect tool selection
3. Hallucinated outputs

Future improvements:

- Better retrieval ranking
- Tool routing optimization
- Verification and self-correction
