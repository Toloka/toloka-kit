# AggregatedSolution
`toloka.client.aggregation.AggregatedSolution` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/aggregation.py#L95)

```python
AggregatedSolution(
    self,
    *,
    pool_id: Optional[str] = None,
    task_id: Optional[str] = None,
    confidence: Optional[float] = None,
    output_values: Optional[Dict[str, Any]] = None
)
```

Aggregated response to the task

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**Optional\[str\]**|<p>In which pool the results were aggregated.</p>
`task_id`|**Optional\[str\]**|<p>The answer for which task was aggregated.</p>
`confidence`|**Optional\[float\]**|<p>Confidence in the aggregate response.</p>
`output_values`|**Optional\[Dict\[str, Any\]\]**|<p>Output data fields and aggregate response.</p>
