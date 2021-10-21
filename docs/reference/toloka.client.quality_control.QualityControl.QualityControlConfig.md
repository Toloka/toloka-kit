# QualityControlConfig
`toloka.client.quality_control.QualityControl.QualityControlConfig`

```
QualityControlConfig(
    self,
    *,
    rules: Optional[List[RuleConfig]] = None,
    collector_config: Optional[CollectorConfig] = None
)
```

Quality control block


Quality control blocks help regulate access to a project or pool: you can filter out users who give incorrect answers
in control tasks, skip many tasks in a row, and so on.

The block consists of two parts: condition and the action to be performed when the condition is met.
There may be several conditions, then they are combined using logical And.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`rules`|**Optional\[List\[[RuleConfig](toloka.client.quality_control.QualityControl.QualityControlConfig.RuleConfig.md)\]\]**|<p>Conditions and action if conditions are met.</p>
`collector_config`|**Optional\[[CollectorConfig](toloka.client.collectors.CollectorConfig.md)\]**|<p>Parameters for collecting statistics (for example, the number of task skips in the pool).</p>
