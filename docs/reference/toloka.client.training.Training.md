# Training
`toloka.client.training.Training`

```python
Training(
    self,
    *,
    project_id: Optional[str] = None,
    private_name: Optional[str] = None,
    may_contain_adult_content: Optional[bool] = None,
    assignment_max_duration_seconds: Optional[int] = None,
    mix_tasks_in_creation_order: Optional[bool] = None,
    shuffle_tasks_in_task_suite: Optional[bool] = None,
    training_tasks_in_task_suite_count: Optional[int] = None,
    task_suites_required_to_pass: Optional[int] = None,
    retry_training_after_days: Optional[int] = None,
    inherited_instructions: Optional[bool] = None,
    public_instructions: Optional[str] = None,
    metadata: Optional[Dict[str, List[str]]] = None,
    owner: Optional[Owner] = None,
    id: Optional[str] = None,
    status: Optional[Status] = None,
    last_close_reason: Optional[CloseReason] = None,
    created: Optional[datetime] = None,
    last_started: Optional[datetime] = None,
    last_stopped: Optional[datetime] = None
)
```

Training pool


Allows:
 - Select for the main pool only those performers who successfully complete the training tasks.
 - Practice performers before the main pool and figure out how to respond correctly.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`project_id`|**Optional\[str\]**|<p>ID of the project to which the training pool belongs.</p>
`private_name`|**Optional\[str\]**|<p>Training pool name (only visible to the requester).</p>
`may_contain_adult_content`|**Optional\[bool\]**|<p>The presence of adult content in learning tasks.</p>
`assignment_max_duration_seconds`|**Optional\[int\]**|<p>Time to complete a set of tasks in seconds. It is recommended to allocate at least 60 seconds for a set of tasks (taking into account the time for loading the page, sending responses).</p>
`mix_tasks_in_creation_order`|**Optional\[bool\]**|<p>The order in which tasks are included in sets:<ul><li>True - Default Behaviour. Include tasks in sets in the order they were loaded.</li><li>False - Include tasks in sets in random order.</li></ul></p>
`shuffle_tasks_in_task_suite`|**Optional\[bool\]**|<p>Order of tasks within the task set:<ul><li>true - Random. Default Behaviour.</li><li>false - The order in which the tasks were loaded.</li></ul></p>
`training_tasks_in_task_suite_count`|**Optional\[int\]**|<p>The number of tasks in the set.</p>
`task_suites_required_to_pass`|**Optional\[int\]**|<p>The number of task suites that must be successfully completed to assign a skill and access the main tasks.</p>
`retry_training_after_days`|**Optional\[int\]**|<p>After how many days the replay will become available.</p>
`inherited_instructions`|**Optional\[bool\]**|<p>Indicates whether to use a project statement. If training need their own instruction, then specify it in public_instructions. Default value - False.</p>
`public_instructions`|**Optional\[str\]**|<p>Instructions for completing training tasks. May contain HTML markup.</p>
`metadata`|**Optional\[Dict\[str, List\[str\]\]\]**|<p></p>
`owner`|**Optional\[[Owner](toloka.client.owner.Owner.md)\]**|<p>Training pool owner.</p>
`id`|**Optional\[str\]**|<p>Internal ID of the training pool. Read only.</p>
`status`|**Optional\[[Status](toloka.client.training.Training.Status.md)\]**|<p>Training pool status. Read only.</p>
`last_close_reason`|**Optional\[[CloseReason](toloka.client.training.Training.CloseReason.md)\]**|<p>The reason the training pool was last closed.</p>
`created`|**Optional\[datetime\]**|<p>UTC date and time of creation of the training pool in ISO 8601 format. Read only.</p>
`last_started`|**Optional\[datetime\]**|<p>UTC date and time of the last start of the training pool in ISO 8601 format. Read only.</p>
`last_stopped`|**Optional\[datetime\]**|<p>UTC date and time of the last stop of the training pool in ISO 8601 format. Read only.</p>
## Methods summary

| Method | Description |
| :------| :-----------|
[is_archived](toloka.client.training.Training.is_archived.md)| None
[is_closed](toloka.client.training.Training.is_closed.md)| None
[is_locked](toloka.client.training.Training.is_locked.md)| None
[is_open](toloka.client.training.Training.is_open.md)| None
[set_owner](toloka.client.training.codegen_setter_for_owner.md)| A shortcut setter for owner
