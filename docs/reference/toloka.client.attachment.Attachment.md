# Attachment
`toloka.client.attachment.Attachment`

```
Attachment(
    self,
    *,
    id: Optional[str] = None,
    name: Optional[str] = None,
    details: Optional[Details] = None,
    created: Optional[datetime] = None,
    media_type: Optional[str] = None,
    owner: Optional[Owner] = None
)
```

Attachment


Files uploaded by users are saved in Toloka.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>File ID.</p>
`name`|**Optional\[str\]**|<p>File name.</p>
`details`|**Optional\[[Details](toloka.client.attachment.Attachment.Details.md)\]**|<p>Infomation about the pool, the task, and the user who uploaded the file.</p>
`created`|**Optional\[datetime\]**|<p>Date the file was uploaded to Toloka.</p>
`media_type`|**Optional\[str\]**|<p>MIME data type.</p>
`owner`|**Optional\[[Owner](toloka.client.owner.Owner.md)\]**|<p>Owner</p>
