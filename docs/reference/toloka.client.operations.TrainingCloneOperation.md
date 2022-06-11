# TrainingCloneOperation
`toloka.client.operations.TrainingCloneOperation` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/operations.py#L212)

```python
TrainingCloneOperation(
    self,
    *,
    id: Optional[str] = None,
    status: Union[Operation.Status, str, None] = None,
    submitted: Optional[datetime] = None,
    started: Optional[datetime] = None,
    finished: Optional[datetime] = None,
    progress: Optional[int] = None,
    parameters: Optional[TrainingOperation.Parameters] = None,
    details: Optional[Details] = None
)
```

Operation returned by an asynchronous cloning training pool via TolokaClient.clone_training_async()


As parameters.training_id contains id of the training pool that needs to be cloned.
New training pool id stored in details.training_id.
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
`parameters`|**Optional\[[TrainingOperation.Parameters](toloka.client.operations.TrainingOperation.Parameters.md)\]**|<p>Operation parameters (depending on the operation type).</p>
`details`|**Optional\[[Details](toloka.client.operations.TrainingCloneOperation.Details.md)\]**|<p>Details of the operation completion.</p>
`training_id`|**-**|<p>On which training pool operation is performed.</p>
`pool_id`|**-**|<p>New training pool id created after cloning.</p>
