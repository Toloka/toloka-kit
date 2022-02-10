# get_task_suite
`toloka.client.TolokaClient.get_task_suite`

```python
get_task_suite(self, task_suite_id: str)
```

Reads one specific task suite

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_suite_id`|**str**|<p>ID of the task suite.</p>

* **Returns:**

  The task suite.

* **Return type:**

  [TaskSuite](toloka.client.task_suite.TaskSuite.md)

**Examples:**

```python
toloka_client.get_task_suite(task_suite_id='1')
```
