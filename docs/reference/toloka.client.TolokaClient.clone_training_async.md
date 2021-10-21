# clone_training_async
`toloka.client.TolokaClient.clone_training_async`

```
clone_training_async(self, training_id: str)
```

Duplicates existing training, asynchronous version


An empty training with the same parameters will be created.
A new training will be attached to the same project.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_id`|**str**|<p>ID of the existing training.</p>

* **Returns:**

  An operation upon completion of which you can get the new training.

* **Return type:**

  [TrainingCloneOperation](toloka.client.operations.TrainingCloneOperation.md)

**Examples:**

```python
clone_training = toloka_client.clone_training_async(training_id='1')
toloka_client.wait_operation(clone_training)
```
