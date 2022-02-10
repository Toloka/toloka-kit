# KnownSolution
`toloka.client.task.BaseTask.KnownSolution`

```python
KnownSolution(
    self,
    *,
    output_values: Optional[Dict[str, Any]] = None,
    correctness_weight: Optional[float] = None
)
```

Answers and hints for control and training tasks.


If several output fields are taken into account when checking, you must specify all combinations of the correct answer.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`output_values`|**Optional\[Dict\[str, Any\]\]**|<p>Correct answers in the task (for control tasks). If there are several correct answer options, for each option you need to define output_values and give the weight of the correct answer (key correctness_weight). &quot;&lt;output field id 1&gt;&quot;: &quot;&lt;correct answer value 1&gt;&quot;, &quot;&lt;output field id 2&gt;&quot;: &quot;&lt;correct answer value 2&gt;&quot;, ... &quot;&lt;output field id n&gt;&quot;: &quot;&lt;correct answer value n&gt;&quot;</p>
`correctness_weight`|**Optional\[float\]**|<p>Weight of the correct answer. Allows you to set several options for correct answers and rank them by correctness. For example, if the weight of the correct answer is 0.5, half of the error is counted to the user. The more correct the answer in correctValues, the higher its weight.</p>
