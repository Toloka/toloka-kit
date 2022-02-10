# GoldenSet
`toloka.client.collectors.GoldenSet`

```python
GoldenSet(
    self,
    *,
    uuid: Optional[UUID] = None,
    history_size: Optional[int] = None
)
```

How performer answers on control tasks


Use control tasks to assign a skill to performers based on their responses and ban performers who submit incorrect responses.

Don't use it if:
- You have a lot of response options.
- Users need to attach a file to their assignment.
- Users need to transcribe text.
- Users need to select objects in a photo.
- Tasks don't have a correct or incorrect response. For example: "Which image do you like best?" or
"Choose the page design option that you like best".

Used with conditions:
* TotalAnswersCount - The number of completed control and training tasks.
* CorrectAnswersRate - The percentage of correct responses in training and control tasks.
* IncorrectAnswersRate - The percentage of incorrect responses in training and control tasks.
* GoldenSetAnswersCount - The number of completed control tasks
* GoldenSetCorrectAnswersRate - The percentage of correct responses in control tasks.
* GoldenSetIncorrectAnswersRate - The percentage of incorrect responses in control tasks.

Used with actions:
* RestrictionV2 - Block access to projects or pools.
* ApproveAllAssignments - Approve all replies from the performer.
* RejectAllAssignments - Reject all replies from the performer.
* SetSkill - Set perfmer skill value.
* SetSkillFromOutputField - Set performer skill value from source.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`history_size`|**Optional\[int\]**|<p>The number of the performer&#x27;s last responses to control tasks.</p>

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
