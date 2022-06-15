# ReplaceHelperV1
`toloka.client.project.template_builder.helpers.ReplaceHelperV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/helpers.py#L143)

```python
ReplaceHelperV1(
    self,
    data: Optional[Any] = None,
    find: Optional[Union[BaseComponent, str]] = None,
    replace: Optional[Union[BaseComponent, str]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Allows you to replace some parts of the string with others.


This helper function returns a string in which all occurrences of `find` in `data` are replaced with `replace`.
Because the helper.replace helper returns a string, it can be used in properties that accept string values.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[Any\]**|<p>Data to perform the replacement on.</p>
`find`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>The value to search for — the string whose occurrences must be found in data and replaced with the string from replace.</p>
`replace`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>The value to insert in place of the matches of the find value.</p>
