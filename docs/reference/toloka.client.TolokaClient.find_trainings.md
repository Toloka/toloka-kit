# find_trainings
`toloka.client.TolokaClient.find_trainings`

Finds all trainings that match certain rules


As a result, it returns an object that contains the first part of the found trainings and whether there
are any more results.
It is better to use the "get_trainings" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status`|**Optional\[[Training.Status](toloka.client.training.Training.Status.md)\]**|<p>Training pool status:<ul><li>OPEN</li><li>CLOSED</li><li>ARCHIVED</li><li>LOCKED</li></ul></p>
`project_id`|**Optional\[str\]**|<p>ID of the project to which the training pool is attached.</p>
`id_lt`|**Optional\[str\]**|<p>Training pools with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Training pools with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Training pools with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Training pools with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Training pools created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Training pools created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Training pools created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Training pools created after or on the specified date.</p>
`last_started_lt`|**Optional\[datetime\]**|<p>Training pools that were last opened before the specified date.</p>
`last_started_lte`|**Optional\[datetime\]**|<p>Training pools that were last opened on or before the specified date.</p>
`last_started_gt`|**Optional\[datetime\]**|<p>Training pools that were last opened after the specified date.</p>
`last_started_gte`|**Optional\[datetime\]**|<p>Training pools that were last opened on or after the specified date.</p>
`sort`|**Union\[List\[str\], [TrainingSortItems](toloka.client.search_requests.TrainingSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned.</p>

* **Returns:**

  The first `limit` trainings in `items`.
And a mark that there is more.

* **Return type:**

  [TrainingSearchResult](toloka.client.search_results.TrainingSearchResult.md)

**Examples:**

Find all trainings in all projects.

```python
toloka_client.find_trainings()
```

Find all open trainings in all projects.

```python
toloka_client.find_trainings(status='OPEN')
```

Find all open trainings in a specific project.

```python
toloka_client.find_trainings(status='OPEN', project_id='1')
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
