# Assignment
`toloka.client.assignment.Assignment`

```python
Assignment(
    self,
    *,
    id: Optional[str] = None,
    task_suite_id: Optional[str] = None,
    pool_id: Optional[str] = None,
    user_id: Optional[str] = None,
    status: Union[Status, str, None] = None,
    reward: Optional[Decimal] = None,
    tasks: Optional[List[Task]] = None,
    automerged: Optional[bool] = None,
    created: Optional[datetime] = None,
    submitted: Optional[datetime] = None,
    accepted: Optional[datetime] = None,
    rejected: Optional[datetime] = None,
    skipped: Optional[datetime] = None,
    expired: Optional[datetime] = None,
    first_declined_solution_attempt: Optional[List[Solution]] = None,
    solutions: Optional[List[Solution]] = None,
    mixed: Optional[bool] = None,
    public_comment: Optional[str] = None
)
```

Contains information about an assigned task suite and the results

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>ID of the task suite assignment to a performer.</p>
`task_suite_id`|**Optional\[str\]**|<p>ID of a task suite.</p>
`pool_id`|**Optional\[str\]**|<p>ID of the pool that the task suite belongs to.</p>
`user_id`|**Optional\[str\]**|<p>ID of the performer who was assigned the task suite.</p>
`status`|**Optional\[[Status](toloka.client.assignment.Assignment.Status.md)\]**|<p>Status of an assigned task suite.<ul><li>ACTIVE - In the process of execution by the performer.</li><li>SUBMITTED - Completed but not checked.</li><li>ACCEPTED - Accepted by the requester.</li><li>REJECTED - Rejected by the requester.</li><li>SKIPPED - Skipped by the performer.</li><li>EXPIRED - The time for completing the tasks expired.</li></ul></p>
`reward`|**Optional\[Decimal\]**|<p>Payment received by the performer.</p>
`tasks`|**Optional\[List\[[Task](toloka.client.task.Task.md)\]\]**|<p>Data for the tasks.</p>
`automerged`|**Optional\[bool\]**|<p>Flag of the response received as a result of merging identical tasks. Value:<ul><li>True - The response was recorded when identical tasks were merged.</li><li>False - Normal performer response.</li></ul></p>
`created`|**Optional\[datetime\]**|<p>The date and time when the task suite was assigned to a performer.</p>
`submitted`|**Optional\[datetime\]**|<p>The date and time when the task suite was completed by a performer.</p>
`accepted`|**Optional\[datetime\]**|<p>The date and time when the responses for the task suite were accepted by the requester.</p>
`rejected`|**Optional\[datetime\]**|<p>The date and time when the responses for the task suite were rejected by the requester.</p>
`skipped`|**Optional\[datetime\]**|<p>The date and time when the task suite was skipped by the performer.</p>
`expired`|**Optional\[datetime\]**|<p>The date and time when the time for completing the task suite expired.</p>
`first_declined_solution_attempt`|**Optional\[List\[[Solution](toloka.client.solution.Solution.md)\]\]**|<p>For training tasks. The performer&#x27;s first responses in the training task (only if these were the wrong answers). If the performer answered correctly on the first try, the first_declined_solution_attempt array is omitted. Arrays with the responses (output_values) are arranged in the same order as the task data in the tasks array.</p>
`solutions`|**Optional\[List\[[Solution](toloka.client.solution.Solution.md)\]\]**|<p>performer responses. Arranged in the same order as the data for tasks in the tasks array.</p>
`mixed`|**Optional\[bool\]**|<p>Type of operation for creating a task suite:<ul><li>True - Automatic (&quot;smart mixing&quot;).</li><li>False - Manually.</li></ul></p>
`public_comment`|**Optional\[str\]**|<p>Public comment about an assignment. Why it was accepted or rejected.</p>
