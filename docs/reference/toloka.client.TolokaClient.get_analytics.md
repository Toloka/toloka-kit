# get_analytics
`toloka.client.TolokaClient.get_analytics`

```
get_analytics(self, stats: List[AnalyticsRequest])
```

Sends analytics queries, for example, to estimate the percentage of completed tasks in the pool


Only pool analytics queries are available.
The values of different analytical metrics will be returned in the "details" field of the operation when it is
completed. See the example.
You can request up to 10 metrics at a time.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`stats`|**List\[[AnalyticsRequest](toloka.client.analytics_request.AnalyticsRequest.md)\]**|<p>Analytics queries list.</p>

* **Returns:**

  An operation that you can wait for to get the required statistics.

* **Return type:**

  [Operation](toloka.client.operations.Operation.md)

**Examples:**

How to get task completion percentage for one pool.

```python
from toloka.client.analytics_request import CompletionPercentagePoolAnalytics
operation = toloka_client.get_analytics([CompletionPercentagePoolAnalytics(subject_id=pool_id)])
operation = toloka_client.wait_operation(operation)
print(operation.details['value'][0]['result']['value'])
```
