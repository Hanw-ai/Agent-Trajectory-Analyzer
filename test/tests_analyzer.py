from src.analyzer import TrajectoryAnalyzer


def test_analyzer_runs_offline():
    analyzer = TrajectoryAnalyzer(
        "data/trajectories_v2.json"
    )

    results = analyzer.analyze(
        export_csv=False
    )

    assert results["total_tasks"] > 0
    assert 0.0 <= results["success_rate"] <= 1.0
    assert "agreement_metrics" in results
    assert "judge_results" in results
