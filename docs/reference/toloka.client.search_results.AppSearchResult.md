# AppSearchResult
`toloka.client.search_results.AppSearchResult`

```
AppSearchResult(
    self,
    *,
    content: Optional[List[App]] = None,
    has_more: Optional[bool] = None
)
```

The list of found Apps and whether there is something else on the original request.


It's better to use TolokaClient.get_apps(),
which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**-**|<p>List of found Apps.</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
