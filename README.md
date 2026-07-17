# Agent Trajectory Analyzer V2
A trajectory-level evaluation framework for diagnosing planning, retrieval, tool-use, grounding, verification, and recovery failures in LLM agents.
V2 Highlights
	•	Real LLM-as-Judge evaluation with structured outputs
	•	Deterministic offline judge for reproducible CI
	•	Pass/fail and failure-type agreement analysis
	•	Judge disagreement case inspection
	•	Confusion matrix and CSV artifact generation
	•	Expanded benchmark across tool use, retrieval, coding, planning, and multi-step reasoning
	•	Automated Markdown reporting and failure visualization
Why This Project Matters
Agent failures are often caused by intermediate execution decisions rather than final-answer fluency.
A final answer may appear plausible even when the agent:
	•	selected the wrong tool,
	•	retrieved irrelevant evidence,
	•	lost important context,
	•	hallucinated an unsupported action,
	•	failed to recover from a tool error, or
	•	terminated without verifying completion.
This framework evaluates the full agent trajectory and identifies the likely root cause of failure.
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


## Why This Project Matters

Modern LLM agents often fail not because the final answer is poorly written, but because the intermediate trajectory is flawed.

Common failure modes include:

- Retrieval error
- Tool selection error
- Reasoning error
- Hallucination
- Overlong trajectory
- Failure to recover from bad tool outputs

This framework analyzes those failures from agent traces.

## Features

- Analyze agent trajectories step by step
- Compute success rate
- Measure average trajectory length
- Track tool usage distribution
- Detect failure root causes
- Generate an evaluation report

## LLM-as-Judge

The framework supports both:

- Rule-Based Judge
- Simulated LLM-as-Judge

Judge agreement is measured to evaluate consistency between deterministic evaluation and model-based evaluation.

This mirrors evaluation workflows commonly used in modern agent systems.

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
Agent Trajectory Analysis Results

{
  'total_tasks': 5,
  'success_rate': 0.4,
  'avg_trajectory_length': 2.4,
  'tool_usage': {
      'search': 3,
      'browser': 4,
      'summarizer': 5
  },
  'failure_breakdown': {
      'retrieval_error': 1,
      'tool_selection_error': 1,
      'hallucination': 1
  },
  'tool_error_rate': 0.2,

  'judge_agreement': 1.0,
  'judge_results': [...]
}

Report generated:
reports/evaluation_report.md
```

## Current Version

- V1: Trajectory metrics and failure analysis
- V2: LLM-as-Judge and judge agreement




## Failure Analysis

![Failure Breakdown](reports/failure_breakdown.png)

## Root Cause Analysis

The analyzer identifies the dominant failure mode across failed agent trajectories.

This helps diagnose whether an agent primarily fails because of:

- Poor retrieval
- Incorrect tool routing
- Unsupported generation
- Reasoning failure
- Recovery failure

This is useful for debugging agentic systems such as coding agents, research agents, browser agents, and tool-using assistants.

## V2: LLM-as-Judge + Judge Agreement

This project includes two judge types:

| Judge | Description |
|---|---|
| Rule-Based Judge | Uses explicit failure labels and success signals |
| Simulated LLM-as-Judge | Evaluates trajectory quality, tool use, and grounding behavior |

The framework computes judge agreement to measure consistency between deterministic rules and LLM-style evaluation.

This mirrors common evaluation workflows for agentic systems, where model outputs are assessed using both programmatic checks and LLM-based evaluators.
