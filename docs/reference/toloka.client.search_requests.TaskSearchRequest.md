# TaskSearchRequest
`toloka.client.search_requests.TaskSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/search_requests.py#L523)

```python
TaskSearchRequest(
    self,
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

Parameters for searching tasks

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**Optional\[str\]**|<p>ID of the pool to get tasks from.</p>
`overlap`|**Optional\[int\]**|<p>Tasks with an overlap equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>Tasks with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Tasks with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Tasks with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Tasks with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Tasks created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Tasks created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Tasks created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Tasks created after or on the specified date.</p>
`overlap_lt`|**Optional\[int\]**|<p>Tasks with an overlap less than the specified value.</p>
`overlap_lte`|**Optional\[int\]**|<p>Tasks with an overlap equal to the specified value.</p>
`overlap_gt`|**Optional\[int\]**|<p>Tasks with an overlap greater than the specified value.</p>
`overlap_gte`|**Optional\[int\]**|<p>Tasks with an overlap equal to the specified value.</p>
