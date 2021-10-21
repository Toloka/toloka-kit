# TextTransformHelperV1
`toloka.client.project.template_builder.helpers.TextTransformHelperV1`

```
TextTransformHelperV1(
    self,
    data: Optional[Any] = None,
    transformation: Optional[Union[BaseComponent, Transformation]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Allows you to change the case of the text, like make all letters uppercase.


For example, you can use this component to automatically process input data.

This component is available in property values with the string type, for example in the content property in the
view.text component.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[Any\]**|<p>The text string in which you want to change the case.</p>
`transformation`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Transformation](toloka.client.project.template_builder.helpers.TextTransformHelperV1.Transformation.md)\]\]**|<p>Conversion mode.</p>
