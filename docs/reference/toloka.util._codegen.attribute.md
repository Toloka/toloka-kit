# attribute
`toloka.util._codegen.attribute` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/util/_codegen.py#L242)

```python
attribute(
    *args,
    required: bool = False,
    origin: Optional[str] = None,
    readonly: bool = False,
    autocast: bool = False,
    **kwargs
)
```

Proxy for attr.attrib(...). Adds several keywords.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`*args`|**-**|<p>All positional arguments from attr.attrib</p>
`required`|**bool**|<p>If True makes attribute not Optional. All other attributes are optional by default. Defaults to False.</p>
`origin`|**Optional\[str\]**|<p>Sets field name in dict for attribute, when structuring/unstructuring from dict. Defaults to None.</p>
`readonly`|**bool**|<p>Affects only when the class &#x27;expanding&#x27; as a parameter in some function. If True, drops this attribute from expanded parameters. Defaults to None.</p>
`autocast`|**bool**|<p>If True then converter.structure will be used to convert input value</p>
`**kwargs`|**-**|<p>All keyword arguments from attr.attrib</p>
