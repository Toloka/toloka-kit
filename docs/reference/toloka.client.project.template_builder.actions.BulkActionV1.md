# BulkActionV1
`toloka.client.project.template_builder.actions.BulkActionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/actions.py#L34)

```python
BulkActionV1(
    self,
    payload: Optional[Union[BaseComponent, List[BaseComponent]]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Use this component to call multiple actions at the same time, like to show more than one notification when a button is clicked.


Actions are invoked in the order in which they are listed. This means that if two actions write a value to the same
variable, the variable will always have the second value.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`payload`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]\]\]**|<p>An array of actions that you want to call.</p>
