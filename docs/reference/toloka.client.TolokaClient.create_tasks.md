# create_tasks
`toloka.client.TolokaClient.create_tasks`

Creates many tasks in pools


By default uses asynchronous operation inside. It's better not to set "async_mode=False", if you not understand
clearly why you need it.
Tasks can be from different pools. You can insert both regular tasks and golden-tasks.
You can send a maximum of 100,000 requests of this kind per minute and a maximum of 2,000,000 requests per day.
Recomended maximum of 10,000 task per request if async_mode is True.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`tasks`|**List\[[Task](toloka.client.task.Task.md)\]**|<p>List of tasks, that will be created.</p>
`allow_defaults`|**Optional\[bool\]**|<p>Overlap settings:<ul><li>True - Use the overlap that is set in the pool parameters (in the defaults.default_overlap_for_new_task_suites key).</li><li>False - Use the overlap that is set in the task suite parameters (in the overlap field).</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters:<ul><li>True — Create the tasks that passed validation. Skip the rest of the tasks (errors will     be listed in the response to the request).</li><li>False — If at least one of the tasks didn&#x27;t pass validation, stop the operation and don&#x27;t create any tasks.</li></ul></p>
`async_mode`|**Optional\[bool\]**|<p>How the request is processed:<ul><li>True — deferred. The query results in an asynchronous operation running in the background.     The response contains information about the operation (start and end time, status, number of sets).</li><li>False — synchronous. The response contains information about the created tasks.     A maximum of 5000 tasks can be sent in a single request.</li></ul></p>

* **Returns:**

  Result of tasks creating. Contains created tasks in `items` and
problems in "validation_errors".

* **Return type:**

  [TaskBatchCreateResult](toloka.client.batch_create_results.TaskBatchCreateResult.md)

**Examples:**

How to create regular tasks from tsv.

```python
dataset = pandas.read_csv('dataset.tsv', sep='  ')
tasks = [
    toloka.task.Task(input_values={'image': url}, pool_id=existing_pool_id)
    for url in dataset['image'].values[:50]
]
created_result = toloka_client.create_tasks(tasks, allow_defaults=True)
print(len(created_result.items))
```

How to create golden-tasks.

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
