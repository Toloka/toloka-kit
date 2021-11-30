# ClientType
`toloka.client.filter.ClientType`

```
ClientType(
    self,
    operator: IdentityOperator,
    value: Union[ClientType, str]
)
```

Use to select users by their application type.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[IdentityOperator](toloka.client.primitives.operators.IdentityOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**[ClientType](toloka.client.filter.ClientType.ClientType.md)**|<p>Client application type.</p>
