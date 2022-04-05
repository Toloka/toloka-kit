# QualityControl
`toloka.client.quality_control.QualityControl` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/quality_control.py#L13)

```python
QualityControl(
    self,
    *,
    training_requirement: Optional[TrainingRequirement] = None,
    captcha_frequency: Union[CaptchaFrequency, str, None] = None,
    configs: Optional[List[QualityControlConfig]] = ...,
    checkpoints_config: Optional[CheckpointsConfig] = None
)
```

Quality control unit settings and pool ID with training tasks


Quality control lets you get more accurate responses and restrict access to tasks for cheating performers.
Quality control consists of rules. All rules work independently.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_requirement`|**Optional\[[TrainingRequirement](toloka.client.quality_control.QualityControl.TrainingRequirement.md)\]**|<p>Parameters of the training pool that is linked to the pool with the main tasks.</p>
`captcha_frequency`|**Optional\[[CaptchaFrequency](toloka.client.quality_control.QualityControl.CaptchaFrequency.md)\]**|<p>Frequency of captcha display (By default, captcha is not shown): LOW - show every 20 tasks. MEDIUM, HIGH - show every 10 tasks.</p>
`configs`|**Optional\[List\[[QualityControlConfig](toloka.client.quality_control.QualityControl.QualityControlConfig.md)\]\]**|<p>List of quality control units. See QualityControl.QualityControlConfig</p>
`checkpoints_config`|**Optional\[[CheckpointsConfig](toloka.client.quality_control.QualityControl.CheckpointsConfig.md)\]**|<p>Random check majority opinion. Datailed description in QualityControl.CheckpointsConfig.</p>

**Examples:**

How to set up quality control on new pool.

```python
new_pool = toloka.pool.Pool(....)
new_pool.quality_control.add_action(
    collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
    conditions=[toloka.conditions.FastSubmittedCount > 1],
    action=toloka.actions.RestrictionV2(
        scope=toloka.user_restriction.UserRestriction.ALL_PROJECTS,
        duration=10,
        duration_unit='DAYS',
        private_comment='Fast responses',  # Only you will see this comment
    )
)
```
## Methods Summary

| Method | Description |
| :------| :-----------|
[add_action](toloka.client.quality_control.QualityControl.add_action.md)| Adds new QualityControlConfig to QualityControl object. Usually in pool.
