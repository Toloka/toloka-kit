# create_tasks_async
`toloka.client.TolokaClient.create_tasks_async`

Creates many tasks in pools, asynchronous version


You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
Recomended maximum of 10,000 task per request if async_mode is True.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`tasks`|**List\[[Task](toloka.client.task.Task.md)\]**|<p>List of tasks, that will be created.</p>
`allow_defaults`|**Optional\[bool\]**|<p>Overlap settings:<ul><li>True - Use the overlap that is set in the pool parameters (in the defaults.default_overlap_for_new_task_suites key).</li><li>False - Use the overlap that is set in the task suite parameters (in the overlap field).</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters:<ul><li>True — Create the tasks that passed validation. Skip the rest of the tasks (errors will     be listed in the response to the request).</li><li>False — If at least one of the tasks didn&#x27;t pass validation, stop the operation and don&#x27;t create any tasks.</li></ul></p>
`async_mode`|**Optional\[bool\]**|<p>How the request is processed:<ul><li>True — deferred. The query results in an asynchronous operation running in the background.     The response contains information about the operation (start and end time, status, number of sets).</li><li>False — synchronous. The response contains information about the created tasks.     A maximum of 5000 tasks can be sent in a single request.</li></ul></p>

* **Returns:**

  An operation upon completion of which you can get the created tasks.

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
