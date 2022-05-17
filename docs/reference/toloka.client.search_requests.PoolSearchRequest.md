# PoolSearchRequest
`toloka.client.search_requests.PoolSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/search_requests.py#L224)

```python
PoolSearchRequest(
    self,
    status: Optional[Pool.Status] = None,
    project_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None,
    last_started_lt: Optional[datetime] = None,
    last_started_lte: Optional[datetime] = None,
    last_started_gt: Optional[datetime] = None,
    last_started_gte: Optional[datetime] = None
)
```

Parameters for searching pools

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status`|**Optional\[[Pool.Status](toloka.client.pool.Pool.Status.md)\]**|<p>Pool status<ul><li>OPEN</li><li>CLOSED</li><li>ARCHIVED</li><li>LOCKED</li></ul></p>
`project_id`|**Optional\[str\]**|<p>ID of the project to which the pool is attached.</p>
`id_lt`|**Optional\[str\]**|<p>Pools with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Pools with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Pools with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Pools with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Pools created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Pools created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Pools created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Pools created after or on the specified date.</p>
`last_started_lt`|**Optional\[datetime\]**|<p>Pools that were last opened before the specified date.</p>
`last_started_lte`|**Optional\[datetime\]**|<p>Pools that were last opened on or before the specified date.</p>
`last_started_gt`|**Optional\[datetime\]**|<p>Pools that were last opened after the specified date.</p>
`last_started_gte`|**Optional\[datetime\]**|<p>Pools that were last opened on or after the specified date.</p>
