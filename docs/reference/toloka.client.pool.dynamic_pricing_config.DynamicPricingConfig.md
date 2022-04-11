# DynamicPricingConfig
`toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/pool/dynamic_pricing_config.py#L9)

```python
DynamicPricingConfig(
    self,
    type: Union[Type, str, None] = None,
    skill_id: Optional[str] = None,
    intervals: Optional[List[Interval]] = None
)
```

The dynamic pricing settings.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`type`|**Optional\[[Type](toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig.Type.md)\]**|<p>Parameter type for calculating dynamic pricing. The SKILL value.</p>
`skill_id`|**Optional\[str\]**|<p>ID of the skill that the task price is based on</p>
`intervals`|**Optional\[List\[[Interval](toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig.Interval.md)\]\]**|<p>Skill level intervals. Must not overlap. A performer with a skill level that is not included in any interval will receive the basic price for a task suite.</p>
