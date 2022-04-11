# AcceptanceRate
`toloka.client.collectors.AcceptanceRate` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/collectors.py#L62)

```python
AcceptanceRate(
    self,
    *,
    uuid: Optional[UUID] = None,
    history_size: Optional[int] = None
)
```

Results of checking the answers of the performer


If non-automatic acceptance (assignment review) is set in the pool, add a rule to:
- Set the performer's skill based on their responses.
- Block access for performers who give incorrect responses.

Used with conditions:
* TotalAssignmentsCount - How many assignments from this performer were checked.
* AcceptedAssignmentsRate - Percentage of how many assignments were accepted from this performer out of all checked assignment.
* RejectedAssignmentsRate - Percentage of how many assignments were rejected from this performer out of all checked assignment.

Used with actions:
* RestrictionV2 - Block access to projects or pools.
* ApproveAllAssignments - Approve all replies from the performer.
* RejectAllAssignments - Reject all replies from the performer.
* SetSkill - Set perfmer skill value.
* SetSkillFromOutputField - Set performer skill value from source.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`history_size`|**Optional\[int\]**|<p>The maximum number of recent tasks that the user completed in the project to use for the calculation. If this field is omitted, the calculation is based on all the tasks that the user completed in the pool.</p>

**Examples:**

How to ban a performer in this project if he makes mistakes.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
collector=toloka.collectors.AcceptanceRate(),
    conditions=[
        toloka.conditions.TotalAssignmentsCount > 2,
        toloka.conditions.RejectedAssignmentsRate > 35,
    ],
    action=toloka.actions.RestrictionV2(
        scope=toloka.user_restriction.UserRestriction.PROJECT,
        duration=15,
        duration_unit='DAYS',
        private_comment='Performer often make mistakes',
    )
)
```
