# TaskSuiteSearchRequest
`toloka.client.search_requests.TaskSuiteSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/search_requests.py#L575)

```python
TaskSuiteSearchRequest(
    self,
    task_id: Optional[str] = None,
    pool_id: Optional[str] = None,
    overlap: Optional[int] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None,
    overlap_lt: Optional[int] = None,
    overlap_lte: Optional[int] = None,
    overlap_gt: Optional[int] = None,
    overlap_gte: Optional[int] = None
)
```

Parameters for searching task suites

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**Optional\[str\]**|<p>The task ID in suites generated automatically using &quot;smart mixing&quot;. You will get task suites that contain the specified task.</p>
`pool_id`|**Optional\[str\]**|<p>ID of the pool to get task suites from.</p>
`overlap`|**Optional\[int\]**|<p>Suites with an overlap equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>Task suites with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Task suites with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Task suites with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Task suites with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Task suites created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Task suites created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Task suites created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Task suites created after or on the specified date.</p>
`overlap_lt`|**Optional\[int\]**|<p>Suites with an overlap less than the specified value.</p>
`overlap_lte`|**Optional\[int\]**|<p>Suites with an overlap less than or equal to the specified value.</p>
`overlap_gt`|**Optional\[int\]**|<p>Suites with an overlap greater than the specified value.</p>
`overlap_gte`|**Optional\[int\]**|<p>Suites with an overlap greater than or equal to the specified value.</p>
