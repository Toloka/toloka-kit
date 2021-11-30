# AggregatedSolutionSearchRequest
`toloka.client.search_requests.AggregatedSolutionSearchRequest`

```
AggregatedSolutionSearchRequest(
    self,
    task_id_lt: Optional[str] = None,
    task_id_lte: Optional[str] = None,
    task_id_gt: Optional[str] = None,
    task_id_gte: Optional[str] = None
)
```

Parameters for searching aggregated solution

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id_lt`|**Optional\[str\]**|<p>Jobs with an ID greater than the specified value.</p>
`task_id_lte`|**Optional\[str\]**|<p>Jobs with an ID greater than or equal to the specified value.</p>
`task_id_gt`|**Optional\[str\]**|<p>Jobs with an ID less than the specified value.</p>
`task_id_gte`|**Optional\[str\]**|<p>Jobs with an ID less than or equal to the specified value.</p>
