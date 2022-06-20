# find_assignments
`toloka.client.TolokaClient.find_assignments`

Finds all assignments that match certain rules


As a result, it returns an object that contains the first part of the found assignments and whether there
are any more results.
It is better to use the "get_assignments" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status`|**Union\[str, [Assignment.Status](toloka.client.assignment.Assignment.Status.md), List\[Union\[str, [Assignment.Status](toloka.client.assignment.Assignment.Status.md)\]\], None\]**|<p>Status of an assigned task suite (Detailed status description in Assignment.Status):<ul><li>ACTIVE</li><li>SUBMITTED</li><li>ACCEPTED</li><li>REJECTED</li><li>SKIPPED</li><li>EXPIRED</li></ul></p>
`task_id`|**Optional\[str\]**|<p>The task ID in suites generated automatically using &quot;smart mixing&quot;. You will get responses for task suites that contain the specified task.</p>
`task_suite_id`|**Optional\[str\]**|<p>ID of a task suite.</p>
`pool_id`|**Optional\[str\]**|<p>Pool ID.</p>
`user_id`|**Optional\[str\]**|<p>Performer ID.</p>
`id_lt`|**Optional\[str\]**|<p>Task suites with an assignment ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Task suites with an assignment ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Task suites with an assignment ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Task suites with an assignment ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Task suites assigned before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Task suites assigned before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Task suites assigned after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Task suites assigned after or on the specified date.</p>
`submitted_lt`|**Optional\[datetime\]**|<p>Task suites completed before the specified date.</p>
`submitted_lte`|**Optional\[datetime\]**|<p>Task suites completed before or on the specified date.</p>
`submitted_gt`|**Optional\[datetime\]**|<p>Task suites completed after the specified date.</p>
`submitted_gte`|**Optional\[datetime\]**|<p>Task suites completed after or on the specified date.</p>
`accepted_lt`|**Optional\[datetime\]**|<p>Task suites accepted before the specified date.</p>
`accepted_lte`|**Optional\[datetime\]**|<p>Task suites accepted before or on the specified date.</p>
`accepted_gt`|**Optional\[datetime\]**|<p>Task suites accepted after the specified date.</p>
`accepted_gte`|**Optional\[datetime\]**|<p>Task suites accepted after or on the specified date.</p>
`rejected_lt`|**Optional\[datetime\]**|<p>Task suites rejected before the specified date.</p>
`rejected_lte`|**Optional\[datetime\]**|<p>Task suites rejected before or on the specified date.</p>
`rejected_gt`|**Optional\[datetime\]**|<p>Task suites rejected after the specified date.</p>
`rejected_gte`|**Optional\[datetime\]**|<p>Task suites rejected after or on the specified date.</p>
`skipped_lt`|**Optional\[datetime\]**|<p>Task suites skipped before the specified date.</p>
`skipped_lte`|**Optional\[datetime\]**|<p>Task suites skipped before or on the specified date.</p>
`skipped_gt`|**Optional\[datetime\]**|<p>Task suites skipped after the specified date.</p>
`skipped_gte`|**Optional\[datetime\]**|<p>Task suites skipped after or on the specified date.</p>
`expired_lt`|**Optional\[datetime\]**|<p>Task suites expired before the specified date.</p>
`expired_lte`|**Optional\[datetime\]**|<p>Task suites expired before or on the specified date.</p>
`expired_gt`|**Optional\[datetime\]**|<p>Task suites expired after the specified date.</p>
`expired_gte`|**Optional\[datetime\]**|<p>Task suites expired after or on the specified date.</p>
`sort`|**Union\[List\[str\], [AssignmentSortItems](toloka.client.search_requests.AssignmentSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of assignments returned. The maximum is 100,000. Defaults to None, in which case it returns first 50 results.</p>

* **Returns:**

  The first `limit` assignments in `items`. And a mark that there is more.

* **Return type:**

  [AssignmentSearchResult](toloka.client.search_results.AssignmentSearchResult.md)

**Examples:**

Search for `SKIPPED` or `EXPIRED` assignments in the specified pool.

```python
toloka_client.find_assignments(pool_id='1', status = ['SKIPPED', 'EXPIRED'])
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
