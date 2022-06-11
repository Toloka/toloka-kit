# TaskSpec
`toloka.client.project.task_spec.TaskSpec` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/task_spec.py#L8)

```python
TaskSpec(
    self,
    *,
    input_spec: Optional[Dict[str, FieldSpec]] = None,
    output_spec: Optional[Dict[str, FieldSpec]] = None,
    view_spec: Optional[ViewSpec] = None
)
```

Parameters for input and output data and the task interface.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`input_spec`|**Optional\[Dict\[str, [FieldSpec](toloka.client.project.field_spec.FieldSpec.md)\]\]**|<p>The input data parameters for tasks. The complete list of parameters is shown in the Input and output data table.</p>
`output_spec`|**Optional\[Dict\[str, [FieldSpec](toloka.client.project.field_spec.FieldSpec.md)\]\]**|<p>Parameters for output data from the input fields. The complete list of parameters is shown in the Input and output data table.</p>
`view_spec`|**Optional\[[ViewSpec](toloka.client.project.view_spec.ViewSpec.md)\]**|<p>Description of the task interface.</p>
