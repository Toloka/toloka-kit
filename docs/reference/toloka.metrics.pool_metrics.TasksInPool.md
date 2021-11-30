# TasksInPool
`toloka.metrics.pool_metrics.TasksInPool`

```
TasksInPool(
    self,
    pool_id: str,
    tasks_name: Optional[str] = None,
    *,
    toloka_client: TolokaClient = None,
    timeout: timedelta = ...
)
```

The number of tasks in the pool. Not new tasks. All tasks on each step.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>From which pool track metrics.</p>
`tasks_name`|**Optional\[str\]**|<p>Metric name for a count of tasks.</p>

**Examples:**

How to collect this metrics:
```python
def print_metric(metric_dict):
    print(metric_dict)
collector = MetricCollector([TasksInPool(pool_id, toloka_client=toloka_client)], print_metric)
asyncio.run(collector.run())
```
## Methods summary

| Method | Description |
| :------| :-----------|
[get_line_names](toloka.metrics.pool_metrics.TasksInPool.get_line_names.md)| Returns a list of metric names that can be generated by this class instance.