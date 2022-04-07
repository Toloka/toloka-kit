# WebhookSubscriptionSearchResult
`toloka.client.search_results.WebhookSubscriptionSearchResult`

```python
WebhookSubscriptionSearchResult(
    self,
    *,
    items: Optional[List[WebhookSubscription]] = None,
    has_more: Optional[bool] = None
)
```

The list of found subscriptions and whether there is something else on the original request


It's better to use TolokaClient.get_webhook_subscriptions(),
which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[WebhookSubscription](toloka.client.webhook_subscription.WebhookSubscription.md)\]\]**|<p>List of found subscriptions</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
