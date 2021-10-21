# MessageThreadSearchRequest
`toloka.client.search_requests.MessageThreadSearchRequest`

```
MessageThreadSearchRequest(
    self,
    folder: Union[str, Folder, List[Union[str, Folder]]] = None,
    folder_ne: Union[str, Folder, List[Union[str, Folder]]] = None,
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

Parameters for searching message threads

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`folder`|**Optional\[List\[[Folder](toloka.client.message_thread.Folder.md)\]\]**|<p>Folders to search for the thread</p>
`folder_ne`|**Optional\[List\[[Folder](toloka.client.message_thread.Folder.md)\]\]**|<p>Folders to not search for the thread</p>
`id_lt`|**Optional\[str\]**|<p>Threads with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Threads with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Threads with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Threads with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Threads created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Threads created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Threads created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Threads created after or on the specified date.</p>
