# UserSkill
`toloka.client.user_skill.UserSkill`

```python
UserSkill(
    self,
    *,
    id: Optional[str] = None,
    skill_id: Optional[str] = None,
    user_id: Optional[str] = None,
    value: Optional[int] = None,
    exact_value: Optional[Decimal] = None,
    created: Optional[datetime] = None,
    modified: Optional[datetime] = None
)
```

Describes the value of a specific skill for a specific performer

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Internal identifier of the user&#x27;s skill value.</p>
`skill_id`|**Optional\[str\]**|<p>Skill identifier, which skill is installed.</p>
`user_id`|**Optional\[str\]**|<p>User identifier, to which performer the skill is installed.</p>
`value`|**Optional\[int\]**|<p>Skill value (from 0 to 100). Rough presentation.</p>
`exact_value`|**Optional\[Decimal\]**|<p>Skill value (from 0 to 100). Exact representation.</p>
`created`|**Optional\[datetime\]**|<p>Date and time when this skill was created for the performer.</p>
`modified`|**Optional\[datetime\]**|<p>Date and time of the last skill change for the performer.</p>
