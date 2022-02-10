# AppBatchSearchRequest
`toloka.client.search_requests.AppBatchSearchRequest`

```python
AppBatchSearchRequest(
    self,
    after_id: Optional[str] = None,
    status: Optional[AppBatch.Status] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    name_lt: Optional[str] = None,
    name_lte: Optional[str] = None,
    name_gt: Optional[str] = None,
    name_gte: Optional[str] = None,
    created_at_lt: Optional[datetime] = None,
    created_at_lte: Optional[datetime] = None,
    created_at_gt: Optional[datetime] = None,
    created_at_gte: Optional[datetime] = None
)
```

Parameters for searching batches in the App project.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`after_id`|**Optional\[str\]**|<p>ID of the batch used for cursor pagination</p>
`status`|**Optional\[[AppBatch.Status](toloka.client.app.AppBatch.Status.md)\]**|<p>batches with this status.</p>
`id_gt`|**Optional\[str\]**|<p>batches with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>batches with an ID greater than or equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>batches with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>batches with an ID less than or equal to the specified value.</p>
`name_gt`|**Optional\[str\]**|<p>batches with the name lexicographically greater than the specified value.</p>
`name_gte`|**Optional\[str\]**|<p>batches with a name lexicographically greater than or equal to the specified value.</p>
`name_lt`|**Optional\[str\]**|<p>batches with a name lexicographically less than the specified value.</p>
`name_lte`|**Optional\[str\]**|<p>batches with a name lexicographically less than or equal to the specified value.</p>
`created_gt`|**-**|<p>batches created after the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_gte`|**-**|<p>batches created after the specified date, inclusive. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lt`|**-**|<p>batches created before the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lte`|**-**|<p>batches created before the specified date, inclusive. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
