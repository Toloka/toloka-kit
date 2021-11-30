# WebhookSubscriptionBatchCreateResult
`toloka.client.batch_create_results.WebhookSubscriptionBatchCreateResult`

```
WebhookSubscriptionBatchCreateResult(
    self,
    *,
    items: Optional[Dict[str, WebhookSubscription]] = None,
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]] = None
)
```

The list with the results of the webhook-subscriptions creation operation.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[Dict\[str, [WebhookSubscription](toloka.client.webhook_subscription.WebhookSubscription.md)\]\]**|<p>Object with created webhook-subscriptions.</p>
`validation_errors`|**Optional\[Dict\[str, Dict\[str, [FieldValidationError](toloka.client.batch_create_results.FieldValidationError.md)\]\]\]**|<p>Object with validation errors.</p>
