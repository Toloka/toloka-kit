# patch_assignment
`toloka.client.TolokaClient.patch_assignment`

Changes status and comment on assignment


It's better to use methods "reject_assignment" and "accept_assignment".

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`assignment_id`|**str**|<p>What assignment will be affected.</p>
`public_comment`|**Optional\[str\]**|<p>Public comment about an assignment. Why it was accepted or rejected.</p>
`status`|**Optional\[[Assignment.Status](toloka.client.assignment.Assignment.Status.md)\]**|<p>Status of an assigned task suite.<ul><li>ACCEPTED - Accepted by the requester.</li><li>REJECTED - Rejected by the requester.</li></ul></p>

* **Returns:**

  Object with new status.

* **Return type:**

  [Assignment](toloka.client.assignment.Assignment.md)

**Examples:**

```python
toloka_client.patch_assignment(assignment_id='1', public_comment='Some issues present, but work is acceptable', status='ACCEPTED')
```
