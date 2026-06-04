import matplotlib.pyplot as plt


def plot_failure_breakdown(failure_dict):

    labels = list(failure_dict.keys())
    values = list(failure_dict.values())

    plt.figure(figsize=(6,4))

    plt.bar(labels, values)

    plt.title("Failure Breakdown")

    plt.savefig(
        "reports/failure_breakdown.png"
    )
