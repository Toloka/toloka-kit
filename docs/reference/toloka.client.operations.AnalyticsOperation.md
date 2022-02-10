# AnalyticsOperation
`toloka.client.operations.AnalyticsOperation`

```python
AnalyticsOperation(
    self,
    *,
    id: Optional[str] = None,
    status: Union[Operation.Status, str, None] = None,
    submitted: Optional[datetime] = None,
    parameters: Optional[Operation.Parameters] = None,
    started: Optional[datetime] = None,
    finished: Optional[datetime] = None,
    progress: Optional[int] = None,
    details: Optional[Any] = None
)
```

Operation returned when requesting analytics via TolokaClient.get_analytics()

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Operation ID.</p>
`status`|**Optional\[[Operation.Status](toloka.client.operations.Operation.Status.md)\]**|<p>The status of the operation.</p>
`submitted`|**Optional\[datetime\]**|<p>The UTC date and time the request was sent.</p>
`parameters`|**Optional\[[Operation.Parameters](toloka.client.operations.Operation.Parameters.md)\]**|<p>Operation parameters (depending on the operation type).</p>
`started`|**Optional\[datetime\]**|<p>The UTC date and time the operation started.</p>
`finished`|**Optional\[datetime\]**|<p>The UTC date and time the operation finished.</p>
`progress`|**Optional\[int\]**|<p>The percentage of the operation completed.</p>
`details`|**Optional\[Any\]**|<p>Details of the operation completion.</p>
