# Agent Trajectory Analyzer V2

A trajectory-level evaluation framework for diagnosing planning,
retrieval, tool-use, grounding, verification, and recovery failures
in LLM agents.

## V2 Highlights

- Real LLM-as-Judge evaluation with structured outputs
- Deterministic offline judge for reproducible CI
- Pass/fail and failure-type agreement analysis
- Judge disagreement case inspection
- Confusion matrix and CSV artifact generation
- Benchmark tasks across tool use, retrieval, coding, and planning
- Automated Markdown reporting and failure visualization

## Benchmark Results

The current V2 benchmark evaluates **36 agent trajectories across 7 task categories**, covering coding, retrieval, planning, multi-step reasoning, tool use, verification, and recovery.

| Metric | Result |
|---|---:|
| Total Tasks | 36 |
| Success Rate | 44.44% |
| Average Trajectory Length | 2.50 |
| Tool Error Rate | 5.56% |
| Trajectory Score | 41.67 |
| Dominant Failure Mode | `verification_failure` |

### Judge Agreement

| Metric | Result |
|---|---:|
| Pass/Fail Agreement | 100.00% |
| Failure-Type Agreement | 100.00% |
| Mean Score Difference | 0.0556 |
| Disagreement Count | 0 |

The benchmark automatically generates detailed evaluation artifacts, including judge outputs, disagreement analysis, a confusion matrix, and failure-mode visualization.

![Failure breakdown](reports/failure_breakdown.png)

For the complete generated evaluation report, see [`reports/v2_report.md`](reports/v2_report.md).

## Why This Project Matters

Agent failures are often caused by intermediate execution decisions,
not only by the quality of the final answer.

A final answer may appear plausible even when the agent:

- selects the wrong tool;
- retrieves irrelevant evidence;
- loses important context;
- produces unsupported claims;
- fails to recover from a tool error;
- terminates without verifying completion.

This framework evaluates the complete execution trajectory and identifies the likely root cause of failure.

Evaluation Architecture
Agent Trajectory
       |
       +--------------------+
       |                    |
       v                    v
Rule-Based Judge      LLM-as-Judge
       |                    |
       +---------+----------+
                 |
                 v
       Agreement Analysis
                 |
       +---------+----------+
       |                    |
       v                    v
Failure Diagnosis    Disagreement Review
                 |
                 v
       Markdown + CSV Reports


## Features

- Analyze agent trajectories step by step
- Compute success rate
- Measure average trajectory length
- Track tool usage distribution
- Detect failure root causes
- Generate an evaluation report

## LLM-as-Judge

The framework supports two complementary evaluation modes:

| Evaluator | Description |
|---|---|
| Rule-Based Judge | Deterministic evaluator for reproducible local and CI runs |
| LLM-as-Judge | OpenAI model evaluator using structured Pydantic outputs |
| Offline Fallback | Deterministic approximation used when no API key is available |

## Example Trajectory

```json
{
  "task_id": "task_001",
  "task": "Find the top 3 competitors of OpenAI in AI coding assistants.",
  "success": true,
  "steps": [
    {
      "step": 1,
      "tool": "search",
      "input": "top AI coding assistant competitors",
      "output": "Found Cursor, Anthropic Claude Code, GitHub Copilot"
    },
    {
      "step": 2,
      "tool": "browser",
      "input": "Cursor AI website",
      "output": "Extracted product details"
    }
  ],
  "failure_reason": null
}

## How to Run

Clone repository

```bash
git clone https://github.com/Hanw-ai/Agent-Trajectory-Analyzer.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run analyzer

```bash
python demo.py
```
## Example Output

```text
Agent Trajectory Analyzer V2

{
  "total_tasks": 36,
  "success_rate": 0.4444,
  "avg_trajectory_length": 2.5,
  "tool_error_rate": 0.0556,
  "trajectory_score": 41.67,
  "dominant_failure_mode": "verification_failure",
  "agreement_metrics": {
    "total_evaluated": 36,
    "label_agreement_rate": 1.0,
    "failure_type_agreement_rate": 1.0,
    "mean_score_difference": 0.0556,
    "disagreement_count": 0
  }
}

Report generated: reports/v2_report.md
Judge results generated: reports/judge_results.csv
Disagreements generated: reports/disagreements.csv
Confusion matrix generated: reports/confusion_matrix.csv
Chart generated: reports/failure_breakdown.png
```

## Current Version

- V1: Trajectory metrics and failure analysis
- V2: LLM-as-Judge and judge agreement


## Root Cause Analysis

The analyzer identifies the dominant failure mode across failed agent trajectories.

This helps diagnose whether an agent primarily fails because of:

- Poor retrieval
- Incorrect tool routing
- Unsupported generation
- Reasoning failure
- Recovery failure

This is useful for debugging agentic systems such as coding agents, research agents, browser agents, and tool-using assistants.

  ## Repository Structure

```text
Agent-Trajectory-Analyzer/
├── data/
│   ├── sample_trajectories.json
│   └── trajectories_v2.json
├── reports/
│   ├── evaluation_report.md
│   ├── judge_results.csv
│   ├── disagreements.csv
│   ├── confusion_matrix.csv
│   └── failure_breakdown.png
├── src/
│   ├── analyzer.py
│   ├── judges.py
│   ├── llm_judge.py
│   ├── judge_agreement.py
│   ├── metrics.py
│   ├── report.py
│   └── visualization.py
├── test/
├── demo.py
├── requirements.txt
└── README.md
