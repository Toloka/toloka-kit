# get_project
`toloka.client.TolokaClient.get_project` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
get_project(self, project_id: str)
```

Reads one specific project

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`project_id`|**str**|<p>ID of the project.</p>

* **Returns:**

  The project.

* **Return type:**

  [Project](toloka.client.project.Project.md)

**Examples:**

```python
toloka_client.get_project(project_id='1')
```
