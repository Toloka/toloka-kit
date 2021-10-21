# get_apps
`toloka.client.TolokaClient.get_apps`

Finds all Apps that match certain rules and returns them in an iterable object.


Unlike find_apps, returns generator. Does not sort Apps.
While iterating over the result, several requests to the Toloka server is possible.

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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[App](toloka.client.app.App.md), None, None\]
