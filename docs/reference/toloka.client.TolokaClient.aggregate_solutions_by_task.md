# aggregate_solutions_by_task
`toloka.client.TolokaClient.aggregate_solutions_by_task`

Starts aggregation of solutions to a single task


The method only starts the aggregation and returns the operation for further tracking.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**Optional\[str\]**|<p>Answers for which task to aggregate.</p>
`pool_id`|**Optional\[str\]**|<p>In which pool this task.</p>
`answer_weight_skill_id`|**Optional\[str\]**|<p>A skill that determines the weight of the performer&#x27;s response.</p>
`fields`|**Optional\[List\[[WeightedDynamicOverlapTaskAggregatedSolutionRequest.Field](toloka.client.aggregation.WeightedDynamicOverlapTaskAggregatedSolutionRequest.Field.md)\]\]**|<p>Output data fields to use for aggregating responses. For best results, each of these fields must have a limited number of response options.</p>

* **Returns:**

  Result of aggregation. Also contains input parameters and result confidence.

* **Return type:**

  [AggregatedSolution](toloka.client.aggregation.AggregatedSolution.md)

**Examples:**

How to aggregate solutions to a task.

```python
aggregation_operation = toloka_client.aggregate_solutions_by_task(
        type=toloka.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
        pool_id=some_existing_pool_id,   # Task in this pool
        task_id=some_existing_task_id,   # Aggregate on this task
        answer_weight_skill_id=some_skill_id,   # Aggregate by this skill
        fields=[toloka.aggregation.PoolAggregatedSolutionRequest.Field(name='result')]  # Aggregate this field
    )
print(aggregation_operation.output_values['result'])
```
