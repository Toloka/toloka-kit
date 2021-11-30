# get_projects
`toloka.client.TolokaClient.get_projects`

Finds all projects that match certain rules and returns them in an iterable object


Unlike find_projects, returns generator. Does not sort projects.
While iterating over the result, several requests to the Toloka server is possible.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status`|**Optional\[[Project.ProjectStatus](toloka.client.project.Project.ProjectStatus.md)\]**|<p>Status of the project, from Project.ProjectStatus:<ul><li>ACTIVE</li><li>ARCHIVED</li></ul></p>
`id_lt`|**Optional\[str\]**|<p>Projects with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Projects with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Projects with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Projects with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Projects created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Projects created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Projects created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Projects created after or on the specified date.</p>

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[Project](toloka.client.project.Project.md), None, None\]

**Examples:**

Get all active projects.

```python
active_projects = toloka_client.get_projects(status='ACTIVE')
```

Get all your projects.

```python
my_projects = toloka_client.get_projects()
```
