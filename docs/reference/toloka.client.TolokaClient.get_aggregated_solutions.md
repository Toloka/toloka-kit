# get_aggregated_solutions
`toloka.client.TolokaClient.get_aggregated_solutions`

Finds all aggregated responses after the AggregatedSolutionOperation completes


**Note**: In all aggregation purposes we are strongly recommending using our crowd-kit library, that have more aggregation
methods and can perform on your computers: [https://github.com/Toloka/crowd-kit](https://github.com/Toloka/crowd-kit)

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operation_id`|**str**|<p>From what aggregation operation you want to get results.</p>
`task_id_lt`|**Optional\[str\]**|<p>Jobs with an ID greater than the specified value.</p>
`task_id_lte`|**Optional\[str\]**|<p>Jobs with an ID greater than or equal to the specified value.</p>
`task_id_gt`|**Optional\[str\]**|<p>Jobs with an ID less than the specified value.</p>
`task_id_gte`|**Optional\[str\]**|<p>Jobs with an ID less than or equal to the specified value.</p>

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[AggregatedSolution](toloka.client.aggregation.AggregatedSolution.md), None, None\]

**Examples:**

How to get all aggregated solutions from pool.

```python
aggregation_results = list(toloka_client.get_aggregated_solutions(aggregation_operation.id))
```
