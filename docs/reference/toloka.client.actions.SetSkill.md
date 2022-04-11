# SetSkill
`toloka.client.actions.SetSkill` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/actions.py#L160)

```python
SetSkill(
    self,
    *,
    skill_id: Optional[str] = None,
    skill_value: Optional[int] = None
)
```

Set performer skill value

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`skill_id`|**Optional\[str\]**|<p>ID of the skill to update.</p>
`skill_value`|**Optional\[int\]**|<p>The value to be assigned to the skill.</p>

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
