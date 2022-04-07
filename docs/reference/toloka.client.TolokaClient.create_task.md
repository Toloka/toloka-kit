# create_task
`toloka.client.TolokaClient.create_task`

Creates a new task in Toloka.


You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
To create several tasks at once use [create_tasks](./toloka.client.TolokaClient.create_tasks.md).

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task`|**[Task](toloka.client.task.Task.md)**|<p>Task to be created.</p>
`allow_defaults`|**Optional\[bool\]**|<p>Overlap setting:<ul><li>True — Use the overlap value that is set in the `defaults.default_overlap_for_new_task_suites` pool parameter.</li><li>False — Use the overlap value that is set in the `overlap` task suite parameter.</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>

* **Returns:**

  The created task.

* **Return type:**

  [Task](toloka.client.task.Task.md)

**Examples:**

```python
task = toloka.task.Task(
    input_values={'image': 'https://tlk.s3.yandex.net/dataset/cats_vs_dogs/dogs/048e5760fc5a46faa434922b2447a527.jpg'},
    pool_id='1'
)
toloka_client.create_task(task=task, allow_defaults=True)
```
