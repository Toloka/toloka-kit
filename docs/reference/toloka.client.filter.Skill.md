# Skill
`toloka.client.filter.Skill` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/filter.py#L208)

```python
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
