# open_training_async
`toloka.client.TolokaClient.open_training_async`

```
open_training_async(self, training_id: str)
```

Starts distributing tasks from the training, asynchronous version

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_id`|**str**|<p>ID of the training that will be started.</p>

* **Returns:**

  An operation upon completion of which you can get the training with new status. If
training is already opened then None is returned.

* **Return type:**

  Optional\[[TrainingOpenOperation](toloka.client.operations.TrainingOpenOperation.md)\]

**Examples:**

Open the training for performers.

```python
open_training = toloka_client.open_training_async(training_id='1')
toloka_client.wait_operation(open_training)
```
