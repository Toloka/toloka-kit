# ProjectSearchResult
`toloka.client.search_results.ProjectSearchResult`

```
ProjectSearchResult(
    self,
    *,
    items: Optional[List[Project]] = None,
    has_more: Optional[bool] = None
)
```

The list of found projects and whether there is something else on the original request


It's better to use TolokaClient.get_projects(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[Project](toloka.client.project.Project.md)\]\]**|<p>List of found projects</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
