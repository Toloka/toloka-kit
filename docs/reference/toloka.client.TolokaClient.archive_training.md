# archive_training
`toloka.client.TolokaClient.archive_training` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/__init__.py#L44)

```python
archive_training(self, training_id: str)
```

Sends training to archive


The training must be in the status "closed".
The archived training is not deleted. You can access it when you will need it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_id`|**str**|<p>ID of training that will be archived.</p>

* **Returns:**

  Object with updated status.

* **Return type:**

  [Training](toloka.client.training.Training.md)

**Examples:**

```python
closed_training = next(toloka_client.get_trainings(status='CLOSED'))
toloka_client.archive_training(training_id=closed_training.id)
```
