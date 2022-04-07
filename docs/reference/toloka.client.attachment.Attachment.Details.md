# Details
`toloka.client.attachment.Attachment.Details` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/attachment.py#L33)

```python
Details(
    self,
    *,
    user_id: Optional[str] = None,
    assignment_id: Optional[str] = None,
    pool_id: Optional[str] = None
)
```

Information about the pool, task, and user from which the file was received.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_id`|**Optional\[str\]**|<p>ID of the user from whom the file was received.</p>
`assignment_id`|**Optional\[str\]**|<p>ID for issuing a set of tasks to the user.</p>
`pool_id`|**Optional\[str\]**|<p>Pool ID.</p>
