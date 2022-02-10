# UserBonusCreateRequestParameters
`toloka.client.user_bonus.UserBonusCreateRequestParameters`

```python
UserBonusCreateRequestParameters(
    self,
    *,
    operation_id: Optional[str] = None,
    skip_invalid_items: Optional[bool] = None
)
```

Parameters for creating performer bonuses


Used in methods 'create_user_bonus', 'create_user_bonuses' и 'create_user_bonuses_async' of the class TolokaClient,
to clarify the behavior when creating bonuses.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operation_id`|**Optional\[str\]**|<p>Operation ID. If asynchronous creation is used, by this identifier you can later get results of creating bonuses.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters of objects:<ul><li>True - Award a bonus if the object with bonus information passed validation. Otherwise, skip the bonus.</li><li>False - Default behaviour. Stop the operation and don&#x27;t award bonuses if at least one object didn&#x27;t pass validation.</li></ul></p>
