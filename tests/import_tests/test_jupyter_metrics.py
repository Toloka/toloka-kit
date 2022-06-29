def test_jupyter_metrics_imported():
    from toloka.metrics import jupyter_dashboard
    assert jupyter_dashboard.DashBoard
    assert jupyter_dashboard.Chart
