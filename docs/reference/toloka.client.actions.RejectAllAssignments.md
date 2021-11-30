# RejectAllAssignments
`toloka.client.actions.RejectAllAssignments`

```
RejectAllAssignments(self, *, public_comment: Optional[str] = None)
```

Reject all replies from the performer. Only for pools with post acceptance.


The performer is not explicitly installed, the rejection occurs on the performer on which the rule will be triggered.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`public_comment`|**Optional\[str\]**|<p>Describes why you reject all assignments from this performer.</p>

**Examples:**

How to reject all assignments if performer sends answers too fast (only for pools with post acceptance).

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
    conditions=[toloka.conditions.FastSubmittedCount > 3],
    action=toloka.actions.RejectAllAssignments(public_comment='Too fast answering. You are cheater!')
)
```
