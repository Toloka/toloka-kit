# patch_task_overlap_or_min
`toloka.client.TolokaClient.patch_task_overlap_or_min`

Stops assigning a task to users.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**str**|<p>The ID of the task.</p>
`overlap`|**Optional\[int\]**|<p>Overlap value.</p>
`infinite_overlap`|**Optional\[bool\]**|<p>Infinite overlap:<ul><li>True — Assign the task to all users. It is useful for training tasks.</li><li>False — Overlap value specified for the task or for the pool is used. </li></ul></p><p>Default value: False.</p>

* **Returns:**

  The task with updated fields.

* **Return type:**

  [Task](toloka.client.task.Task.md)

**Examples:**

Setting an infinite overlap for a training task.

```python
toloka_client.patch_task_overlap_or_min(task_id='1', infinite_overlap=True)
```

{% note info %}

You can't set infinite overlap in a regular pool.

{% endnote %}
