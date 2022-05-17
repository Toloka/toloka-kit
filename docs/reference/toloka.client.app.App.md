# App
`toloka.client.app.App` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/app/__init__.py#L71)

```python
App(
    self,
    *,
    id: Optional[str] = None,
    name: Optional[str] = None,
    image: Optional[str] = None,
    description: Optional[str] = None,
    constraints_description: Optional[str] = None,
    default_item_price: Optional[Decimal] = None,
    param_spec: Optional[Dict] = None,
    input_spec: Optional[Dict[str, FieldSpec]] = None,
    output_spec: Optional[Dict[str, FieldSpec]] = None,
    examples: Optional[Any] = None
)
```

An example of a standard task that you want to solve using Toloka. Unlike project templates, you don't have to


set up everything yourself.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>ID of the App.</p>
`name`|**Optional\[str\]**|<p></p>
`image`|**Optional\[str\]**|<p>Image.</p>
`description`|**Optional\[str\]**|<p>Overview.</p>
`constraints_description`|**Optional\[str\]**|<p>Description of limitations.</p>
`default_item_price`|**Optional\[Decimal\]**|<p>Default processing cost per work item.</p>
`param_spec`|**Optional\[Dict\]**|<p>Specification of parameters for creating a project.</p>
`input_spec`|**Optional\[Dict\[str, [FieldSpec](toloka.client.project.field_spec.FieldSpec.md)\]\]**|<p>Schema of input data in Toloka format.</p>
`output_spec`|**Optional\[Dict\[str, [FieldSpec](toloka.client.project.field_spec.FieldSpec.md)\]\]**|<p>Schema of output data in Toloka format.</p>
`examples`|**Optional\[Any\]**|<p>Task examples.</p>
