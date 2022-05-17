# PoolCloneOperation
`toloka.client.operations.PoolCloneOperation` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/operations.py#L153)

```python
PoolCloneOperation(
    self,
    *,
    id: Optional[str] = None,
    status: Union[Operation.Status, str, None] = None,
    submitted: Optional[datetime] = None,
    started: Optional[datetime] = None,
    finished: Optional[datetime] = None,
    progress: Optional[int] = None,
    parameters: Optional[PoolOperation.Parameters] = None,
    details: Optional[Details] = None
)
```

Operation returned by an asynchronous cloning pool via TolokaClient.clone_pool_async()


As parameters.pool_id contains id of the pool that needs to be cloned.
New pool id stored in details.pool_id.
Don't be mistaken.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Operation ID.</p>
`status`|**Optional\[[Operation.Status](toloka.client.operations.Operation.Status.md)\]**|<p>The status of the operation.</p>
`submitted`|**Optional\[datetime\]**|<p>The UTC date and time the request was sent.</p>
`started`|**Optional\[datetime\]**|<p>The UTC date and time the operation started.</p>
`finished`|**Optional\[datetime\]**|<p>The UTC date and time the operation finished.</p>
`progress`|**Optional\[int\]**|<p>The percentage of the operation completed.</p>
`parameters`|**Optional\[[PoolOperation.Parameters](toloka.client.operations.PoolOperation.Parameters.md)\]**|<p>Operation parameters (depending on the operation type).</p>
`details`|**Optional\[[Details](toloka.client.operations.PoolCloneOperation.Details.md)\]**|<p>Details of the operation completion.</p>
`pool_id`|**-**|<p>On which pool operation is performed.</p>
`pool_id`|**-**|<p>New pool id created after cloning.</p>
