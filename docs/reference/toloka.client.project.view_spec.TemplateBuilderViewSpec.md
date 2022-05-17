# TemplateBuilderViewSpec
`toloka.client.project.view_spec.TemplateBuilderViewSpec` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/view_spec.py#L115)

```python
TemplateBuilderViewSpec(
    self,
    *,
    settings: Optional[ViewSpec.Settings] = None,
    view: Optional[BaseComponent] = None,
    plugins: Optional[List[BaseComponent]] = None,
    vars: Optional[Dict[str, Any]] = None,
    core_version: Optional[str] = '1.0.0'
)
```

A template builder view scpecification that defines an interface with


template builder components

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`view`|**-**|<p></p>
`plugins`|**-**|<p></p>
`vars`|**-**|<p></p>
`core_version`|**Optional\[str\]**|<p>Default template components version. Most users will not need to change this parameter.</p>

**Examples:**

How to declare simple interface:

```python
import toloka.client.project.template_builder as tb
project_interface = toloka.project.view_spec.TemplateBuilderViewSpec(
    view=tb.view.ListViewV1(
        items=[header, output_field, radiobuttons],
        validation=some_validation,
    ),
    plugins=[plugin1, plugin2]
)
```
