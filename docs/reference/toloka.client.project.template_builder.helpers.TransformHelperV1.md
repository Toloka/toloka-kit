# TransformHelperV1
`toloka.client.project.template_builder.helpers.TransformHelperV1`

```python
TransformHelperV1(
    self,
    into: Optional[Any] = None,
    items: Optional[Union[BaseComponent, List[Any]]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Creates a new array by transforming each of the elements in the original array.


For example, you can convert an array of image links to view.image components to display these images. This may be
useful if the number of images in the array is unknown in advance

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`into`|**Optional\[Any\]**|<p>Template to transform elements in the array. The array value can be substituted using the data.local component. To do this, use the construction { &quot;type&quot;: &quot;data.local&quot;, &quot;path&quot;: &quot;item&quot;}</p>
`items`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Any\]\]\]**|<p>The array that you want to convert. You can specify an array in three ways:<ul><li>Specify the array itself. Example: [&quot;one&quot;, &quot;two&quot;, &quot;three&quot;].</li><li>Insert a reference to data (input, output, or internal). Example: {&quot;type&quot;: &quot;data.input&quot;,     &quot;path&quot;: &quot;path.to.data&quot;}.</li><li>Use a reference to another configuration element. Example: {&quot;$ref&quot;: &quot;vars.myarray&quot;}.</li></ul></p>
