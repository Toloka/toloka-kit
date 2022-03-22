# UserBonusEvent
`toloka.streaming.event.UserBonusEvent` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/streaming/event.py#L65)

```python
UserBonusEvent(
    self,
    *,
    event_time: Optional[datetime] = None,
    user_bonus: Optional[UserBonus] = None
)
```

UserBonus-related event.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`event_time`|**Optional\[datetime\]**|<p>Event datetime.</p>
`user_bonus`|**Optional\[[UserBonus](toloka.client.user_bonus.UserBonus.md)\]**|<p>UserBonus object itself.</p>
