# find_app_items
`toloka.client.TolokaClient.find_app_items`

Finds all work items in the App project that match certain rules.


As a result, it returns an object that contains the first part of the found work items in the App project
and whether there are any more results.
It is better to use the "get_app_items" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`app_project_id`|**str**|<p>Project ID.</p>
`after_id`|**Optional\[str\]**|<p>ID of the item used for cursor pagination.</p>
`batch_id`|**Optional\[str\]**|<p>Batch ID.</p>
`status`|**Optional\[[AppItem.Status](toloka.client.app.AppItem.Status.md)\]**|<p>items in this status.</p>
`id_gt`|**Optional\[str\]**|<p>items with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>items with an ID greater than or equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>items with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>items with an ID less than or equal to the specified value.</p>
`created_gt`|**-**|<p>items created after the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_gte`|**-**|<p>items created after the specified date, inclusive. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lt`|**-**|<p>items created before the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lte`|**-**|<p>items created before the specified date, inclusive. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`sort`|**Union\[List\[str\], [AppItemSortItems](toloka.client.search_requests.AppItemSortItems.md), None\]**|<p>The order and direction of sorting the results.</p>
`limit`|**Optional\[int\]**|<p>number of objects per page.</p>

* **Returns:**

  The first `limit` App items in `content`. And a mark that there is more.

* **Return type:**

  [AppItemSearchResult](toloka.client.search_results.AppItemSearchResult.md)
