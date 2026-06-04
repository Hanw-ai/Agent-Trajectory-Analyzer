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
