# create_pool
`toloka.client.TolokaClient.create_pool` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
create_pool(self, pool: Pool)
```

Creates a new pool


You can send a maximum of 20 requests of this kind per minute and 100 requests per day.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool`|**[Pool](toloka.client.pool.Pool.md)**|<p>New Pool with setted parameters.</p>

* **Returns:**

  Created pool. With read-only fields.

* **Return type:**

  [Pool](toloka.client.pool.Pool.md)

**Examples:**

How to create a new pool in a project.

```python
new_pool = toloka.pool.Pool(
    project_id=existing_project_id,
    private_name='Pool 1',
    may_contain_adult_content=False,
    will_expire=datetime.datetime.utcnow() + datetime.timedelta(days=365),
    reward_per_assignment=0.01,
    assignment_max_duration_seconds=60*20,
    defaults=toloka.pool.Pool.Defaults(default_overlap_for_new_task_suites=3),
    filter=toloka.filter.Languages.in_('EN'),
)
new_pool.set_mixer_config(real_tasks_count=10, golden_tasks_count=0, training_tasks_count=0)
new_pool.quality_control.add_action(...)
new_pool = toloka_client.create_pool(new_pool)
print(new_pool.id)
```
