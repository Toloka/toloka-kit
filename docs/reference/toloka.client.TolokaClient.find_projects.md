# find_projects
`toloka.client.TolokaClient.find_projects`

Finds all projects that match certain rules


As a result, it returns an object that contains the first part of the found projects and whether there
are any more results.
It is better to use the "get_projects" method, they allow to iterate trought all results
and not just the first output.

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
`sort`|**Union\[List\[str\], [ProjectSortItems](toloka.client.search_requests.ProjectSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned. The maximum is 300. Defaults to None, in which case it returns first 20 results.</p>

* **Returns:**

  The first `limit` projects in `items`.
And a mark that there is more.

* **Return type:**

  [ProjectSearchResult](toloka.client.search_results.ProjectSearchResult.md)

**Examples:**

Find projects that were created before a specific date.

```python
toloka_client.find_projects(created_lt='2021-06-01T00:00:00')
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
