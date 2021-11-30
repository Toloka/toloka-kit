# Rating
`toloka.client.filter.Rating`

```
Rating(
    self,
    operator: CompareOperator,
    value: Optional[float] = None
)
```

Use to select users by user rating.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[CompareOperator](toloka.client.primitives.operators.CompareOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**Optional\[float\]**|<p>User rating. Calculated based on earnings in all projects available to the user.</p>
