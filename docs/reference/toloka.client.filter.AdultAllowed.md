# AdultAllowed
`toloka.client.filter.AdultAllowed` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/filter.py#L291)

```python
AdultAllowed(
    self,
    operator: IdentityOperator,
    value: bool
)
```

Use to select users by their agreement to perform tasks that contain adult content.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[IdentityOperator](toloka.client.primitives.operators.IdentityOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**bool**|<p>User agreement.</p>
