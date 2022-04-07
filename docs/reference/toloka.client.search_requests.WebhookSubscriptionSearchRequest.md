# WebhookSubscriptionSearchRequest
`toloka.client.search_requests.WebhookSubscriptionSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/search_requests.py#L903)

```python
WebhookSubscriptionSearchRequest(
    self,
    event_type: Optional[WebhookSubscription.EventType] = None,
    pool_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None
)
```

Parameters for searching webhook-subscriptions.

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
