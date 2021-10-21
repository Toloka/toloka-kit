# get_app_items
`toloka.client.TolokaClient.get_app_items`

Finds all work items in the App project that match certain rules and returns them in an iterable object.


Unlike find_app_items, returns generator. Does not sort work items in the App project.
While iterating over the result, several requests to the Toloka server is possible.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[AppItem](toloka.client.app.AppItem.md), None, None\]
