# MapViewV1
`toloka.client.project.template_builder.view.MapViewV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/view.py#L429)

```python
MapViewV1(
    self,
    center: Optional[Union[BaseComponent, str]] = None,
    *,
    markers: Optional[Union[BaseComponent, List[Union[BaseComponent, Marker]]]] = None,
    polygons: Optional[Union[BaseComponent, List[Union[BaseComponent, Polygon]]]] = None,
    zoom: Optional[Union[BaseComponent, int]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Adds a map to your task.


Use this component to set the targets for the tasks with the markers, select the areas with polygons.
Specify the position and colors for the elements on the map.

You can set the following map properties: scale, position of the map center, label, and hint for the users.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`center`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Determines the position of the map center. Specify the coordinates in the string format, for example, &quot;29.748713,-95.404287&quot;, or use the data.location component to set the center of the map to the Toloker&#x27;s current position.</p>
`markers`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Marker](toloka.client.project.template_builder.view.MapViewV1.Marker.md)\]\]\]\]**|<p>Specifies the markers present on the map.</p>
`polygons`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Polygon](toloka.client.project.template_builder.view.MapViewV1.Polygon.md)\]\]\]\]**|<p>Specifies the polygonal objects that you can use to select areas on the map.</p>
`zoom`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), int\]\]**|<p>The map initial scale. Use the values from 0 to 19. Bigger values give a more detailed map view.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
