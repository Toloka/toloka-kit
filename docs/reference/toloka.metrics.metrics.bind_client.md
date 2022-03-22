# bind_client
`toloka.metrics.metrics.bind_client` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/metrics/metrics.py#L34)

```python
bind_client(metrics: List[BaseMetric], toloka_client: TolokaClient)
```

Sets/updates toloka_client for all metrics in list.


**Examples:**

How to bind same client for all metrics:
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
```

How to bind several clients:
```python
metrics_1 = bind_client([Balance(), AssignmentsInPool(pool_id_1)], toloka_client_1)
metrics_2 = bind_client([Balance(), AssignmentsInPool(pool_id_2)], toloka_client_2)
collector = MetricCollector(metrics_1 + metrics_2)
```
