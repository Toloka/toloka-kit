# UserSkillEvent
`toloka.streaming.event.UserSkillEvent`

```
UserSkillEvent(
    self,
    *,
    event_time: Optional[datetime] = None,
    event_type: Union[Type, str, None] = None,
    user_skill: Optional[UserSkill] = None
)
```

UserSkill-related event.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`event_time`|**Optional\[datetime\]**|<p>Event datetime.</p>
`event_type`|**Optional\[[Type](toloka.streaming.event.UserSkillEvent.Type.md)\]**|<p>One of the folllowing event types:<ul><li>CREATED</li><li>MODIFIED</li></ul></p>
`user_skill`|**Optional\[[UserSkill](toloka.client.user_skill.UserSkill.md)\]**|<p>UserSkill object itself.</p>
