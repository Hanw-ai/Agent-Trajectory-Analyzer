from src.analyzer import TrajectoryAnalyzer
from src.report import generate_markdown_report


def main():
    analyzer = TrajectoryAnalyzer("data/sample_trajectories.json")
    results = analyzer.analyze()

    print("Agent Trajectory Analysis Results")
    print(results)

    generate_markdown_report(
        results,
        "reports/evaluation_report.md"
    )

    print("Report generated: reports/evaluation_report.md")


if __name__ == "__main__":
    main()
