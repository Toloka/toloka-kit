# PoolAggregatedSolutionRequest
`toloka.client.aggregation.PoolAggregatedSolutionRequest`

```
PoolAggregatedSolutionRequest(
    self,
    *,
    type: Union[AggregatedSolutionType, str, None] = None,
    pool_id: Optional[str] = None,
    answer_weight_skill_id: Optional[str] = None,
    fields: Optional[List[Field]] = None
)
```

Request that allows you to aggregate results in a specific pool


Responses to all completed tasks will be aggregated.
See an example of how to use it in "TolokaClient.aggregate_solutions_by_pool".

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`type`|**Optional\[[AggregatedSolutionType](toloka.client.aggregation.AggregatedSolutionType.md)\]**|<p>Aggregation type. WEIGHTED_DYNAMIC_OVERLAP - Aggregation of responses in a pool with dynamic overlap. DAWID_SKENE - Dawid-Skene aggregation model.     A. Philip Dawid and Allan M. Skene. 1979.     Maximum Likelihood Estimation of Observer Error-Rates Using the EM Algorithm.     Journal of the Royal Statistical Society. Series C (Applied Statistics), Vol. 28, 1 (1979), 20–28.     [https://doi.org/10.2307/2346806](https://doi.org/10.2307/2346806)</p>
`pool_id`|**Optional\[str\]**|<p>In which pool to aggregate the results.</p>
`answer_weight_skill_id`|**Optional\[str\]**|<p>A skill that determines the weight of the performer&#x27;s response.</p>
`fields`|**Optional\[List\[[Field](toloka.client.aggregation.PoolAggregatedSolutionRequest.Field.md)\]\]**|<p>Output data fields to use for aggregating responses. For best results, each of these fields must have a limited number of response options.</p>
