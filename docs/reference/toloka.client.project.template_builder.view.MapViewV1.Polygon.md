# Polygon
`toloka.client.project.template_builder.view.MapViewV1.Polygon` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/view.py#L461)

```python
Polygon(
    self,
    points: Optional[Union[BaseComponent, List[Union[BaseComponent, str]]]] = None,
    *,
    color: Optional[Union[BaseComponent, str]] = None
)
```

Polygon parameters.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`points`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]\]\]**|<p>The list of the polygonal selection area points. Specify the coordinates in the string format, for example, &quot;29.748713,-95.404287&quot;.</p>
`color`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Determines the polygonal selection area color. Use the hexadecimal values preceded by the # sign to specify the color.</p>
