# SubmitedAssignmentsCountPoolAnalytics
`toloka.client.analytics_request.SubmitedAssignmentsCountPoolAnalytics` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/analytics_request.py#L76)

```python
SubmitedAssignmentsCountPoolAnalytics(self, *, subject_id: str)
```

Number of assignments in the "submited" status in the pool


Do not confuse it with the approved status.
"Submited" status means that the task was completed by the performer and send for review.
"Approved" status means that the task has passed review and money has been paid for it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`subject_id`|**str**|<p>ID of the object you want to get analytics about.</p>
