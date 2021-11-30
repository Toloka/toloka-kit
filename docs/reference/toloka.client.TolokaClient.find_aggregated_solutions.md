# find_aggregated_solutions
`toloka.client.TolokaClient.find_aggregated_solutions`

Gets aggregated responses after the AggregatedSolutionOperation completes.


It is better to use the "get_aggregated_solutions" method, that allows to iterate through all results.

**Note**: In all aggregation purposes we are strongly recommending using our [crowd-kit library](https://github.com/Toloka/crowd-kit),
that have more aggregation methods and can perform on your computers.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operation_id`|**str**|<p>From what aggregation operation you want to get results.</p>
`task_id_lt`|**Optional\[str\]**|<p>Jobs with an ID greater than the specified value.</p>
`task_id_lte`|**Optional\[str\]**|<p>Jobs with an ID greater than or equal to the specified value.</p>
`task_id_gt`|**Optional\[str\]**|<p>Jobs with an ID less than the specified value.</p>
`task_id_gte`|**Optional\[str\]**|<p>Jobs with an ID less than or equal to the specified value.</p>
`sort`|**Union\[List\[str\], [AggregatedSolutionSortItems](toloka.client.search_requests.AggregatedSolutionSortItems.md), None\]**|<p>How to sort results. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned. The maximum is 100,000. Defaults to None, in which case it returns first 50 results.</p>

* **Returns:**

  The first `limit` solutions in `items`. And a mark that there is more.

* **Return type:**

  [AggregatedSolutionSearchResult](toloka.client.search_results.AggregatedSolutionSearchResult.md)

**Examples:**

How to get all aggregated solutions from pool.

```python
current_result = toloka_client.find_aggregated_solutions(aggregation_operation.id)
aggregation_results = current_result.items
while current_result.has_more:
    current_result = toloka_client.find_aggregated_solutions(
        aggregation_operation.id,
        task_id_gt=current_result.items[len(current_result.items) - 1].task_id,
    )
    aggregation_results = aggregation_results + current_result.items
print(len(aggregation_results))
```
