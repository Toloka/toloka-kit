# AssessmentEvent
`toloka.client.conditions.AssessmentEvent` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/conditions.py#L101)

```python
AssessmentEvent(
    self,
    operator: IdentityOperator,
    value: Union[Type, str, None] = None
)
```

Assessment of the assignment changes its status to the specified one


This condition can work only with compare operator '=='.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`value`|**Optional\[[Type](toloka.client.conditions.AssessmentEvent.Type.md)\]**|<p>Possible values:<ul><li>conditions.AssessmentEvent.ACCEPT</li><li>conditions.AssessmentEvent.ACCEPT_AFTER_REJECT</li><li>conditions.AssessmentEvent.REJECT</li></ul></p>

**Examples:**

How to increase task overlap when you reject assignment in delayed mode.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.AssignmentsAssessment(),
    conditions=[toloka.conditions.AssessmentEvent == toloka.conditions.AssessmentEvent.REJECT],
    action=toloka.actions.ChangeOverlap(delta=1, open_pool=True),
)
```
