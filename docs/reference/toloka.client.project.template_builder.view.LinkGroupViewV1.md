# LinkGroupViewV1
`toloka.client.project.template_builder.view.LinkGroupViewV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/view.py#L299)

```python
LinkGroupViewV1(
    self,
    links: Optional[Union[BaseComponent, List[Union[BaseComponent, Link]]]] = None,
    *,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Puts links into groups


The most important link in a group can be highlighted with a border: set the theme property to primary for this link.
This only groups links, unlike GroupViewV1.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`links`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Link](toloka.client.project.template_builder.view.LinkGroupViewV1.Link.md)\]\]\]\]**|<p>Array of links that make up a group.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>

**Examples:**

How to add several links.

```python
links = tb.view.LinkGroupViewV1(
    [
        tb.view.LinkGroupViewV1.Link(
            'https://any.com/useful/url/1',
            'Example1',
        ),
        tb.view.LinkGroupViewV1.Link(
            'https://any.com/useful/url/2',
            'Example2',
        ),
    ]
)
```
