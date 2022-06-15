# get_task_suite
`toloka.client.TolokaClient.get_task_suite` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/__init__.py#L40)

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
