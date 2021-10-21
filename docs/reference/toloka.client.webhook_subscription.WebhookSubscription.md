# WebhookSubscription
`toloka.client.webhook_subscription.WebhookSubscription`

```
WebhookSubscription(
    self,
    *,
    webhook_url: Optional[str] = None,
    event_type: Union[EventType, str, None] = None,
    pool_id: Optional[str] = None,
    secret_key: Optional[str] = None,
    id: Optional[str] = None,
    created: Optional[datetime] = None
)
```

Webhook subscription to make a callback to the given address when some event happen.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`webhook_url`|**Optional\[str\]**|<p>The URL to which notifications will be sent.</p>
`event_type`|**Optional\[[EventType](toloka.client.webhook_subscription.WebhookSubscription.EventType.md)\]**|<p>Event type.</p>
`pool_id`|**Optional\[str\]**|<p>ID of the pool for which the subscription was created.</p>
`id`|**Optional\[str\]**|<p>Pool ID. Read only field.</p>
`created`|**Optional\[datetime\]**|<p>When this pool was created. Read only field.</p>
