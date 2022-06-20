# AttachmentSearchResult
`toloka.client.search_results.AttachmentSearchResult`

```python
AttachmentSearchResult(
    self,
    *,
    items: Optional[List[Attachment]] = None,
    has_more: Optional[bool] = None
)
```

The list of found attachments and whether there is something else on the original request


It's better to use TolokaClient.get_attachments(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[Attachment](toloka.client.attachment.Attachment.md)\]\]**|<p>List of found Attachment</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
