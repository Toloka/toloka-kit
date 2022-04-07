# RestrictionV2
`toloka.client.actions.RestrictionV2` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/actions.py#L58)

```python
RestrictionV2(
    self,
    *,
    scope: Union[UserRestriction.Scope, str, None] = None,
    duration: Optional[int] = None,
    duration_unit: Union[DurationUnit, str, None] = None,
    private_comment: Optional[str] = None
)
```

Block access to projects or pools

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`scope`|**Union\[[UserRestriction.Scope](toloka.client.user_restriction.UserRestriction.Scope.md), str, None\]**|<p><ul><li>POOL - Current pool where this rule was triggered. Does not affect the user&#x27;s rating.</li><li>PROJECT - Current project where this rule was triggered. Affects the user&#x27;s rating.</li><li>ALL_PROJECTS - All customer&#x27;s projects.</li></ul></p>
`duration`|**Optional\[int\]**|<p>Blocking period in duration_unit.</p>
`duration_unit`|**Union\[[DurationUnit](toloka.client.user_restriction.DurationUnit.md), str, None\]**|<p>In what units the restriction duration is measured:<ul><li>MINUTES</li><li>HOURS</li><li>DAYS</li><li>PERMANENT</li></ul></p>
`private_comment`|**Optional\[str\]**|<p>Comment (reason for blocking). Available only to the customer.</p>

**Examples:**

How to ban performers who answers too fast.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
    conditions=[toloka.conditions.FastSubmittedCount > 1],
    action=toloka.actions.RestrictionV2(
        scope=toloka.user_restriction.UserRestriction.PROJECT,
        duration=10,
        duration_unit='DAYS',
        private_comment='Fast responses',
    )
)
```
