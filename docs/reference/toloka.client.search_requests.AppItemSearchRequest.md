# AppItemSearchRequest
`toloka.client.search_requests.AppItemSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/search_requests.py#L1065)

```python
AppItemSearchRequest(
    self,
    after_id: Optional[str] = None,
    batch_id: Optional[str] = None,
    status: Optional[AppItem.Status] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_at_lt: Optional[datetime] = None,
    created_at_lte: Optional[datetime] = None,
    created_at_gt: Optional[datetime] = None,
    created_at_gte: Optional[datetime] = None
)
```

Parameters for searching App items.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`after_id`|**Optional\[str\]**|<p>ID of the item used for cursor pagination.</p>
`batch_id`|**Optional\[str\]**|<p>Batch ID.</p>
`status`|**Optional\[[AppItem.Status](toloka.client.app.AppItem.Status.md)\]**|<p>items in this status.</p>
`id_gt`|**Optional\[str\]**|<p>items with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>items with an ID greater than or equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>items with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>items with an ID less than or equal to the specified value.</p>
`created_gt`|**-**|<p>items created after the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_gte`|**-**|<p>items created after the specified date, inclusive. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lt`|**-**|<p>items created before the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lte`|**-**|<p>items created before the specified date, inclusive. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
