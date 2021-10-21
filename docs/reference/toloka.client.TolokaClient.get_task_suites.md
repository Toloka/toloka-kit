# get_task_suites
`toloka.client.TolokaClient.get_task_suites`

Finds all task suites that match certain rules and returns them in an iterable object


Unlike find_task_suites, returns generator. Does not sort task suites.
While iterating over the result, several requests to the Toloka server is possible.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**Optional\[str\]**|<p>The task ID in suites generated automatically using &quot;smart mixing&quot;. You will get task suites that contain the specified task.</p>
`pool_id`|**Optional\[str\]**|<p>ID of the pool to get task suites from.</p>
`overlap`|**Optional\[int\]**|<p>Suites with an overlap equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>Task suites with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Task suites with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Task suites with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Task suites with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Task suites created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Task suites created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Task suites created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Task suites created after or on the specified date.</p>
`overlap_lt`|**Optional\[int\]**|<p>Suites with an overlap less than the specified value.</p>
`overlap_lte`|**Optional\[int\]**|<p>Suites with an overlap less than or equal to the specified value.</p>
`overlap_gt`|**Optional\[int\]**|<p>Suites with an overlap greater than the specified value.</p>
`overlap_gte`|**Optional\[int\]**|<p>Suites with an overlap greater than or equal to the specified value.</p>

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[TaskSuite](toloka.client.task_suite.TaskSuite.md), None, None\]

**Examples:**

Get task suites from a specific pool.

```python
results_list = [task_suite for task_suite in toloka_client.get_task_suites(pool_id='1')]
```
