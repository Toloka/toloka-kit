# ChangeOverlap
`toloka.client.actions.ChangeOverlap`

```python
ChangeOverlap(
    self,
    *,
    delta: Optional[int] = None,
    open_pool: Optional[bool] = None
)
```

Increase the overlap of the set of tasks (or tasks, if the option is used "smart mixing")


You can use this rule only with collectors.UsersAssessment and collectors.AssignmentsAssessment.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`delta`|**Optional\[int\]**|<p>The number by which you want to increase the overlap of the task set (or the task if the option is used &quot;smart mixing&quot;).</p>
`open_pool`|**Optional\[bool\]**|<p>Changing the pool status:<ul><li>True - Open the pool after changing if it is closed.</li><li>False - Do not open the pool after the change if it is closed.</li></ul></p>

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
