# OSVersionMajor
`toloka.client.filter.OSVersionMajor` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/filter.py#L513)

```python
OSVersionMajor(
    self,
    operator: CompareOperator,
    value: int
)
```

Use to select users by OS major version.


For example: 14

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[CompareOperator](toloka.client.primitives.operators.CompareOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**int**|<p>Major version of the operating system.</p>
