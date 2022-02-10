# AppSearchRequest
`toloka.client.search_requests.AppSearchRequest`

```python
AppSearchRequest(
    self,
    after_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    name_lt: Optional[str] = None,
    name_lte: Optional[str] = None,
    name_gt: Optional[str] = None,
    name_gte: Optional[str] = None
)
```

Parameters for searching Apps.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`after_id`|**Optional\[str\]**|<p>The ID of the App used for cursor pagination.</p>
`id_gt`|**Optional\[str\]**|<p>only with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>only with an ID greater than or equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>only with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>only with an ID less than or equal to the specified value.</p>
`name_gt`|**Optional\[str\]**|<p>only with a name lexicographically greater than the specified value.</p>
`name_gte`|**Optional\[str\]**|<p>only with a name lexicographically greater than or equal to the specified value.</p>
`name_lt`|**Optional\[str\]**|<p>only with a name lexicographically less than the specified value.</p>
`name_lte`|**Optional\[str\]**|<p>only with a name lexicographically less than or equal to the specified value.</p>
