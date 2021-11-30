# patch_task_suite_overlap_or_min
`toloka.client.TolokaClient.patch_task_suite_overlap_or_min`

Stops issuing the task suites

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_suite_id`|**str**|<p>ID of the task suite.</p>

* **Returns:**

  Task suite with updated fields.

* **Return type:**

  [TaskSuite](toloka.client.task_suite.TaskSuite.md)

**Examples:**

```python
toloka_client.patch_task_suite_overlap_or_min(task_suite_id='1', overlap=100)
```
