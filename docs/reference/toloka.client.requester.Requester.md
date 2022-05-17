# Requester
`toloka.client.requester.Requester` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/requester.py#L9)

```python
Requester(
    self,
    *,
    id: Optional[str] = None,
    balance: Optional[Decimal] = None,
    public_name: Optional[Dict[str, str]] = None,
    company: Optional[Company] = None
)
```

Contains information about the customer and the account balance

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Requester ID.</p>
`balance`|**Optional\[Decimal\]**|<p>Account balance in dollars.</p>
`public_name`|**Optional\[Dict\[str, str\]\]**|<p>The requester&#x27;s name in Toloka.</p>
`company`|**Optional\[[Company](toloka.client.requester.Requester.Company.md)\]**|<p></p>
