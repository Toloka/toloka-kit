# Skill
`toloka.client.filter.Skill`

```
Skill(
    self,
    key: str,
    operator: CompareOperator = CompareOperator.EQ,
    value: Optional[float] = None
)
```

Use to select users by skill value.


To select users without a skill set the parameter value operator=CompareOperator.EQ and exclude the parameter value.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`key`|**str**|<p>Skill ID.</p>
`operator`|**[CompareOperator](toloka.client.primitives.operators.CompareOperator.md)**|<p>Comparison operator in the condition.</p>
`value`|**Optional\[float\]**|<p>Attribute value from the field key.</p>
