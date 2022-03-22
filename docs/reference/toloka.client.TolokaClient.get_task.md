# get_task
`toloka.client.TolokaClient.get_task` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
get_task(self, task_id: str)
```

Reads one specific task

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**str**|<p>ID of the task.</p>

* **Returns:**

  The task.

* **Return type:**

  [Task](toloka.client.task.Task.md)

**Examples:**

```python
toloka_client.get_task(task_id='1')
```
