# UserBonusCreateBatchOperation
`toloka.client.operations.UserBonusCreateBatchOperation` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/operations.py#L344)

```python
UserBonusCreateBatchOperation(
    self,
    *,
    id: Optional[str] = None,
    status: Union[Operation.Status, str, None] = None,
    submitted: Optional[datetime] = None,
    started: Optional[datetime] = None,
    finished: Optional[datetime] = None,
    progress: Optional[int] = None,
    parameters: Optional[Parameters] = None,
    details: Optional[Details] = None
)
```

Operation returned by an asynchronous creating user bonuses via TolokaClient.create_user_bonuses_async()


All parameters are for reference only and describe the initial parameters of the request that this operation monitors.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Operation ID.</p>
`status`|**Optional\[[Operation.Status](toloka.client.operations.Operation.Status.md)\]**|<p>The status of the operation.</p>
`submitted`|**Optional\[datetime\]**|<p>The UTC date and time the request was sent.</p>
`started`|**Optional\[datetime\]**|<p>The UTC date and time the operation started.</p>
`finished`|**Optional\[datetime\]**|<p>The UTC date and time the operation finished.</p>
`progress`|**Optional\[int\]**|<p>The percentage of the operation completed.</p>
`parameters`|**Optional\[[Parameters](toloka.client.operations.UserBonusCreateBatchOperation.Parameters.md)\]**|<p>Operation parameters (depending on the operation type).</p>
`details`|**Optional\[[Details](toloka.client.operations.UserBonusCreateBatchOperation.Details.md)\]**|<p>Details of the operation completion.</p>
`skip_invalid_items`|**-**|<p>Validation parameters for JSON objects:<ul><li>True - Create the user bonuses that passed validation. Skip the rest of the user bonuses.</li><li>False - If at least one of the user bonus didn&#x27;t pass validation, stop the operation and     don&#x27;t create any user bonus.</li></ul></p>
`pool_id`|**-**|<p></p>
`total_count`|**-**|<p>The number of bonuses in the request.</p>
`valid_count`|**-**|<p>The number of JSON objects with bonus information that have passed validation.</p>
`not_valid_count`|**-**|<p>The number of JSON objects with bonus information that failed validation.</p>
`success_count`|**-**|<p>Number of bonuses issued.</p>
`failed_count`|**-**|<p>The number of bonuses that were not issued.</p>
