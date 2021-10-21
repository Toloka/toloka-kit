# Owner
`toloka.client.owner.Owner`

```
Owner(
    self,
    *,
    id: Optional[str] = None,
    myself: Optional[bool] = None,
    company_id: Optional[str] = None
)
```

Parameters of the customer who created an object.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Customer ID.</p>
`myself`|**Optional\[bool\]**|<p>An object accessory marker. Possible values:<ul><li>True - an object created by the customer whose OAuth-токен in the request;</li><li>False - an object does not belong to the customer whose OAuth-токен in the request.</li></ul></p>
`company_id`|**Optional\[str\]**|<p>ID of the customer&#x27;s company.</p>
