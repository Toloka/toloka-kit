# TrainingOpenOperation
`toloka.client.operations.TrainingOpenOperation` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/operations.py#L238)

```python
TrainingOpenOperation(
    self,
    *,
    id: Optional[str] = None,
    status: Union[Operation.Status, str, None] = None,
    submitted: Optional[datetime] = None,
    started: Optional[datetime] = None,
    finished: Optional[datetime] = None,
    progress: Optional[int] = None,
    details: Optional[Any] = None,
    parameters: Optional[TrainingOperation.Parameters] = None
)
```

Operation returned by an asynchronous opening training pool via TolokaClient.open_training_async()

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Operation ID.</p>
`status`|**Optional\[[Operation.Status](toloka.client.operations.Operation.Status.md)\]**|<p>The status of the operation.</p>
`submitted`|**Optional\[datetime\]**|<p>The UTC date and time the request was sent.</p>
`started`|**Optional\[datetime\]**|<p>The UTC date and time the operation started.</p>
`finished`|**Optional\[datetime\]**|<p>The UTC date and time the operation finished.</p>
`progress`|**Optional\[int\]**|<p>The percentage of the operation completed.</p>
`details`|**Optional\[Any\]**|<p>Details of the operation completion.</p>
`parameters`|**Optional\[[TrainingOperation.Parameters](toloka.client.operations.TrainingOperation.Parameters.md)\]**|<p>Operation parameters (depending on the operation type).</p>
`training_id`|**-**|<p>On which training pool operation is performed.</p>
