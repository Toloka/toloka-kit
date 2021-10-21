# DateOfBirth
`toloka.client.filter.DateOfBirth`

```
DateOfBirth(
    self,
    operator: CompareOperator,
    value: int
)
```

Use to select users by date of birth.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[CompareOperator](toloka.client.primitives.operators.CompareOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**int**|<p>The user&#x27;s date of birth (UNIX time in seconds).</p>
