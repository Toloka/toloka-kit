# patch_task_suite
`toloka.client.TolokaClient.patch_task_suite`

Changes the task suite overlap or priority

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_suite_id`|**str**|<p>ID of the task suite that will be changed.</p>
`issuing_order_override`|**Optional\[float\]**|<p>The priority of a task suite among other sets in the pool. Defines the order in which task suites are assigned to performers. The larger the parameter value, the higher the priority. This parameter can be used if the pool has issue_task_suites_in_creation_order: true. Allowed values: from -99999.99999 to 99999.99999.</p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after changing a task suite, if the pool is closed.</p>

* **Returns:**

  Task suite with updated fields.

* **Return type:**

  [TaskSuite](toloka.client.task_suite.TaskSuite.md)

**Examples:**

Change the task suite's priority.

```python
toloka_client.patch_task_suite(task_suite_id='1', issuing_order_override=100)
```
