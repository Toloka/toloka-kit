# find_apps
`toloka.client.TolokaClient.find_apps`

Finds all Apps that match certain rules.


As a result, it returns an object that contains the first part of the found Apps and whether there
are any more results.
It is better to use the "get_apps" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`after_id`|**Optional\[str\]**|<p>The ID of the App used for cursor pagination.</p>
`id_gt`|**Optional\[str\]**|<p>only with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>only with an ID greater than or equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>only with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>only with an ID less than or equal to the specified value.</p>
`name_gt`|**Optional\[str\]**|<p>only with a name lexicographically greater than the specified value.</p>
`name_gte`|**Optional\[str\]**|<p>only with a name lexicographically greater than or equal to the specified value.</p>
`name_lt`|**Optional\[str\]**|<p>only with a name lexicographically less than the specified value.</p>
`name_lte`|**Optional\[str\]**|<p>only with a name lexicographically less than or equal to the specified value.</p>
`sort`|**Union\[List\[str\], [AppSortItems](toloka.client.search_requests.AppSortItems.md), None\]**|<p>The order and direction of sorting the results.</p>
`limit`|**Optional\[int\]**|<p>number of objects per page.</p>

* **Returns:**

  The first `limit` Apps in `content`. And a mark that there is more.

* **Return type:**

  [AppSearchResult](toloka.client.search_results.AppSearchResult.md)
