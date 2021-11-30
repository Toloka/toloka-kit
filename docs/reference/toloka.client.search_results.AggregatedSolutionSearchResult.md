# AggregatedSolutionSearchResult
`toloka.client.search_results.AggregatedSolutionSearchResult`

```
AggregatedSolutionSearchResult(
    self,
    *,
    items: Optional[List[AggregatedSolution]] = None,
    has_more: Optional[bool] = None
)
```

The list of found AggregatedSolutions and whether there is something else on the original request

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[AggregatedSolution](toloka.client.aggregation.AggregatedSolution.md)\]\]**|<p>List of found AggregatedSolution</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
