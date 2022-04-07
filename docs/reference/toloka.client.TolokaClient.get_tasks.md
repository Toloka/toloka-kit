# get_tasks
`toloka.client.TolokaClient.get_tasks`

Finds all tasks that match certain criteria.


`get_tasks` returns a generator and you can iterate over all found tasks. Several requests to the Toloka server
are possible while iterating.

Note that tasks can not be sorted. If you need to sort tasks use [find_tasks](toloka.client.TolokaClient.find_tasks.md).

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

* **Yields:**

  An iterable with found tasks.

* **Yield type:**

  Generator\[[Task](toloka.client.task.Task.md), None, None\]

**Examples:**

Getting all tasks from a single pool.

```python
results_list = [task for task in toloka_client.get_tasks(pool_id='1')]
```
