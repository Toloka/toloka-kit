# get_webhook_subscriptions
`toloka.client.TolokaClient.get_webhook_subscriptions`

Finds all webhook-subscriptions that match certain rules and returns them in an iterable object


Unlike find_webhook-subscriptions, returns generator. Does not sort webhook-subscriptions.
While iterating over the result, several requests to the Toloka server is possible.

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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[WebhookSubscription](toloka.client.webhook_subscription.WebhookSubscription.md), None, None\]
