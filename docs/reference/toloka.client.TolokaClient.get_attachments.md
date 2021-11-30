# get_attachments
`toloka.client.TolokaClient.get_attachments`

Finds all attachments that match certain rules and returns their metadata in an iterable object


Unlike find_attachments, returns generator. Does not sort attachments.
While iterating over the result, several requests to the Toloka server is possible.

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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[Attachment](toloka.client.attachment.Attachment.md), None, None\]

**Examples:**

Make a list of all received attachments in the specified pool.

```python
results_list = [attachment for attachment in toloka_client.get_attachments(pool_id='1')]
```
