# SetSkillFromOutputField
`toloka.client.actions.SetSkillFromOutputField` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/actions.py#L98)

```python
SetSkillFromOutputField(
    self,
    *,
    skill_id: Optional[str] = None,
    from_field: Union[RuleConditionKey, str, None] = None
)
```

Set performer skill value from source


You can use this rule only with collectors.MajorityVote and collectors.GoldenSet.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`skill_id`|**Optional\[str\]**|<p>ID of the skill to update.</p>
`from_field`|**Union\[[RuleConditionKey](toloka.client.conditions.RuleConditionKey.md), str, None\]**|<p>The value to assign to the skill:<ul><li>correct_answers_rate - Percentage of correct answers.</li><li>incorrect_answer_rate - Percentage of incorrect answers.</li></ul></p>

**Examples:**

How to set the skill value to mean consistency with the majority.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.MajorityVote(answer_threshold=2, history_size=10),
    conditions=[
        toloka.conditions.TotalAnswersCount > 2,
    ],
    action=toloka.actions.SetSkillFromOutputField(
        skill_id=some_skill_id,
        from_field='correct_answers_rate',
    ),
)
```
