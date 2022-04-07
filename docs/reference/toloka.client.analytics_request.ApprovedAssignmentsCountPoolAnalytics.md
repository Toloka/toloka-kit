# ApprovedAssignmentsCountPoolAnalytics
`toloka.client.analytics_request.ApprovedAssignmentsCountPoolAnalytics` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/analytics_request.py#L101)

```python
ApprovedAssignmentsCountPoolAnalytics(self, *, subject_id: str)
```

Number of assignments in the "approved" status in the pool


Do not confuse it with the submited status.
"Submited" status means that the task was completed by the performer and send for review.
"Approved" status means that the task has passed review and money has been paid for it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`subject_id`|**str**|<p>ID of the object you want to get analytics about.</p>
