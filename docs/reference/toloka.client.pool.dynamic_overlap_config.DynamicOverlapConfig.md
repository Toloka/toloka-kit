# DynamicOverlapConfig
`toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/pool/dynamic_overlap_config.py#L9)

```python
DynamicOverlapConfig(
    self,
    *,
    type: Union[Type, str, None] = None,
    max_overlap: Optional[int] = None,
    min_confidence: Optional[float] = None,
    answer_weight_skill_id: Optional[str] = None,
    fields: Optional[List[Field]] = None
)
```

Dynamic overlap setting.


Allows you to change the overlap depending on how well the performers handle the task.
Set the closing interval (auto_close_after_complete_delay_seconds). It should be enough to complete tasks
with an overlap higher than the minimum.
When all pool tasks are completed, aggregate the responses.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`type`|**Optional\[[Type](toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig.Type.md)\]**|<p>The algorithm for dynamic overlap.</p>
`max_overlap`|**Optional\[int\]**|<p>Maximum overlap. Must be higher than the values in defaults. Minimum — 1. Maximum — 30000.</p>
`min_confidence`|**Optional\[float\]**|<p>Minimum confidence of the aggregated response. Values from 0 to 1.</p>
`answer_weight_skill_id`|**Optional\[str\]**|<p>A skill that determines the weight of the performer&#x27;s response. For best results, use a skill calculated as percentage of correct responses in control tasks.</p>
`fields`|**Optional\[List\[[Field](toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig.Field.md)\]\]**|<p>Output data fields to use for aggregating responses.</p>
