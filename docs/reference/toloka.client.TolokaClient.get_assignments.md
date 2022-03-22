# get_assignments
`toloka.client.TolokaClient.get_assignments`

Finds all assignments that match certain rules and returns them in an iterable object


Unlike find_assignments, returns generator. Does not sort assignments.
While iterating over the result, several requests to the Toloka server is possible.

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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[Assignment](toloka.client.assignment.Assignment.md), None, None\]

**Examples:**

Let’s make a list of `assignment_id` of all `SUBMITTED` assignments in the specified pool.

```python
from toloka.client import Assignment
assignments = toloka_client.get_assignments(pool_id='1', status=Assignment.SUBMITTED)
result_list = [assignment.id for assignment in assignments]
```
