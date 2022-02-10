# MajorityVote
`toloka.client.collectors.MajorityVote`

```python
MajorityVote(
    self,
    *,
    uuid: Optional[UUID] = None,
    answer_threshold: Optional[int] = None,
    history_size: Optional[int] = None
)
```

Majority vote is a quality control method based on coinciding responses from the majority


The response chosen by the majority is considered correct, and other responses are considered incorrect.
Depending on the percentage of correct responses, you can either increase the user's skill value, or ban the user from tasks.

Used with conditions:
* TotalAnswersCount - The number of completed tasks by the performer.
* CorrectAnswersRate - The percentage of correct responses.
* IncorrectAnswersRate - The percentage of incorrect responses.

Used with actions:
* RestrictionV2 - Block access to projects or pools.
* ApproveAllAssignments - Approve all replies from the performer.
* RejectAllAssignments - Reject all replies from the performer.
* SetSkill - Set perfmer skill value.
* SetSkillFromOutputField - Set performer skill value from source.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`answer_threshold`|**Optional\[int\]**|<p>The number of users considered the majority (for example, 3 out of 5).</p>
`history_size`|**Optional\[int\]**|<p>The maximum number of the user&#x27;s recent responses in the project to use for calculating the percentage of correct responses. If this field is omitted, the calculation is based on all the user&#x27;s responses in the pool.</p>

**Examples:**

How to ban a performer in this project if he made enough answers (only for pools with post acceptance).

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.MajorityVote(answer_threshold=2),
    conditions=[
        toloka.conditions.TotalAnswersCount > 9,
        toloka.conditions.CorrectAnswersRate < 60,
    ],
    action=toloka.actions.RejectAllAssignments(public_comment='Too low quality')
)
```
