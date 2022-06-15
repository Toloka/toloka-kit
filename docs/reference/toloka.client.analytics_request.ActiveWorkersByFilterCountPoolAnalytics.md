# ActiveWorkersByFilterCountPoolAnalytics
`toloka.client.analytics_request.ActiveWorkersByFilterCountPoolAnalytics` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/analytics_request.py#L147)

```python
ActiveWorkersByFilterCountPoolAnalytics(
    self,
    *,
    subject_id: str,
    interval_hours: int
)
```

The number of active performers matching the pool filters for the last hours

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`subject_id`|**str**|<p>ID of the object you want to get analytics about.</p>
`interval_hours`|**int**|<p>The number of hours to take into account when collecting statistics.</p>
