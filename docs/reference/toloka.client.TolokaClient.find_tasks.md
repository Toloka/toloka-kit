# find_tasks
`toloka.client.TolokaClient.find_tasks`

Finds all tasks that match certain rules


As a result, it returns an object that contains the first part of the found tasks and whether there
are any more results.
It is better to use the "get_tasks" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**Optional\[str\]**|<p>ID of the pool to get tasks from.</p>
`overlap`|**Optional\[int\]**|<p>Tasks with an overlap equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>Tasks with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Tasks with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Tasks with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Tasks with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Tasks created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Tasks created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Tasks created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Tasks created after or on the specified date.</p>
`overlap_lt`|**Optional\[int\]**|<p>Tasks with an overlap less than the specified value.</p>
`overlap_lte`|**Optional\[int\]**|<p>Tasks with an overlap equal to the specified value.</p>
`overlap_gt`|**Optional\[int\]**|<p>Tasks with an overlap greater than the specified value.</p>
`overlap_gte`|**Optional\[int\]**|<p>Tasks with an overlap equal to the specified value.</p>
`sort`|**Union\[List\[str\], [TaskSortItems](toloka.client.search_requests.TaskSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned. The maximum is 100 000. Defaults to None, in which case it returns first 50 results.</p>

* **Returns:**

  The first `limit` tasks in `items`. And a mark that there is more.

* **Return type:**

  [TaskSearchResult](toloka.client.search_results.TaskSearchResult.md)

**Examples:**

Find three most recently created tasks in a specified pool.

```python
toloka_client.find_tasks(pool_id='1', sort=['-created', '-id'], limit=3)
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
