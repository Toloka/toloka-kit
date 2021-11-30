# TrainingRequirement
`toloka.client.quality_control.QualityControl.TrainingRequirement`

```
TrainingRequirement(
    self,
    *,
    training_pool_id: Optional[str] = None,
    training_passing_skill_value: Optional[int] = None
)
```

Parameters of the training pool that is linked to the pool with the main tasks

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_pool_id`|**Optional\[str\]**|<p>ID of the training pool that is linked to the pool with the main tasks.</p>
`training_passing_skill_value`|**Optional\[int\]**|<p>The percentage of correct answers in training tasks (from 0 to 100) required for admission to the main tasks. The user&#x27;s first responses in tasks are used for counting.</p>
