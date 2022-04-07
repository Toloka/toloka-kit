# create_tasks_async
`toloka.client.TolokaClient.create_tasks_async`

Creates tasks in Toloka asynchronously.


You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`tasks`|**List\[[Task](toloka.client.task.Task.md)\]**|<p>List of tasks to be created.</p>
`allow_defaults`|**Optional\[bool\]**|<p>Overlap setting:<ul><li>True — Use the overlap value that is set in the `defaults.default_overlap_for_new_task_suites` pool parameter.</li><li>False — Use the overlap value that is set in the `overlap` task suite parameter.</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Task validation option:<ul><li>True — All valid tasks are added. If a task does not pass validation, then it is not added to Toloka. All such tasks are listed in the response.</li><li>False — If any task does not pass validation, then operation is cancelled and no tasks are added to Toloka.</li></ul></p>
`async_mode`|**Optional\[bool\]**|<p>Request processing mode:<ul><li>True — Asynchronous operation is started internally and `create_tasks` waits for the completion of it. It is recommended to create no more than 10,000 tasks per request in this mode.</li><li>False — The request is processed synchronously. A maximum of 5000 tasks can be added in a single request in this mode.</li></ul></p>

* **Returns:**

  An object to track the progress of the operation.

* **Return type:**

  [TasksCreateOperation](toloka.client.operations.TasksCreateOperation.md)

**Examples:**

```python
training_tasks = [
    toloka.task.Task(
                input_values={'image': 'link1'},
                pool_id='1'),
    toloka.task.Task(
            input_values={'image': 'link2'},
            pool_id='1')
]
tasks_op = toloka_client.create_tasks_async(training_tasks)
toloka_client.wait_operation(tasks_op)
```
