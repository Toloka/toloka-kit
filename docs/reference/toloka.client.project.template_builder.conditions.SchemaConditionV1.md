# SchemaConditionV1
`toloka.client.project.template_builder.conditions.SchemaConditionV1`

```
SchemaConditionV1(
    self,
    data: Optional[Any] = None,
    schema: Optional[Dict] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Allows validating data using JSON Schema. This is a special format for describing data in JSON format.


For example, you can describe the data type, the minimum and maximum values, and specify that all values must be
unique.

This component is useful in the following cases:
    * If available components don't provide everything you need to configure validation.
    * If you already have a prepared JSON Schema configuration for the check and you want to use it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[Any\]**|<p>Data that should be checked.</p>
`schema`|**Optional\[Dict\]**|<p>The schema for validating data.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>
