# AssignmentSearchRequest
`toloka.client.search_requests.AssignmentSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/search_requests.py#L384)

```python
AssignmentSearchRequest(
    self,
    status: Union[str, Assignment.Status, List[Union[str, Assignment.Status]], None] = None,
    task_id: Optional[str] = None,
    task_suite_id: Optional[str] = None,
    pool_id: Optional[str] = None,
    user_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None,
    submitted_lt: Optional[datetime] = None,
    submitted_lte: Optional[datetime] = None,
    submitted_gt: Optional[datetime] = None,
    submitted_gte: Optional[datetime] = None,
    accepted_lt: Optional[datetime] = None,
    accepted_lte: Optional[datetime] = None,
    accepted_gt: Optional[datetime] = None,
    accepted_gte: Optional[datetime] = None,
    rejected_lt: Optional[datetime] = None,
    rejected_lte: Optional[datetime] = None,
    rejected_gt: Optional[datetime] = None,
    rejected_gte: Optional[datetime] = None,
    skipped_lt: Optional[datetime] = None,
    skipped_lte: Optional[datetime] = None,
    skipped_gt: Optional[datetime] = None,
    skipped_gte: Optional[datetime] = None,
    expired_lt: Optional[datetime] = None,
    expired_lte: Optional[datetime] = None,
    expired_gt: Optional[datetime] = None,
    expired_gte: Optional[datetime] = None
)
```

Parameters for searching assignment

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status`|**Optional\[List\[[Assignment.Status](toloka.client.assignment.Assignment.Status.md)\]\]**|<p>Status of an assigned task suite (Detailed status description in Assignment.Status):<ul><li>ACTIVE</li><li>SUBMITTED</li><li>ACCEPTED</li><li>REJECTED</li><li>SKIPPED</li><li>EXPIRED</li></ul></p>
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
