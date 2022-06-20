# Entries2ObjectHelperV1
`toloka.client.project.template_builder.helpers.Entries2ObjectHelperV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/helpers.py#L45)

```python
Entries2ObjectHelperV1(
    self,
    entries: Optional[Union[BaseComponent, List[Union[BaseComponent, Entry]]]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Creating an object from a specified array of key-value pairs.


For example, let's say you have an array like this:
[
    {
        "key": "foo",
        "value": "hello"
    },
    {
        "key": "bar",
        "value": "world"
    }
]
It is converted to an object whose elements consist of the values of the original array:
{ "foo": "hello", "bar": "world" }

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`entries`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Entry](toloka.client.project.template_builder.helpers.Entries2ObjectHelperV1.Entry.md)\]\]\]\]**|<p>Source array of key-value pairs.</p>
