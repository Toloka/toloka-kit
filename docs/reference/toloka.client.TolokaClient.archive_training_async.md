# archive_training_async
`toloka.client.TolokaClient.archive_training_async` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/__init__.py#L44)

```python
archive_training_async(self, training_id: str)
```

Sends training to archive, asynchronous version


The training must be in the status "closed".
The archived training is not deleted. You can access it when you will need it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_id`|**str**|<p>ID of training that will be archived.</p>

* **Returns:**

  An operation upon completion of which you can get the training with updated
status. If pool is already archived then None is returned.

* **Return type:**

  Optional\[[TrainingArchiveOperation](toloka.client.operations.TrainingArchiveOperation.md)\]

**Examples:**

```python
closed_training = next(toloka_client.find_trainings(status='CLOSED'))
archive_op = toloka_client.archive_training_async(training_id=closed_training.id)
toloka_client.wait_operation(archive_op)
```
