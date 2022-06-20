# find_tasks
`toloka.client.TolokaClient.find_tasks`

Finds tasks that match certain criteria.


The number of returned tasks is limited. `find_tasks` additionally returns a flag showing whether there are more matching tasks.
Consider using [get_tasks](./toloka.client.TolokaClient.get_tasks.md) to iterate over all matching tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**Optional\[str\]**|<p>The ID of the pool to get tasks from.</p>
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
`overlap_lte`|**Optional\[int\]**|<p>Tasks with an overlap less than or equal to the specified value.</p>
`overlap_gt`|**Optional\[int\]**|<p>Tasks with an overlap greater than the specified value.</p>
`overlap_gte`|**Optional\[int\]**|<p>Tasks with an overlap greater than or equal to the specified value.</p>
`sort`|**Union\[List\[str\], [TaskSortItems](toloka.client.search_requests.TaskSortItems.md), None\]**|<p>Sorting options. </p><p>Default value: `None`.</p>
`limit`|**Optional\[int\]**|<p>Returned tasks limit. The maximum value is 100,000. </p><p>Default value: 50.</p>

* **Returns:**

  Found tasks and a flag showing whether there are more matching tasks.

* **Return type:**

  [TaskSearchResult](toloka.client.search_results.TaskSearchResult.md)

**Examples:**

To find three most recently created tasks in a pool, call the method with the following parameters:

```python
toloka_client.find_tasks(pool_id='1', sort=['-created', '-id'], limit=3)
```
