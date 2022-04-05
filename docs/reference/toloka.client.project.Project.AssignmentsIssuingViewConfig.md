# AssignmentsIssuingViewConfig
`toloka.client.project.Project.AssignmentsIssuingViewConfig` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/__init__.py#L141)

```python
AssignmentsIssuingViewConfig(
    self,
    *,
    title_template: Optional[str] = None,
    description_template: Optional[str] = None,
    map_provider: Optional[MapProvider] = None
)
```

How the task will be displayed on the map


Used only then assignments_issuing_type == MAP_SELECTOR

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`title_template`|**Optional\[str\]**|<p>Name of the task. Users will see it in the task preview mode.</p>
`description_template`|**Optional\[str\]**|<p>Brief description of the task. Users will see it in the task preview mode.</p>
