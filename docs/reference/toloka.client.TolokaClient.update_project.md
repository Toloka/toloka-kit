# update_project
`toloka.client.TolokaClient.update_project` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
update_project(
    self,
    project_id: str,
    project: Project
)
```

Makes changes to the project

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`project_id`|**str**|<p>Project ID that will be changed.</p>
`project`|**[Project](toloka.client.project.Project.md)**|<p>A project object with all the fields: those that will be updated and those that will not.</p>

* **Returns:**

  Project object with all fields.

* **Return type:**

  [Project](toloka.client.project.Project.md)

**Examples:**

```python
updated_project = toloka_client.update_project(project_id=old_project.id, project=new_project_object)
```
