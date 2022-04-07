# BaseViewV1
`toloka.client.project.template_builder.view.BaseViewV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/view.py#L52)

```python
BaseViewV1(
    self,
    *,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Elements displayed in the interface, such as text, list, audio player, or image.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
