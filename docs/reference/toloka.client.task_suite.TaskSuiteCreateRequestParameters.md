# TaskSuiteCreateRequestParameters
`toloka.client.task_suite.TaskSuiteCreateRequestParameters` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/task_suite.py#L77)

```python
TaskSuiteCreateRequestParameters(
    self,
    *,
    operation_id: Optional[UUID] = None,
    skip_invalid_items: Optional[bool] = None,
    allow_defaults: Optional[bool] = None,
    open_pool: Optional[bool] = None,
    async_mode: Optional[bool] = True
)
```

Parameters for TaskSuite creation controlling

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operation_id`|**Optional\[UUID\]**|<p>Operation ID for asynchronous loading of task suites.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters:<ul><li>True - Create the task suites that passed validation. Skip the rest of the task suites.</li><li>False - If at least one of the task suites didn&#x27;t pass validation, stop the operation and     don&#x27;t create the task suites.</li></ul></p>
`allow_defaults`|**Optional\[bool\]**|<p>Overlap settings:<ul><li>True - Use the overlap that is set in the pool parameters.</li><li>False - Use the overlap that is set in the task suite parameters (in the overlap field).</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
`async_mode`|**Optional\[bool\]**|<p>How the request is processed:<ul><li>True — deferred. The query results in an asynchronous operation running in the background.     Answer contains information about the operation (start and end time, status, number of sets).</li><li>False — synchronous. Answer contains information about the generated sets of tasks.     You can send a maximum of 5000 task sets in a single request.</li></ul></p>
