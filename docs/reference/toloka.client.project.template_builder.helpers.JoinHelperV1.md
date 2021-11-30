# JoinHelperV1
`toloka.client.project.template_builder.helpers.JoinHelperV1`

```
JoinHelperV1(
    self,
    items: Optional[Union[BaseComponent, List[Union[BaseComponent, str]]]] = None,
    by: Optional[Any] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

The component combines two or more strings into one.


You can add a delimiter to separate the strings, such as a space or comma.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]\]\]**|<p>Array of strings to join.</p>
`by`|**Optional\[Any\]**|<p>Delimiter for joining strings. You can use any number of characters in the delimiter.</p>
