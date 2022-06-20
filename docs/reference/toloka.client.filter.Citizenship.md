# Citizenship
`toloka.client.filter.Citizenship` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/filter.py#L256)

```python
Citizenship(
    self,
    operator: IdentityOperator,
    value: str
)
```

Use to select users by citizenship.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[IdentityOperator](toloka.client.primitives.operators.IdentityOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**str**|<p>User citizenship (two-letter country code) ISO 3166-1 alpha-2</p>
