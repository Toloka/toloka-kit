# UsersAssessment
`toloka.client.collectors.UsersAssessment`

```
UsersAssessment(self, *, uuid: Optional[UUID] = None)
```

Recompletion of assignments from banned users


If you or the system banned a performer and you want someone else to complete their tasks.
This rule will help you do this automatically.

Used with conditions:
* PoolAccessRevokedReason - Reason for loss of access of the performer to the current pool.
* SkillId - The performer no longer meets the specific skill filter.

Used with actions:
* ChangeOverlap - Increase the overlap of the set of tasks.


**Examples:**

How to resend rejected assignments for re-completion to other performers.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.UsersAssessment(),
    conditions=[toloka.conditions.PoolAccessRevokedReason == toloka.conditions.PoolAccessRevokedReason.RESTRICTION],
    action=toloka.actions.ChangeOverlap(delta=1, open_pool=True),
)
```
