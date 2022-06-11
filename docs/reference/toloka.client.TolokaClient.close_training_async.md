# close_training_async
`toloka.client.TolokaClient.close_training_async` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/__init__.py#L40)

```python
close_training_async(self, training_id: str)
```

Stops distributing tasks from the training, asynchronous version

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_id`|**str**|<p>ID of the training that will be closed.</p>

* **Returns:**

  An operation upon completion of which you can get the training with updated status.
If training is already closed then None is returned.

* **Return type:**

  Optional\[[TrainingCloseOperation](toloka.client.operations.TrainingCloseOperation.md)\]

**Examples:**

```python
open_training = next(toloka_client.get_trainings(status='OPEN'))
close_training = toloka_client.close_training_async(training_id=open_training.id)
toloka_client.wait_operation(close_training)
```
