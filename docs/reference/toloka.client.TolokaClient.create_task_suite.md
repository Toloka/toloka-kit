# create_task_suite
`toloka.client.TolokaClient.create_task_suite`

Creates a new task suite


Generally, you don't need to create a task set yourself, because you can create tasks and Toloka will create
task suites for you. Use this method only then you need to group specific tasks in one suite or to set a
different parameters on different tasks suites.
It's better to use "create_task_suites", if you need to insert several task suites.
You can send a maximum of 100,000 requests of this kind per minute and 2,000,000 requests per day.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_suite`|**[TaskSuite](toloka.client.task_suite.TaskSuite.md)**|<p>Task suite that need to be created.</p>
`operation_id`|**Optional\[UUID\]**|<p>Operation ID for asynchronous loading of task suites.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters:<ul><li>True - Create the task suites that passed validation. Skip the rest of the task suites.</li><li>False - If at least one of the task suites didn&#x27;t pass validation, stop the operation and     don&#x27;t create the task suites.</li></ul></p>
`allow_defaults`|**Optional\[bool\]**|<p>Overlap settings:<ul><li>True - Use the overlap that is set in the pool parameters.</li><li>False - Use the overlap that is set in the task suite parameters (in the overlap field).</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
`async_mode`|**Optional\[bool\]**|<p>How the request is processed:<ul><li>True — deferred. The query results in an asynchronous operation running in the background.     Answer contains information about the operation (start and end time, status, number of sets).</li><li>False — synchronous. Answer contains information about the generated sets of tasks.     You can send a maximum of 5000 task sets in a single request.</li></ul></p>

* **Returns:**

  Created task suite.

* **Return type:**

  [TaskSuite](toloka.client.task_suite.TaskSuite.md)

**Examples:**

```python
new_task_suite = toloka.task_suite.TaskSuite(
                pool_id='1',
                tasks=[toloka.task.Task(input_values={'label': 'Cats vs Dogs'})],
                overlap=2)
toloka_client.create_task_suite(new_task_suite)
```
