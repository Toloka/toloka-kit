# GroupViewV1
`toloka.client.project.template_builder.view.GroupViewV1`

```
GroupViewV1(
    self,
    content: Optional[BaseComponent] = None,
    *,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Groups components visually into framed blocks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Content of a group block.</p>
`hint`|**Optional\[Any\]**|<p>Explanation of the group heading. To insert a new line, use .</p>
`label`|**Optional\[Any\]**|<p>Group heading.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
