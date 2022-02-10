# TrainingSearchRequest
`toloka.client.search_requests.TrainingSearchRequest`

```python
TrainingSearchRequest(
    self,
    status: Optional[Training.Status] = None,
    project_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None,
    last_started_lt: Optional[datetime] = None,
    last_started_lte: Optional[datetime] = None,
    last_started_gt: Optional[datetime] = None,
    last_started_gte: Optional[datetime] = None
)
```

Parameters for searching training pools

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status`|**Optional\[[Training.Status](toloka.client.training.Training.Status.md)\]**|<p>Training pool status:<ul><li>OPEN</li><li>CLOSED</li><li>ARCHIVED</li><li>LOCKED</li></ul></p>
`project_id`|**Optional\[str\]**|<p>ID of the project to which the training pool is attached.</p>
`id_lt`|**Optional\[str\]**|<p>Training pools with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Training pools with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Training pools with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Training pools with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Training pools created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Training pools created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Training pools created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Training pools created after or on the specified date.</p>
`last_started_lt`|**Optional\[datetime\]**|<p>Training pools that were last opened before the specified date.</p>
`last_started_lte`|**Optional\[datetime\]**|<p>Training pools that were last opened on or before the specified date.</p>
`last_started_gt`|**Optional\[datetime\]**|<p>Training pools that were last opened after the specified date.</p>
`last_started_gte`|**Optional\[datetime\]**|<p>Training pools that were last opened on or after the specified date.</p>
