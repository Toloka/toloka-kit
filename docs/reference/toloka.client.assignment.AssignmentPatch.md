# AssignmentPatch
`toloka.client.assignment.AssignmentPatch`

```
AssignmentPatch(
    self,
    *,
    public_comment: Optional[str] = None,
    status: Optional[Assignment.Status] = None
)
```

Allows you to accept or reject tasks, and leave a comment


Used in "TolokaClient.patch_assignment" method.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`public_comment`|**Optional\[str\]**|<p>Public comment about an assignment. Why it was accepted or rejected.</p>
`status`|**Optional\[[Assignment.Status](toloka.client.assignment.Assignment.Status.md)\]**|<p>Status of an assigned task suite.<ul><li>ACCEPTED - Accepted by the requester.</li><li>REJECTED - Rejected by the requester.</li></ul></p>
