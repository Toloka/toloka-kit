# OSVersionBugfix
`toloka.client.filter.OSVersionBugfix` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/filter.py#L537)

```python
OSVersionBugfix(
    self,
    operator: CompareOperator,
    value: int
)
```

Use to select users by build number (bugfix version) of the operating system.


For example: 1

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[CompareOperator](toloka.client.primitives.operators.CompareOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**int**|<p>Build number (bugfix version) of the operating system.</p>
