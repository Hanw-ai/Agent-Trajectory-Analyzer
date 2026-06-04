from src.analyzer import TrajectoryAnalyzer
from src.report import generate_markdown_report
from src.visualization import plot_failure_breakdown


def main():
    analyzer = TrajectoryAnalyzer("data/sample_trajectories.json")
    results = analyzer.analyze()

    print("Agent Trajectory Analysis Results")
    print(results)

    generate_markdown_report(
        results,
        "reports/evaluation_report.md"
    )

    plot_failure_breakdown(
        results["failure_breakdown"]
    )

    print("Report generated: reports/evaluation_report.md")
    print("Chart generated: reports/failure_breakdown.png")


if __name__ == "__main__":
    main()
