# create_project
`toloka.client.TolokaClient.create_project` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
create_project(self, project: Project)
```

Creates a new project

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`project`|**[Project](toloka.client.project.Project.md)**|<p>New Project with setted parameters.</p>

* **Returns:**

  Created project. With read-only fields.

* **Return type:**

  [Project](toloka.client.project.Project.md)

**Examples:**

How to create a new project.

```python
new_project = toloka.project.Project(
    assignments_issuing_type=toloka.project.Project.AssignmentsIssuingType.AUTOMATED,
    public_name='My best project',
    public_description='Describe the picture',
    public_instructions='Describe in a few words what is happening in the image.',
    task_spec=toloka.project.task_spec.TaskSpec(
        input_spec={'image': toloka.project.field_spec.UrlSpec()},
        output_spec={'result': toloka.project.field_spec.StringSpec()},
        view_spec=project_interface,
    ),
)
new_project = toloka_client.create_project(new_project)
print(new_project.id)
```
