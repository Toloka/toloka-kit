# AssignmentsAssessment
`toloka.client.collectors.AssignmentsAssessment`

```python
AssignmentsAssessment(self, *, uuid: Optional[UUID] = None)
```

Processing rejected and accepted assignments


This rule is helpful when you need to:
- Resend rejected assignments for re-completion to other performers. If you rejected an assignment, you may want it
to be completed by another performer instead of the one whose response you rejected. To do this, you can increase
the overlap for this assignment only. This is especially helpful if you have the overlap value set to 1.
- Save money on re-completing assignments that you have already accepted. If you reviewed and accepted an assignment,
it may not make sense for other users to complete the same assignment. To avoid this, you can reduce the overlap for
accepted assignments only.

Used with conditions:
* PendingAssignmentsCount - Number of Assignments pending checking.
* AcceptedAssignmentsCount - How many times this assignment was accepted.
* RejectedAssignmentsCount - How many times this assignment was rejected.
* AssessmentEvent - Assessment of the assignment changes its status to the specified one.

Used with actions:
* ChangeOverlap - Increase the overlap of the set of tasks.


**Examples:**

How to resend rejected assignments for re-completion to other performers.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.AssignmentsAssessment(),
    conditions=[toloka.conditions.AssessmentEvent == toloka.conditions.AssessmentEvent.REJECT],
    action=toloka.actions.ChangeOverlap(delta=1, open_pool=True),
)
```
