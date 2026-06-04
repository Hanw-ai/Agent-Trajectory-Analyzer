def rule_based_judge(trajectory):
    if trajectory["success"]:
        return {
            "judge": "rule_based",
            "score": 1.0,
            "label": "pass",
            "reason": "Task completed successfully."
        }

    failure_reason = trajectory.get("failure_reason")

    if failure_reason == "hallucination":
        score = 0.1
    elif failure_reason == "retrieval_error":
        score = 0.3
    elif failure_reason == "tool_selection_error":
        score = 0.4
    elif failure_reason == "reasoning_error":
        score = 0.5
    else:
        score = 0.2

    return {
        "judge": "rule_based",
        "score": score,
        "label": "fail",
        "reason": f"Detected failure mode: {failure_reason}"
    }


def llm_based_judge_simulated(trajectory):
    """
    Simulated LLM-as-Judge.

    In a production setting, this function can be replaced with an API call
    to an LLM judge that evaluates trajectory quality, tool use, and final answer grounding.
    """

    steps = trajectory["steps"]
    failure_reason = trajectory.get("failure_reason")

    if trajectory["success"] and len(steps) <= 3:
        score = 0.9
        label = "pass"
        reason = "Efficient successful trajectory with appropriate tool use."
    elif failure_reason == "hallucination":
        score = 0.2
        label = "fail"
        reason = "Output appears unsupported by retrieved evidence."
    elif failure_reason == "retrieval_error":
        score = 0.35
        label = "fail"
        reason = "Trajectory failed because relevant information was not retrieved."
    elif failure_reason == "tool_selection_error":
        score = 0.45
        label = "fail"
        reason = "Agent selected a suboptimal tool for the task."
    else:
        score = 0.5
        label = "fail"
        reason = "Trajectory shows incomplete or unreliable task execution."

    return {
        "judge": "llm_based_simulated",
        "score": score,
        "label": label,
        "reason": reason
    }


def compute_judge_agreement(trajectories):
    agreements = 0
    total = len(trajectories)

    for trajectory in trajectories:
        rule_result = rule_based_judge(trajectory)
        llm_result = llm_based_judge_simulated(trajectory)

        if rule_result["label"] == llm_result["label"]:
            agreements += 1

    return agreements / total if total else 0


def evaluate_with_judges(trajectories):
    judged_results = []

    for trajectory in trajectories:
        judged_results.append({
            "task_id": trajectory["task_id"],
            "rule_based_judge": rule_based_judge(trajectory),
            "llm_based_judge": llm_based_judge_simulated(trajectory),
        })

    return judged_results
