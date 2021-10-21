# WebhookSubscriptionSortItems
`toloka.client.search_requests.WebhookSubscriptionSortItems`

```
WebhookSubscriptionSortItems(self, items=None)
```

Parameters for sorting webhook-subscriptions search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Subscription ID (in ascending order).</li><li>created - Date of creation of the subscription in UTC in the format YYYY-MM-DD (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.WebhookSubscriptionSortItems(['-created', 'id'])
result = toloka_client.find_webhook_subscriptions(event_type=some_event_type, pool_id=my_pretty_pool_id, sort=sort, limit=10)
```
