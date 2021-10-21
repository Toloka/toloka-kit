# Income
`toloka.client.collectors.Income`

```
Income(self, *, uuid: Optional[UUID] = None)
```

Limit the performer's daily earnings in the pool


Helpful when you need to:
- Get responses from as many performers as possible.

Used with conditions:
* IncomeSumForLast24Hours - The performer earnings for completed tasks in the pool over the last 24 hours.

Used with actions:
* RestrictionV2 - Block access to projects or pools.
* ApproveAllAssignments - Approve all replies from the performer.
* RejectAllAssignments - Reject all replies from the performer.
* SetSkill - Set perfmer skill value.


**Examples:**

How to ban a performer in this project if he made enough answers.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.Income(),
    conditions=[toloka.conditions.IncomeSumForLast24Hours > 1],
    action=toloka.actions.RestrictionV2(
        scope=toloka.user_restriction.UserRestriction.PROJECT,
        duration=15,
        duration_unit='DAYS',
        private_comment='No need more answers from this performer',
    )
)
```
