# find_app_batches
`toloka.client.TolokaClient.find_app_batches`

Finds all batches in the App project that match certain rules.


As a result, it returns an object that contains the first part of the found batches in the App project
and whether there are any more results.
It is better to use the "get_app_batches" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`app_project_id`|**str**|<p>Project ID.</p>
`after_id`|**Optional\[str\]**|<p>ID of the batch used for cursor pagination</p>
`status`|**Optional\[[AppBatch.Status](toloka.client.app.AppBatch.Status.md)\]**|<p>batches with this status.</p>
`id_gt`|**Optional\[str\]**|<p>batches with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>batches with an ID greater than or equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>batches with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>batches with an ID less than or equal to the specified value.</p>
`name_gt`|**Optional\[str\]**|<p>batches with the name lexicographically greater than the specified value.</p>
`name_gte`|**Optional\[str\]**|<p>batches with a name lexicographically greater than or equal to the specified value.</p>
`name_lt`|**Optional\[str\]**|<p>batches with a name lexicographically less than the specified value.</p>
`name_lte`|**Optional\[str\]**|<p>batches with a name lexicographically less than or equal to the specified value.</p>
`created_gt`|**-**|<p>batches created after the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_gte`|**-**|<p>batches created after the specified date, inclusive. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lt`|**-**|<p>batches created before the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lte`|**-**|<p>batches created before the specified date, inclusive. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`sort`|**Union\[List\[str\], [AppBatchSortItems](toloka.client.search_requests.AppBatchSortItems.md), None\]**|<p>The order and direction of sorting the results.</p>
`limit`|**Optional\[int\]**|<p>number of objects per page.</p>

* **Returns:**

  The first `limit` batches in `content`. And a mark that there is more.

* **Return type:**

  [AppBatchSearchResult](toloka.client.search_results.AppBatchSearchResult.md)
