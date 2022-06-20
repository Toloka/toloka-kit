# find_message_threads
`toloka.client.TolokaClient.find_message_threads`

Finds all message threads that match certain rules


As a result, it returns an object that contains the first part of the found threads and whether there
are any more results.
It is better to use the "get_message_threads" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`folder`|**Union\[str, [Folder](toloka.client.message_thread.Folder.md), List\[Union\[str, [Folder](toloka.client.message_thread.Folder.md)\]\], None\]**|<p>Folders to search for the thread</p>
`folder_ne`|**Union\[str, [Folder](toloka.client.message_thread.Folder.md), List\[Union\[str, [Folder](toloka.client.message_thread.Folder.md)\]\], None\]**|<p>Folders to not search for the thread</p>
`id_lt`|**Optional\[str\]**|<p>Threads with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Threads with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Threads with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Threads with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Threads created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Threads created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Threads created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Threads created after or on the specified date.</p>
`sort`|**Union\[List\[str\], [MessageThreadSortItems](toloka.client.search_requests.MessageThreadSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned. The maximum is 300. Defaults to None, in which case it returns first 50 results.</p>

* **Returns:**

  The first `limit` message threads in `items`.
And a mark that there is more.

* **Return type:**

  [MessageThreadSearchResult](toloka.client.search_results.MessageThreadSearchResult.md)

**Examples:**

Find all message threads in the Inbox folder.

```python
toloka_client.find_message_threads(folder='INBOX')
```
