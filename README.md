# Agent Trajectory Analyzer

Agent Trajectory Analyzer is an evaluation framework for analyzing LLM agent trajectories, tool-use behavior, and failure root causes.

This project is designed for agentic AI systems where an LLM uses external tools such as search, browser, calculator, retriever, or code execution.

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
  'tool_error_rate': 0.2
}

Report generated:
reports/evaluation_report.md
```

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
