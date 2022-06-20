# SpecClassIdentificationError
`toloka.client.exceptions.SpecClassIdentificationError` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/exceptions.py#L25)

```python
SpecClassIdentificationError(
    self,
    *,
    spec_field: Optional[str] = None,
    spec_enum: Optional[str] = None
)
```

Raised when cannot find spec_сlass for spec_field value.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`spec_field`|**Optional\[str\]**|<p>value that defines spec_class type</p>
`spec_enum`|**Optional\[str\]**|<p>enum class containing spec_class possible types</p>
