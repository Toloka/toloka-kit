# clone_training
`toloka.client.TolokaClient.clone_training` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/__init__.py#L44)

```python
clone_training(self, training_id: str)
```

Duplicates existing training


An empty training with the same parameters will be created.
A new training will be attached to the same project.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training_id`|**str**|<p>ID of the existing training.</p>

* **Returns:**

  New training.

* **Return type:**

  [Training](toloka.client.training.Training.md)

**Examples:**

```python
toloka_client.clone_training(training_id='1')
```
