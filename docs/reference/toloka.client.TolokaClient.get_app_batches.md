# get_app_batches
`toloka.client.TolokaClient.get_app_batches`

Finds all batches in the App project that match certain rules and returns them in an iterable object.


Unlike find_app_batches, returns generator. Does not sort batches in the App project.
While iterating over the result, several requests to the Toloka server is possible.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[AppBatch](toloka.client.app.AppBatch.md), None, None\]
