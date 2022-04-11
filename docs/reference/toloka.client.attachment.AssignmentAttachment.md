# AssignmentAttachment
`toloka.client.attachment.AssignmentAttachment` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/attachment.py#L55)

```python
AssignmentAttachment(
    self,
    *,
    id: Optional[str] = None,
    name: Optional[str] = None,
    details: Optional[Attachment.Details] = None,
    created: Optional[datetime] = None,
    media_type: Optional[str] = None,
    owner: Optional[Owner] = None
)
```

Assignment Attachment.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>File ID.</p>
`name`|**Optional\[str\]**|<p>File name.</p>
`details`|**Optional\[[Attachment.Details](toloka.client.attachment.Attachment.Details.md)\]**|<p>Infomation about the pool, the task, and the user who uploaded the file.</p>
`created`|**Optional\[datetime\]**|<p>Date the file was uploaded to Toloka.</p>
`media_type`|**Optional\[str\]**|<p>MIME data type.</p>
`owner`|**Optional\[[Owner](toloka.client.owner.Owner.md)\]**|<p>Owner</p>
