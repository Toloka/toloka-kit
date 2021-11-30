# Interval
`toloka.client.task_distribution_function.TaskDistributionFunction.Interval`

```
Interval(
    self,
    *,
    from_: Optional[int] = None,
    to: Optional[int] = None,
    frequency: Optional[int] = None
)
```

Interval borders and number of tasks in an interval

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`from_`|**Optional\[int\]**|<p>Start of the interval (number of task completed by the user in the project or in the pool).</p>
`to`|**Optional\[int\]**|<p>End of the interval (number of task completed by the user in the project or in the pool).</p>
`frequency`|**Optional\[int\]**|<p>Frequency of tasks in an interval. The first task in an interval is a distributed task. For example, if you set frequency: 3 tasks number 1, 4, 7 and so on will be distributed tasks.</p>
