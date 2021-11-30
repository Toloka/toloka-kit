# aggregate_solutions_by_pool
`toloka.client.TolokaClient.aggregate_solutions_by_pool`

Starts aggregation of solutions in the pool


Responses to all completed tasks will be aggregated.
The method only starts the aggregation and returns the operation for further tracking.

**Note**: In all aggregation purposes we are strongly recommending using our [crowd-kit library](https://github.com/Toloka/crowd-kit),
that have more aggregation methods and can perform on your computers.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`type`|**Union\[[AggregatedSolutionType](toloka.client.aggregation.AggregatedSolutionType.md), str, None\]**|<p>Aggregation type. WEIGHTED_DYNAMIC_OVERLAP - Aggregation of responses in a pool with dynamic overlap. DAWID_SKENE - Dawid-Skene aggregation model.     A. Philip Dawid and Allan M. Skene. 1979.     Maximum Likelihood Estimation of Observer Error-Rates Using the EM Algorithm.     Journal of the Royal Statistical Society. Series C (Applied Statistics), Vol. 28, 1 (1979), 20–28.     [https://doi.org/10.2307/2346806](https://doi.org/10.2307/2346806)</p>
`pool_id`|**Optional\[str\]**|<p>In which pool to aggregate the results.</p>
`answer_weight_skill_id`|**Optional\[str\]**|<p>A skill that determines the weight of the performer&#x27;s response.</p>
`fields`|**Optional\[List\[[PoolAggregatedSolutionRequest.Field](toloka.client.aggregation.PoolAggregatedSolutionRequest.Field.md)\]\]**|<p>Output data fields to use for aggregating responses. For best results, each of these fields must have a limited number of response options.</p>

* **Returns:**

  An operation upon completion of which you can get the results of the aggregation.

* **Return type:**

  [AggregatedSolutionOperation](toloka.client.operations.AggregatedSolutionOperation.md)

**Examples:**

How to start aggregating solutions by pool.

```python
aggregation_operation = toloka_client.aggregate_solutions_by_pool(
        type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
        pool_id=some_existing_pool_id,   # Aggregate in this pool
        answer_weight_skill_id=some_skill_id,   # Aggregate by this skill
        fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]  # Aggregate this field
    )
aggregation_operation = toloka_client.wait_operation(aggregation_operation)
```
