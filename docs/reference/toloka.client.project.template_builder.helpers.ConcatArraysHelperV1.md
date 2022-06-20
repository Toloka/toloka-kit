# ConcatArraysHelperV1
`toloka.client.project.template_builder.helpers.ConcatArraysHelperV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/helpers.py#L31)

```python
ConcatArraysHelperV1(
    self,
    items: Optional[Union[BaseComponent, List[Any]]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Merging multiple arrays into a single array.


For example, let's say you have multiple arrays:
([1, 2, 3], [4, 5, 6], [7, 8, 9])
Their elements can be combined into a single array to show simultaneously:
[1, 2, 3, 4, 5, 6, 7, 8, 9]

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Any\]\]\]**|<p>Arrays to combine.</p>
