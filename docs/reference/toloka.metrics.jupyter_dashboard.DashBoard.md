# DashBoard
`toloka.metrics.jupyter_dashboard.DashBoard` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/metrics/jupyter_dashboard.py#L174)

```python
DashBoard(
    self,
    metrics: List[Union[BaseMetric, Chart]],
    header: str = 'Toloka metrics dashboard',
    update_seconds: int = 10,
    min_time_range: timedelta = ...,
    max_time_range: timedelta = ...
)
```

Toloka dashboard with metrics. Only for jupyter.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`metrics`|**List\[Union\[[BaseMetric](toloka.metrics.metrics.BaseMetric.md), [Chart](toloka.metrics.jupyter_dashboard.Chart.md)\]\]**|<p>List of metrics or charts, that will be displayed on the dashboard. Each element will be displayed in a separate chart (coordinates). If you want to draw several metrics in one coordinates, wrap it into an instance of the class Chart.</p>
`header`|**str**|<p>Your pretty header for this dashboard.</p>
`update_seconds`|**int**|<p>Count of seconds between dash updates.</p>
`min_time_range`|**timedelta**|<p>The minimum time range for all charts.</p>
`max_time_range`|**timedelta**|<p>The maximum time range for all charts. If you have more data, you will see only the last range on charts.</p>

**Examples:**

How to create online dashboard in jupyter.

```python
import toloka.metrics as metrics
from toloka.metrics.jupyter_dashboard import Chart, DashBoard
import toloka.client as toloka
toloka_client = toloka.TolokaClient(oauth_token, 'PRODUCTION')
new_dash = DashBoard(
    [
        metrics.Balance(),
        metrics.AssignmentsInPool('123'),
        metrics.AssignmentEventsInPool('123', submitted_name='submitted', join_events=True),
        Chart(
            'Manualy configured chart',
            [metrics.AssignmentsInPool('123'), metrics.AssignmentsInPool('345'),]
        )
    ],
    header='My cool dash',
)
metrics.bind_client(new_dash.metrics, toloka_client)
new_dash.run_dash()
new_dash.stop_dash()
```
## Methods Summary

| Method | Description |
| :------| :-----------|
[run_dash](toloka.metrics.jupyter_dashboard.DashBoard.run_dash.md)| Starts dashboard. Starts server for online updating charts.
[stop_dash](toloka.metrics.jupyter_dashboard.DashBoard.stop_dash.md)| Stops server. And stops updating dashboard.
[update_charts](toloka.metrics.jupyter_dashboard.DashBoard.update_charts.md)| Redraws all charts on each iteration
