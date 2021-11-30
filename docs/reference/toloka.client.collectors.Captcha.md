# Captcha
`toloka.client.collectors.Captcha`

```
Captcha(
    self,
    *,
    uuid: Optional[UUID] = None,
    history_size: Optional[int] = None
)
```

Captchas provide a high level of protection from robots


Used with conditions:
* StoredResultsCount - How many times the performer entered captcha.
* SuccessRate - Percentage of correct answers of the performer to the captcha.
* FailRate - Percentage of wrong answers of the performer to the captcha.

Used with actions:
* RestrictionV2 - Block access to projects or pools.
* ApproveAllAssignments - Approve all replies from the performer.
* RejectAllAssignments - Reject all replies from the performer.
* SetSkill - Set perfmer skill value.
* SetSkillFromOutputField - Set performer skill value from source.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`history_size`|**Optional\[int\]**|<p>The number of times the performer was shown a captcha recently.</p>

**Examples:**

How to ban a performer in this project if he mistakes in captcha.

```python
new_pool = toloka.pool.Pool(....)
new_pool.set_captcha_frequency('MEDIUM')
new_pool.quality_control.add_action(
collector=toloka.collectors.Captcha(history_size=5),
    conditions=[
        toloka.conditions.SuccessRate < 60,
    ],
    action=toloka.actions.RestrictionV2(
        scope=toloka.user_restriction.UserRestriction.PROJECT,
        duration=15,
        duration_unit='DAYS',
        private_comment='Performer often make mistakes in captcha',
    )
)
```
