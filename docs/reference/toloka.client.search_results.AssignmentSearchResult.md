# AssignmentSearchResult
`toloka.client.search_results.AssignmentSearchResult`

```
AssignmentSearchResult(
    self,
    *,
    items: Optional[List[Assignment]] = None,
    has_more: Optional[bool] = None
)
```

The list of found assignments and whether there is something else on the original request


It's better to use TolokaClient.get_assignments(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[Assignment](toloka.client.assignment.Assignment.md)\]\]**|<p>List of found assignments</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
