# TrainingSearchResult
`toloka.client.search_results.TrainingSearchResult`

```
TrainingSearchResult(
    self,
    *,
    items: Optional[List[Training]] = None,
    has_more: Optional[bool] = None
)
```

The list of found training pools and whether there is something else on the original request


It's better to use TolokaClient.get_trainings(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[Training](toloka.client.training.Training.md)\]\]**|<p>List of found training pools</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
