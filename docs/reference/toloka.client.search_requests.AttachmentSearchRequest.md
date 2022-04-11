# AttachmentSearchRequest
`toloka.client.search_requests.AttachmentSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/search_requests.py#L630)

```python
AttachmentSearchRequest(
    self,
    name: Optional[str] = None,
    type: Optional[Attachment.Type] = None,
    user_id: Optional[str] = None,
    assignment_id: Optional[str] = None,
    pool_id: Optional[str] = None,
    owner_id: Optional[str] = None,
    owner_company_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None
)
```

Parameters for searching attachment

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`name`|**Optional\[str\]**|<p>File name.</p>
`type`|**Optional\[[Attachment.Type](toloka.client.attachment.Attachment.Type.md)\]**|<p>Attachment type. Currently the key can have only one value - ASSIGNMENT_ATTACHMENT.</p>
`user_id`|**Optional\[str\]**|<p>ID of the user who uploaded the file(s).</p>
`assignment_id`|**Optional\[str\]**|<p>Assignment ID.</p>
`pool_id`|**Optional\[str\]**|<p>Pool ID.</p>
`owner_id`|**Optional\[str\]**|<p>Optional[str]</p>
`owner_company_id`|**Optional\[str\]**|<p>Optional[str]</p>
`id_lt`|**Optional\[str\]**|<p>Files with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Files with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Files with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Files with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Files uploaded by users before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Files uploaded by users before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Files uploaded by users after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Files uploaded by users after or on the specified date.</p>
