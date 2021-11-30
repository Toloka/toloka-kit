# get_tasks
`toloka.client.TolokaClient.get_tasks`

Finds all tasks that match certain rules and returns them in an iterable object


Unlike find_tasks, returns generator. Does not sort tasks.
While iterating over the result, several requests to the Toloka server is possible.

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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[Task](toloka.client.task.Task.md), None, None\]

**Examples:**

Get tasks from a specific pool.

```python
results_list = [task for task in toloka_client.get_tasks(pool_id='1')]
```
