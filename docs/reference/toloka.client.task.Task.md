# Task
`toloka.client.task.Task` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/task.py#L65)

```python
Task(
    self,
    *,
    input_values: Optional[Dict[str, Any]] = None,
    known_solutions: Optional[List[BaseTask.KnownSolution]] = None,
    message_on_unknown_solution: Optional[str] = None,
    id: Optional[str] = None,
    infinite_overlap=None,
    overlap=None,
    pool_id: Optional[str] = None,
    remaining_overlap: Optional[int] = None,
    reserved_for: Optional[List[str]] = None,
    unavailable_for: Optional[List[str]] = None,
    traits_all_of: Optional[List[str]] = None,
    traits_any_of: Optional[List[str]] = None,
    traits_none_of_any: Optional[List[str]] = None,
    origin_task_id: Optional[str] = None,
    created: Optional[datetime] = None,
    baseline_solutions: Optional[List[BaselineSolution]] = None
)
```

The task that will be issued to the performers


Not to be confused with TaskSuite - a set of tasks that is shown to the user at one time.
TaskSuite may contain several Tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`input_values`|**Optional\[Dict\[str, Any\]\]**|<p>Input data for a task. List of pairs: &quot;&lt;input field ID 1&gt;&quot;: &quot;&lt;field value 1&gt;&quot;, &quot;&lt;input field ID 1&gt;&quot;: &quot;&lt;field value 2&gt;&quot;, ... &quot;&lt;input field ID n&gt;&quot;: &quot;&lt;field value n&gt;&quot;</p>
`known_solutions`|**Optional\[List\[[BaseTask.KnownSolution](toloka.client.task.BaseTask.KnownSolution.md)\]\]**|<p>Responses and hints for control tasks and training tasks. If multiple output fields are included in the validation, all combinations of the correct response must be specified.</p>
`message_on_unknown_solution`|**Optional\[str\]**|<p>Hint for the task (for training tasks).</p>
`id`|**Optional\[str\]**|<p>Task ID.</p>
`pool_id`|**Optional\[str\]**|<p>The ID of the pool that the task is uploaded to.</p>
`remaining_overlap`|**Optional\[int\]**|<p>How many times will this task be issued to performers. Read Only field.</p>
`reserved_for`|**Optional\[List\[str\]\]**|<p>IDs of users who will have access to the task.</p>
`unavailable_for`|**Optional\[List\[str\]\]**|<p>IDs of users who shouldn&#x27;t have access to the task.</p>
`traits_all_of`|**Optional\[List\[str\]\]**|<p></p>
`traits_any_of`|**Optional\[List\[str\]\]**|<p></p>
`traits_none_of_any`|**Optional\[List\[str\]\]**|<p></p>
`origin_task_id`|**Optional\[str\]**|<p>ID of the task it was copied from.</p>
`created`|**Optional\[datetime\]**|<p>The UTC date and time when the task was created.</p>
`baseline_solutions`|**Optional\[List\[[BaselineSolution](toloka.client.task.Task.BaselineSolution.md)\]\]**|<p>Preliminary responses. This data simulates performer responses when calculating confidence in a response. It is used in dynamic overlap (also known as incremental relabeling or IRL) and aggregation of results by skill.</p>

**Examples:**

How to create tasks.

```python
tasks = [
    Task(input_values={'image': 'https://some.url/my_img0001.png'}, pool_id=my_pool_id),
    Task(input_values={'image': 'https://some.url/my_img0002.png'}, pool_id=my_pool_id),
]
created_tasks = toloka_client.create_tasks(tasks, allow_defaults=True)
print(len(created_tasks.items))
```
