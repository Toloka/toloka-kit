# SearchQueryHelperV1
`toloka.client.project.template_builder.helpers.SearchQueryHelperV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/helpers.py#L160)

```python
SearchQueryHelperV1(
    self,
    query: Optional[Any] = None,
    engine: Optional[Union[BaseComponent, Engine]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Component for creating a string with a search query reference.


The list of available search engines is specified in the engine enum.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`query`|**Optional\[Any\]**|<p>Search query.</p>
`engine`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Engine](toloka.client.project.template_builder.helpers.SearchQueryHelperV1.Engine.md)\]\]**|<p>Search engine.</p>
