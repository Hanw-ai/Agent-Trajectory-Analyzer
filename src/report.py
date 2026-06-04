def generate_markdown_report(results, output_path):
    report = f"""# Agent Trajectory Evaluation Report

## Summary

| Metric | Value |
|---|---:|
| Total Tasks | {results["total_tasks"]} |
| Success Rate | {results["success_rate"]:.2%} |
| Average Trajectory Length | {results["avg_trajectory_length"]:.2f} |
| Tool Error Rate | {results["tool_error_rate"]:.2%} |

## Tool Usage

"""

    for tool, count in results["tool_usage"].items():
        report += f"- {tool}: {count}\n"

    report += "\n## Failure Breakdown\n\n"

    for reason, count in results["failure_breakdown"].items():
        report += f"- {reason}: {count}\n"

    report += """

## Interpretation

The framework analyzes agent behavior across tool-use trajectories. It identifies whether failures are caused by retrieval errors, tool selection errors, hallucination, or other reasoning issues.

This type of analysis is useful for debugging LLM agents, improving tool routing, and evaluating production agent reliability.
"""

    with open(output_path, "w") as file:
        file.write(report)
