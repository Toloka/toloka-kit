# ApproveAllAssignments
`toloka.client.actions.ApproveAllAssignments` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/actions.py#L208)

```python
ApproveAllAssignments(self)
```

Approve all replies from the performer


The performer is not explicitly installed, the approval occurs on the performer on which the rule will be triggered.


**Examples:**

How to approve all assignments if performer doing well with golden tasks.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.GoldenSet(history_size=5),
    conditions=[toloka.conditions.GoldenSetCorrectAnswersRate > 90],
    action=toloka.actions.ApproveAllAssignments()
)
```
