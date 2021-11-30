# get_lines
`toloka.metrics.metrics.BaseMetric.get_lines`

```
get_lines(self)
```

Gather and return metrics


All metrics returned in the same format: named list, contain pairs of: datetime of some event, metric value.
Could not return some metrics in dict on iteration or return it with empty list:
means that is nothing being gathered on this step. This is not zero value!

Return example:
{
    'rejected_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 44, 895232), 0)],
    'submitted_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 45, 321904), 75)],
    'accepted_assignments_in_pool': [(datetime.datetime(2021, 8, 12, 10, 4, 45, 951156), 75)],
    'accepted_events_in_pool': [(datetime.datetime(2021, 8, 11, 15, 13, 3, 65000), 1), ... ],
    'rejected_events_in_pool': [],
    # no toloka_requester_balance on this iteration
}

