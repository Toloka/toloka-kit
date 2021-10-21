# CreateTasksParameters
`toloka.client.task.CreateTasksParameters`

```
CreateTasksParameters(
    self,
    *,
    allow_defaults: Optional[bool] = None,
    open_pool: Optional[bool] = None,
    skip_invalid_items: Optional[bool] = None,
    operation_id: Optional[UUID] = None,
    async_mode: Optional[bool] = True
)
```

Parameters for Tasks creation controlling


Used when creating many Tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`allow_defaults`|**Optional\[bool\]**|<p>Overlap settings:<ul><li>True - Use the overlap that is set in the pool parameters (in the defaults.default_overlap_for_new_task_suites key).</li><li>False - Use the overlap that is set in the task suite parameters (in the overlap field).</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters:<ul><li>True — Create the tasks that passed validation. Skip the rest of the tasks (errors will     be listed in the response to the request).</li><li>False — If at least one of the tasks didn&#x27;t pass validation, stop the operation and don&#x27;t create any tasks.</li></ul></p>
`async_mode`|**Optional\[bool\]**|<p>How the request is processed:<ul><li>True — deferred. The query results in an asynchronous operation running in the background.     The response contains information about the operation (start and end time, status, number of sets).</li><li>False — synchronous. The response contains information about the created tasks.     A maximum of 5000 tasks can be sent in a single request.</li></ul></p>
