# TaskSuiteCreateBatchOperation
`toloka.client.operations.TaskSuiteCreateBatchOperation` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/operations.py#L297)

```python
TaskSuiteCreateBatchOperation(
    self,
    *,
    id: Optional[str] = None,
    status: Union[Operation.Status, str, None] = None,
    submitted: Optional[datetime] = None,
    started: Optional[datetime] = None,
    progress: Optional[int] = None,
    parameters: Optional[Parameters] = None,
    finished: Optional[datetime] = None,
    details: Optional[Any] = None
)
```

Operation returned by an asynchronous creating TaskSuite's via TolokaClient.create_task_suites_async()


All parameters are for reference only and describe the initial parameters of the request that this operation monitors.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Operation ID.</p>
`status`|**Optional\[[Operation.Status](toloka.client.operations.Operation.Status.md)\]**|<p>The status of the operation.</p>
`submitted`|**Optional\[datetime\]**|<p>The UTC date and time the request was sent.</p>
`started`|**Optional\[datetime\]**|<p>The UTC date and time the operation started.</p>
`progress`|**Optional\[int\]**|<p>The percentage of the operation completed.</p>
`parameters`|**Optional\[[Parameters](toloka.client.operations.TaskSuiteCreateBatchOperation.Parameters.md)\]**|<p>Operation parameters (depending on the operation type).</p>
`finished`|**Optional\[datetime\]**|<p>The UTC date and time the operation finished.</p>
`details`|**Optional\[Any\]**|<p>Details of the operation completion.</p>
`skip_invalid_items`|**-**|<p>Validation parameters for JSON objects:<ul><li>True - Create the task suites that passed validation. Skip the rest of the task suites.</li><li>False - If at least one of the task suites didn&#x27;t pass validation, stop the operation and     don&#x27;t create any task suites.</li></ul></p>
`allow_defaults`|**-**|<p>Overlap settings:<ul><li>True - Use the overlap that is set in the pool parameters.</li><li>False - Use the overlap that is set in the task parameters (in the overlap field).</li></ul></p>
`open_pool`|**-**|<p>Open the pool immediately after creating the task suites, if the pool is closed.</p>
