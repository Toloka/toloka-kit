# Settings
`toloka.client.quality_control.QualityControl.CheckpointsConfig.Settings` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/quality_control.py#L80)

```python
Settings(
    self,
    *,
    target_overlap: Optional[int] = None,
    task_distribution_function: Optional[TaskDistributionFunction] = None
)
```

Setting for checkpoints

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`target_overlap`|**Optional\[int\]**|<p>Overlap in tasks with majority opinion verification.</p>
`task_distribution_function`|**Optional\[[TaskDistributionFunction](toloka.client.task_distribution_function.TaskDistributionFunction.md)\]**|<p>Distribution of tasks with majority opinion verification.</p>
