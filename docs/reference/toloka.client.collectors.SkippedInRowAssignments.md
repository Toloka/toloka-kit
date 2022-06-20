# SkippedInRowAssignments
`toloka.client.collectors.SkippedInRowAssignments` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/collectors.py#L434)

```python
SkippedInRowAssignments(self, *, uuid: Optional[UUID] = None)
```

Skipping tasks is considered an indirect indicator of the quality of responses.


You can block access to a pool or project if a user skips multiple task suites in a row.

Used with conditions:
* SkippedInRowCount - How many tasks in a row the performer skipped.

Used with actions:
* RestrictionV2 - Block access to projects or pools.
* ApproveAllAssignments - Approve all replies from the performer.
* RejectAllAssignments - Reject all replies from the performer.
* SetSkill - Set perfmer skill value.


**Examples:**

How to ban a performer in this project if he skipped tasks.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.SkippedInRowAssignments(),
    conditions=[toloka.conditions.SkippedInRowCount > 3],
    action=toloka.actions.RestrictionV2(
        scope=toloka.user_restriction.UserRestriction.PROJECT,
        duration=15,
        duration_unit='DAYS',
        private_comment='Lazy performer',
    )
)
```
