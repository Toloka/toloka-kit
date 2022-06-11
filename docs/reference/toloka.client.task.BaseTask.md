# BaseTask
`toloka.client.task.BaseTask` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/task.py#L20)

```python
BaseTask(
    self,
    *,
    input_values: Optional[Dict[str, Any]] = None,
    known_solutions: Optional[List[KnownSolution]] = None,
    message_on_unknown_solution: Optional[str] = None,
    id: Optional[str] = None,
    origin_task_id: Optional[str] = None
)
```

Base class for Task

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`input_values`|**Optional\[Dict\[str, Any\]\]**|<p>Input data for a task. List of pairs: &quot;&lt;input field ID 1&gt;&quot;: &quot;&lt;field value 1&gt;&quot;, &quot;&lt;input field ID 1&gt;&quot;: &quot;&lt;field value 2&gt;&quot;, ... &quot;&lt;input field ID n&gt;&quot;: &quot;&lt;field value n&gt;&quot;</p>
`known_solutions`|**Optional\[List\[[KnownSolution](toloka.client.task.BaseTask.KnownSolution.md)\]\]**|<p>Responses and hints for control tasks and training tasks. If multiple output fields are included in the validation, all combinations of the correct response must be specified.</p>
`message_on_unknown_solution`|**Optional\[str\]**|<p>Hint for the task (for training tasks).</p>
`id`|**Optional\[str\]**|<p>Task ID.</p>
`origin_task_id`|**Optional\[str\]**|<p>ID of the task it was copied from.</p>
