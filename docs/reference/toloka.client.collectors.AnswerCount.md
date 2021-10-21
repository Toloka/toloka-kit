# AnswerCount
`toloka.client.collectors.AnswerCount`

```
AnswerCount(self, *, uuid: Optional[UUID] = None)
```

How many assignment was accepted from performer


Use this rule if you want to:
- Get responses from as many performers as possible (for this purpose, set a low threshold, such as one task suite).
- Protect yourself from robots (for this purpose, the threshold should be higher, such as 10% of the pool's tasks).
- Mark performers completing a task so that you can filter them later in the checking project.

Used with conditions:
* AssignmentsAcceptedCount - How many assignment was accepted from performer

Used with actions:
* RestrictionV2 - Block access to projects or pools.
* ApproveAllAssignments - Approve all replies from the performer.
* RejectAllAssignments - Reject all replies from the performer.
* SetSkill - Set perfmer skill value.


**Examples:**

How to mark performers completing a task so that you can filter them later in the checking project.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.AnswerCount(),
    conditions=[toloka.conditions.AssignmentsAcceptedCount > 0],
    action=toloka.actions.SetSkill(skill_id=some_skill_id, skill_value=1),
)
```
