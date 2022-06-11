# Link
`toloka.client.project.template_builder.view.LinkGroupViewV1.Link` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/view.py#L327)

```python
Link(
    self,
    url: Optional[Union[BaseComponent, str]] = None,
    content: Optional[Union[BaseComponent, str]] = None,
    *,
    theme: Optional[Union[BaseComponent, str]] = None
)
```

Link parameters

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`url`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Link address</p>
`content`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Link text that&#x27;s displayed to the user. Unviewed links are blue and underlined, and clicked links are purple.</p>
`theme`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Defines the appearance of the link. If you specify &quot;theme&quot;: &quot;primary&quot;, it&#x27;s a button, otherwise it&#x27;s a text link.</p>
