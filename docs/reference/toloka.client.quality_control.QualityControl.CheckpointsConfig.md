# CheckpointsConfig
`toloka.client.quality_control.QualityControl.CheckpointsConfig`

```python
CheckpointsConfig(
    self,
    *,
    real_settings: Optional[Settings] = None,
    golden_settings: Optional[Settings] = None,
    training_settings: Optional[Settings] = None
)
```

Random check majority opinion.


Only some tasks are issued with a high overlap (for example, "5") and are being tested.
Other tasks are issued with the overlap set in the pool settings (for example, "1") and remain without verification.
Spot check saves money and speeds up pool execution.

You can reduce the frequency of checks over time.

Example settings: in the first 25 tasks completed by the user in the pool, issue every fifth task with an overlap "5"
to check the answers. In subsequent tasks issue each 25 task with an overlap "5".

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`real_settings`|**Optional\[[Settings](toloka.client.quality_control.QualityControl.CheckpointsConfig.Settings.md)\]**|<p>Checkpoints settings for main tasks.</p>
`golden_settings`|**Optional\[[Settings](toloka.client.quality_control.QualityControl.CheckpointsConfig.Settings.md)\]**|<p>Checkpoints settings for golden tasks.</p>
`training_settings`|**Optional\[[Settings](toloka.client.quality_control.QualityControl.CheckpointsConfig.Settings.md)\]**|<p>Checkpoints settings for train tasks.</p>
