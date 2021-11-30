# find_webhook_subscriptions
`toloka.client.TolokaClient.find_webhook_subscriptions`

Finds all webhook-subscriptions that match certain rules


As a result, it returns an object that contains the first part of the found webhook-subscriptions
and whether there are any more results.
It is better to use the "get_webhook_subscriptions" method, they allow to iterate through all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`event_type`|**Optional\[[WebhookSubscription.EventType](toloka.client.webhook_subscription.WebhookSubscription.EventType.md)\]**|<p>Event type.</p>
`pool_id`|**Optional\[str\]**|<p>ID of the pool for which subscription information is requested.</p>
`id_lt`|**Optional\[str\]**|<p>Subscriptions with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Subscriptions with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Subscriptions with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Subscriptions with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Subscriptions created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Subscriptions created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Subscriptions created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Subscriptions created after or on the specified date.</p>
`sort`|**Union\[List\[str\], [WebhookSubscriptionSortItems](toloka.client.search_requests.WebhookSubscriptionSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned. The maximum is 100 000. Defaults to None, in which case it returns first 50 results.</p>

* **Returns:**

  The first `limit` webhook-subscriptions in `items`.
And a mark that there is more.

* **Return type:**

  [WebhookSubscriptionSearchResult](toloka.client.search_results.WebhookSubscriptionSearchResult.md)
