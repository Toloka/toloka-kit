# create_tasks
`toloka.client.TolokaClient.create_tasks`

Creates several tasks in Toloka using a single request.


Tasks can be added to different pools. You can add together regular tasks and control tasks.
You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.

By default, `create_tasks` starts asynchronous operation internally and waits for the completion of it. Do not
change `async_mode` to False, if you do not understand clearly why you need it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`tasks`|**List\[[Task](toloka.client.task.Task.md)\]**|<p>List of tasks to be created.</p>
`allow_defaults`|**Optional\[bool\]**|<p>Overlap setting:<ul><li>True — Use the overlap value that is set in the `defaults.default_overlap_for_new_task_suites` pool parameter.</li><li>False — Use the overlap value that is set in the `overlap` task suite parameter.</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Task validation option:<ul><li>True — All valid tasks are added. If a task does not pass validation, then it is not added to Toloka. All such tasks are listed in the response.</li><li>False — If any task does not pass validation, then operation is cancelled and no tasks are added to Toloka.</li></ul></p>
`async_mode`|**Optional\[bool\]**|<p>Request processing mode:<ul><li>True — Asynchronous operation is started internally and `create_tasks` waits for the completion of it. It is recommended to create no more than 10,000 tasks per request in this mode.</li><li>False — The request is processed synchronously. A maximum of 5000 tasks can be added in a single request in this mode.</li></ul></p>

* **Returns:**

  An object with created tasks in `items` and invalid tasks in
`validation_errors`.

* **Return type:**

  [TaskBatchCreateResult](toloka.client.batch_create_results.TaskBatchCreateResult.md)

**Examples:**

The first example shows how to create regular tasks using a TSV file.

```python
dataset = pandas.read_csv('dataset.tsv', sep='  ')
tasks = [
    toloka.task.Task(input_values={'image': url}, pool_id=existing_pool_id)
    for url in dataset['image'].values[:50]
]
created_result = toloka_client.create_tasks(tasks, allow_defaults=True)
print(len(created_result.items))
```

The second example shows how to create control tasks.

```python
dataset = pd.read_csv('dateset.tsv', sep=';')
golden_tasks = []
for _, row in dataset.iterrows():
    golden_tasks.append(
            toloka.task.Task(
                input_values={'image': row['image']},
                known_solutions = [toloka.task.BaseTask.KnownSolution(output_values={'animal': row['label']})],
                pool_id = existing_pool_id,
            )
        )
created_result = toloka_client.create_tasks(golden_tasks, allow_defaults=True)
print(len(created_result.items))
```
