# get_project
`toloka.client.TolokaClient.get_project`

```
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
