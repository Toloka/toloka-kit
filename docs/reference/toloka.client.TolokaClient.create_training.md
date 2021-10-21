# create_training
`toloka.client.TolokaClient.create_training`

```
create_training(self, training: Training)
```

Creates a new training

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`training`|**[Training](toloka.client.training.Training.md)**|<p>New Training with setted parameters.</p>

* **Returns:**

  Created training. With read-only fields.

* **Return type:**

  [Training](toloka.client.training.Training.md)

**Examples:**

How to create a new training in a project.

```python
new_training = toloka.training.Training(
    project_id=existing_project_id,
    private_name='Some training in my project',
    may_contain_adult_content=True,
    assignment_max_duration_seconds=10000,
    mix_tasks_in_creation_order=True,
    shuffle_tasks_in_task_suite=True,
    training_tasks_in_task_suite_count=3,
    task_suites_required_to_pass=1,
    retry_training_after_days=7,
    inherited_instructions=True,
    public_instructions='',
)
new_training = toloka_client.create_training(new_training)
print(new_training.id)
```
