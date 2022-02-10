# MessageThreadSearchResult
`toloka.client.search_results.MessageThreadSearchResult`

```python
MessageThreadSearchResult(
    self,
    *,
    items: Optional[List[MessageThread]] = None,
    has_more: Optional[bool] = None
)
```

The list of found message chains and whether there is something else on the original request


It's better to use TolokaClient.get_message_threads(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[MessageThread](toloka.client.message_thread.MessageThread.md)\]\]**|<p>List of found MessageThread</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
