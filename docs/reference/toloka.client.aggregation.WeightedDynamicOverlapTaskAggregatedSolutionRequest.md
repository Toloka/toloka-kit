# WeightedDynamicOverlapTaskAggregatedSolutionRequest
`toloka.client.aggregation.WeightedDynamicOverlapTaskAggregatedSolutionRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/aggregation.py#L75)

```python
WeightedDynamicOverlapTaskAggregatedSolutionRequest(
    self,
    *,
    task_id: Optional[str] = None,
    pool_id: Optional[str] = None,
    answer_weight_skill_id: Optional[str] = None,
    fields: Optional[List[Field]] = None
)
```

Request that allows you to run WeightedDynamicOverlap aggregation on a single task

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**Optional\[str\]**|<p>Answers for which task to aggregate.</p>
`pool_id`|**Optional\[str\]**|<p>In which pool this task.</p>
`answer_weight_skill_id`|**Optional\[str\]**|<p>A skill that determines the weight of the performer&#x27;s response.</p>
`fields`|**Optional\[List\[[Field](toloka.client.aggregation.WeightedDynamicOverlapTaskAggregatedSolutionRequest.Field.md)\]\]**|<p>Output data fields to use for aggregating responses. For best results, each of these fields must have a limited number of response options.</p>
