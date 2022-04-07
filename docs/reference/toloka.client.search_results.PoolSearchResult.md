# PoolSearchResult
`toloka.client.search_results.PoolSearchResult`

```python
PoolSearchResult(
    self,
    *,
    items: Optional[List[Pool]] = None,
    has_more: Optional[bool] = None
)
```

The list of found pools and whether there is something else on the original request


It's better to use TolokaClient.get_pools(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[Pool](toloka.client.pool.Pool.md)\]\]**|<p>List of found pools</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
