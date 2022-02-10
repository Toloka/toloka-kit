# Project
`toloka.client.project.Project`

```python
Project(
    self,
    *,
    public_name: Optional[str] = None,
    public_description: Optional[str] = None,
    task_spec: Optional[TaskSpec] = None,
    assignments_issuing_type: Union[AssignmentsIssuingType, str] = AssignmentsIssuingType.AUTOMATED,
    assignments_issuing_view_config: Optional[AssignmentsIssuingViewConfig] = None,
    assignments_automerge_enabled: Optional[bool] = None,
    max_active_assignments_count: Optional[int] = None,
    quality_control: Optional[QualityControl] = None,
    metadata: Optional[Dict[str, List[str]]] = None,
    status: Optional[ProjectStatus] = None,
    created: Optional[datetime] = None,
    id: Optional[str] = None,
    public_instructions: Optional[str] = None,
    private_comment: Optional[str] = None,
    localization_config: Optional[LocalizationConfig] = None
)
```

Top-level object in Toloka. All other entities are contained in some project.


Describes one type of task from the requester's point of view. For example: one project can describe image segmentation,
another project can test this segmentation. The easier the task, the better the results. If your task contains more
than one question, it may be worth dividing it into several projects.

In a project, you set properties for tasks and responses:
* Input data parameters. These parameters describe the objects to display in a task, such as images or text.
* Output data parameters. These parameters describe users' responses. They are used for validating the
    responses entered: the data type (integer, string, etc.), range of values, string length, and so on.
* Task interface. For more information about how to define the appearance of tasks, see the document
    Toloka. requester's guide.

Pools and training pools are related to a project.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`public_name`|**Optional\[str\]**|<p>Name of the project. Visible to users.</p>
`public_description`|**Optional\[str\]**|<p>Description of the project. Visible to users.</p>
`public_instructions`|**Optional\[str\]**|<p>Instructions for completing the task. You can use any HTML markup in the instructions.</p>
`private_comment`|**Optional\[str\]**|<p>Comments about the project. Visible only to the requester.</p>
`task_spec`|**Optional\[[TaskSpec](toloka.client.project.task_spec.TaskSpec.md)\]**|<p>Parameters for input and output data and the task interface.</p>
`assignments_issuing_type`|**[AssignmentsIssuingType](toloka.client.project.Project.AssignmentsIssuingType.md)**|<p>How to assign tasks. The default value is AUTOMATED.</p>
`assignments_automerge_enabled`|**Optional\[bool\]**|<p>Solve merging identical tasks in the project.</p>
`max_active_assignments_count`|**Optional\[int\]**|<p>The number of task suites the user can complete simultaneously (“Active” status)</p>
`quality_control`|**Optional\[[QualityControl](toloka.client.quality_control.QualityControl.md)\]**|<p>The quality control rule.</p>
`metadata`|**Optional\[Dict\[str, List\[str\]\]\]**|<p>Additional information about project.</p>
`status`|**Optional\[[ProjectStatus](toloka.client.project.Project.ProjectStatus.md)\]**|<p>Project status.</p>
`created`|**Optional\[datetime\]**|<p>The UTC date and time the project was created.</p>
`id`|**Optional\[str\]**|<p>Project ID (assigned automatically).</p>
`public_instructions`|**Optional\[str\]**|<p>Instructions for completing tasks. You can use any HTML markup in the instructions.</p>
`private_comment`|**Optional\[str\]**|<p>Comment on the project. Available only to the customer.</p>

**Examples:**

How to create a new project.

```python
toloka_client = toloka.TolokaClient(your_token, 'PRODUCTION')
new_project = toloka.project.Project(
    public_name='My best project!!!',
    public_description='Look at the instruction and do it well',
    public_instructions='!Describe your task for performers here!',
    task_spec=toloka.project.task_spec.TaskSpec(
        input_spec={'image': toloka.project.field_spec.UrlSpec()},
        output_spec={'result': toloka.project.field_spec.StringSpec(allowed_values=['OK', 'BAD'])},
        view_spec=verification_interface_prepared_before,
    ),
)
new_project = toloka_client.create_project(new_project)
print(new_project.id)
```
## Methods summary

| Method | Description |
| :------| :-----------|
[add_requester_translation](toloka.client.project.Project.add_requester_translation.md)| Add new translations to other language.
[set_default_language](toloka.client.project.Project.set_default_language.md)| Sets the source language used in the fields public_name, public_description, and public_instructions.
