# Chart
`toloka.metrics.jupyter_dashboard.Chart` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/metrics/jupyter_dashboard.py#L44)

```python
Chart(
    self,
    name: Optional[str],
    metrics: List[BaseMetric],
    loop=None
)
```

One chart on the dashboard. Could include several metrics.


If you want to draw really cool chart that displays several metrics in the same coordinates.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`name`|**Optional\[str\]**|<p>The header for this chart. Could be None, Chart create name from the first metric.</p>
`metrics`|**List\[[BaseMetric](toloka.metrics.metrics.BaseMetric.md)\]**|<p>List of metrics, that will be displayed on this chart (in the same coordinates).</p>

**Examples:**

How to display all submitted and accepted answers from some pool and its checking pool, in one chart.

```python
Chart(
    'Answers count',
    [
)
```
## Methods Summary

| Method | Description |
| :------| :-----------|
[create_async_tasks](toloka.metrics.jupyter_dashboard.Chart.create_async_tasks.md)| None
[create_figure](toloka.metrics.jupyter_dashboard.Chart.create_figure.md)| Create figure for this chart. Called at each step.
[update_metrics](toloka.metrics.jupyter_dashboard.Chart.update_metrics.md)| Gathers all metrics, and stores them in lines.
