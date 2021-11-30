# MessageThreadSortItems
`toloka.client.search_requests.MessageThreadSortItems`

```
MessageThreadSortItems(self, items=None)
```

Parameters for sorting message thread search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.MessageThreadSortItems.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Thread ID in ascending order.</li><li>created - Creation date in UTC format yyyy-MM-DD (ascending).</li></ul></p>
