# AttachmentSortItems
`toloka.client.search_requests.AttachmentSortItems`

```
AttachmentSortItems(self, items=None)
```

Parameters for sorting attachment search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.AttachmentSortItems.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - File ID in ascending order.</li><li>created - Date of sending the file in UTC in the yyyy-MM-DD format (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.AttachmentSortItems(['-created', 'id'])
result = toloka_client.find_attachments(pool_id=my_pretty_pool_id, sort=sort, limit=10)
```
