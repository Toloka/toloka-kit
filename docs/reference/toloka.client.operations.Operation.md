# Operation
`toloka.client.operations.Operation` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/operations.py#L50)

```python
Operation(
    self,
    *,
    id: Optional[str] = None,
    status: Union[Status, str, None] = None,
    submitted: Optional[datetime] = None,
    parameters: Optional[Parameters] = None,
    started: Optional[datetime] = None,
    finished: Optional[datetime] = None,
    progress: Optional[int] = None,
    details: Optional[Any] = None
)
```

Tracking Operation


Some API requests (opening and closing a pool, archiving a pool or a project, loading multiple tasks,
awarding bonuses) are processed as asynchronous operations that run in the background.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Operation ID.</p>
`status`|**Optional\[[Status](toloka.client.operations.Operation.Status.md)\]**|<p>The status of the operation.</p>
`submitted`|**Optional\[datetime\]**|<p>The UTC date and time the request was sent.</p>
`parameters`|**Optional\[[Parameters](toloka.client.operations.Operation.Parameters.md)\]**|<p>Operation parameters (depending on the operation type).</p>
`started`|**Optional\[datetime\]**|<p>The UTC date and time the operation started.</p>
`finished`|**Optional\[datetime\]**|<p>The UTC date and time the operation finished.</p>
`progress`|**Optional\[int\]**|<p>The percentage of the operation completed.</p>
`details`|**Optional\[Any\]**|<p>Details of the operation completion.</p>
## Methods Summary

| Method | Description |
| :------| :-----------|
[is_completed](toloka.client.operations.Operation.is_completed.md)| Returns True if the operation is completed. Status equals SUCCESS or FAIL.
[raise_on_fail](toloka.client.operations.Operation.raise_on_fail.md)| Raises FailedOperation exception if status is FAIL. Otherwise does nothing.
