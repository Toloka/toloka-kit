# close_training
`toloka.client.TolokaClient.close_training` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
close_training(self, training_id: str)
```

Stops distributing tasks from the training

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_id`|**str**|<p>ID of the training that will be closed.</p>

* **Returns:**

  Training object with new status.

* **Return type:**

  [Training](toloka.client.training.Training.md)

**Examples:**

```python
open_training = next(toloka_client.get_trainings(status='OPEN'))
toloka_client.close_training(training_id=open_training.id)
```
