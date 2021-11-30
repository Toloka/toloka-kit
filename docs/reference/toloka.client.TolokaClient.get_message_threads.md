# get_message_threads
`toloka.client.TolokaClient.get_message_threads`

Finds all message threads that match certain rules and returns them in an iterable object


Unlike find_message_threads, returns generator. Does not sort threads.
While iterating over the result, several requests to the Toloka server is possible.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`folder`|**Union\[str, [Folder](toloka.client.message_thread.Folder.md), List\[Union\[str, [Folder](toloka.client.message_thread.Folder.md)\]\]\]**|<p>Folders to search for the thread</p>
`folder_ne`|**Union\[str, [Folder](toloka.client.message_thread.Folder.md), List\[Union\[str, [Folder](toloka.client.message_thread.Folder.md)\]\]\]**|<p>Folders to not search for the thread</p>
`id_lt`|**Optional\[str\]**|<p>Threads with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Threads with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Threads with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Threads with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Threads created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Threads created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Threads created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Threads created after or on the specified date.</p>

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[MessageThread](toloka.client.message_thread.MessageThread.md), None, None\]

**Examples:**

How to get all unread incoming messages.

```python
message_threads = toloka_client.get_message_threads(folder=['INBOX', 'UNREAD'])
```
