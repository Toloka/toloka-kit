# Computed
`toloka.client.filter.Computed` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/filter.py#L179)

```python
Computed(
    self,
    *,
    operator: Any,
    value: Any
)
```

Use to select users based on data received or calculated by Toloka.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**Any**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**Any**|<p>Attribute value from the field key. For example, the ID of the region specified in the profile, or the minimum skill value.</p>
