# TaskSuiteSearchResult
`toloka.client.search_results.TaskSuiteSearchResult`

```python
TaskSuiteSearchResult(
    self,
    *,
    items: Optional[List[TaskSuite]] = None,
    has_more: Optional[bool] = None
)
```

The list of found sets of tasks and whether there is something else on the original request


It's better to use TolokaClient.get_task_suites(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[TaskSuite](toloka.client.task_suite.TaskSuite.md)\]\]**|<p>List of found sets of tasks</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
