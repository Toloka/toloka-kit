# remove_message_thread_from_folders
`toloka.client.TolokaClient.remove_message_thread_from_folders`

```
remove_message_thread_from_folders(
    self,
    message_thread_id: str,
    folders: Union[List[Union[Folder, str]], MessageThreadFolders]
)
```

Deletes a message chain from one or more folders ("unread", "important" etc.)

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`message_thread_id`|**str**|<p>ID of message chain.</p>
`folders`|**Union\[List\[Union\[[Folder](toloka.client.message_thread.Folder.md), str\]\], [MessageThreadFolders](toloka.client.message_thread.MessageThreadFolders.md)\]**|<p> List of folders, where from to remove chain.</p>

* **Returns:**

  Full object by ID with updated folders.

* **Return type:**

  [MessageThread](toloka.client.message_thread.MessageThread.md)

**Examples:**

```python
toloka_client.remove_message_thread_from_folders(message_thread_id='1', folders=['IMPORTANT'])
```
