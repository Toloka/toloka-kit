# find_attachments
`toloka.client.TolokaClient.find_attachments`

Finds all attachments that match certain rules


As a result, it returns an object that contains the first part of the found attachments and whether there
are any more results.
It is better to use the "get_attachments" method, they allow to iterate trought all results
and not just the first output.

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
`sort`|**Union\[List\[str\], [AttachmentSortItems](toloka.client.search_requests.AttachmentSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned. The maximum is 100,000. Defaults to None, in which case it returns first 50 results.</p>

* **Returns:**

  The first `limit` assignments in `items`. And a mark that there is more.

* **Return type:**

  [AttachmentSearchResult](toloka.client.search_results.AttachmentSearchResult.md)

**Examples:**

Let's find attachments in the pool and sort them by id and date of creation.

```python
toloka_client.find_attachments(pool_id='1', sort=['-created', '-id'], limit=10)
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
