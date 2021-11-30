# patch_task_overlap_or_min
`toloka.client.TolokaClient.patch_task_overlap_or_min`

Stops issuing the task

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**str**|<p>ID of the task.</p>
`overlap`|**Optional\[int\]**|<p>Overlapping a set of tasks.</p>
`infinite_overlap`|**Optional\[bool\]**|<p>Issue a task with infinite overlap. Used, for example, for sets of training tasks to give them to all users:<ul><li>True - Set infinite overlap.</li><li>False - Leave the overlap specified for the task or pool. Default Behaviour.</li></ul></p>

* **Returns:**

  Task with updated fields.

* **Return type:**

  [Task](toloka.client.task.Task.md)

**Examples:**

Set an infinite overlap for a specific task in training.

```python
toloka_client.patch_task_overlap_or_min(task_id='1', infinite_overlap=True)
```

**Note**: you can't set infinite overlap in a regular pool.
