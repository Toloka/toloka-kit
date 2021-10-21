# archive_project_async
`toloka.client.TolokaClient.archive_project_async`

```
archive_project_async(self, project_id: str)
```

Sends project to archive, asynchronous version


Use when you have no need this project anymore. To perform the operation, all pools in the project must be archived.
The archived project is not deleted. You can access it when you will need it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`project_id`|**str**|<p>ID of project that will be archived.</p>

* **Returns:**

  An operation upon completion of which you can get the project with updated status.

* **Return type:**

  [ProjectArchiveOperation](toloka.client.operations.ProjectArchiveOperation.md)

**Examples:**

```python
archive_op = toloka_client.archive_project_async(project_id='1')
toloka_client.wait_operation(archive_op)
```
