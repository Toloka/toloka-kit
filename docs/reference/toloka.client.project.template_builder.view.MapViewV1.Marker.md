# Marker
`toloka.client.project.template_builder.view.MapViewV1.Marker` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/view.py#L446)

```python
Marker(
    self,
    position: Optional[Union[BaseComponent, str]] = None,
    *,
    color: Optional[Union[BaseComponent, str]] = None,
    label: Optional[Union[BaseComponent, str]] = None
)
```

Marker parameters.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`position`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Determines the marker position. Specify the coordinates in the string format, for example, &quot;29.748713,-95.404287&quot;, or use the data.location component to set the marker to the Toloker&#x27;s current position.</p>
`color`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Determines the marker color. Use the hexadecimal values preceded by the # sign to specify the color.</p>
`label`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>The label for the marker that tells Tolokers what this marker is for and helps distinguish it from other markers.</p>
