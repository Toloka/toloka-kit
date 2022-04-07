# OSVersion
`toloka.client.filter.OSVersion` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/filter.py#L501)

```python
OSVersion(
    self,
    operator: CompareOperator,
    value: float
)
```

Use to select users by OS full version.


For example: 14.4

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[CompareOperator](toloka.client.primitives.operators.CompareOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**float**|<p>Full version of the operating system.</p>
