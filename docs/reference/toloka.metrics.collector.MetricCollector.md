# MetricCollector
`toloka.metrics.collector.MetricCollector`

```
MetricCollector(self, metrics: List[BaseMetric])
```

Gather metrics


**Examples:**

How to gather metrics and sends it to zabbix:

```python
import toloka.client as toloka
from toloka.metrics import AssignmentsInPool, Balance, bind_client, MetricCollector
toloka_client = toloka.TolokaClient(auth_token, 'PRODUCTION')
collector = MetricCollector(
    [
        Balance(),
        AssignmentsInPool(pool_id),
    ],
)
bind_client(collector.metrics, toloka_client)
while True:
    metric_dict = collector.get_lines()
    send_metric_to_zabbix(metric_dict)
    sleep(10)
```
## Methods summary

| Method | Description |
| :------| :-----------|
[get_lines](toloka.metrics.collector.MetricCollector.get_lines.md)| None
