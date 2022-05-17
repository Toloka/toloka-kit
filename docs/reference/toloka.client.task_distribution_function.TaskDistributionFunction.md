# TaskDistributionFunction
`toloka.client.task_distribution_function.TaskDistributionFunction` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/task_distribution_function.py#L9)

```python
TaskDistributionFunction(
    self,
    *,
    scope: Union[Scope, str, None] = None,
    distribution: Union[Distribution, str, None] = None,
    window_days: Optional[int] = None,
    intervals: Optional[List[Interval]] = None
)
```

Issue of tasks with uneven frequency


Can be used for:
- Distribution of tasks with majority opinion verification.
- Issuing control tasks with uneven frequency. Allows you to change the frequency of verification as the user completes tasks.
- Issuing training tasks with uneven frequency. Allows you to change the frequency of training tasks as the user completes tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`scope`|**Optional\[[Scope](toloka.client.task_distribution_function.TaskDistributionFunction.Scope.md)\]**|<p>How to count tasks completed by the user:<ul><li>POOL - Count completed pool tasks.</li><li>PROJECT - Count completed project tasks.</li></ul></p>
`distribution`|**Optional\[[Distribution](toloka.client.task_distribution_function.TaskDistributionFunction.Distribution.md)\]**|<p>Distribution of tasks within an interval. Parameter has only one possible: value - UNIFORM.</p>
`window_days`|**Optional\[int\]**|<p>Period in which completed tasks are counted (number of days).</p>
`intervals`|**Optional\[List\[[Interval](toloka.client.task_distribution_function.TaskDistributionFunction.Interval.md)\]\]**|<p>Interval borders and number of tasks in an interval.</p>
