# UserAgentType
`toloka.client.filter.UserAgentType`

```
UserAgentType(
    self,
    operator: IdentityOperator,
    value: Union[UserAgentType, str]
)
```

Use to select users by user agent type:

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[IdentityOperator](toloka.client.primitives.operators.IdentityOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**[UserAgentType](toloka.client.filter.UserAgentType.UserAgentType.md)**|<p>User agent type.</p>
