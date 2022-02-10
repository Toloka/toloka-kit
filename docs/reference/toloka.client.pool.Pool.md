# Pool
`toloka.client.pool.Pool`

```python
Pool(
    self,
    *,
    project_id: Optional[str] = None,
    private_name: Optional[str] = None,
    may_contain_adult_content: Optional[bool] = None,
    reward_per_assignment: Optional[float] = None,
    assignment_max_duration_seconds: Optional[int] = None,
    defaults: Optional[Defaults] = ...,
    will_expire: Optional[datetime] = None,
    private_comment: Optional[str] = None,
    public_description: Optional[str] = None,
    public_instructions: Optional[str] = None,
    auto_close_after_complete_delay_seconds: Optional[int] = None,
    dynamic_pricing_config: Optional[DynamicPricingConfig] = None,
    auto_accept_solutions: Optional[bool] = None,
    auto_accept_period_day: Optional[int] = None,
    assignments_issuing_config: Optional[AssignmentsIssuingConfig] = None,
    priority: Optional[int] = None,
    filter: Optional[FilterCondition] = None,
    quality_control: Optional[QualityControl] = ...,
    dynamic_overlap_config: Optional[DynamicOverlapConfig] = None,
    mixer_config: Optional[MixerConfig] = None,
    training_config: Optional[TrainingConfig] = None,
    metadata: Optional[Dict[str, List[str]]] = None,
    owner: Optional[Owner] = None,
    id: Optional[str] = None,
    status: Optional[Status] = None,
    last_close_reason: Optional[CloseReason] = None,
    created: Optional[datetime] = None,
    last_started: Optional[datetime] = None,
    last_stopped: Optional[datetime] = None,
    type: Optional[Type] = None
)
```

A set of tasks that are issued and checked according to the same rules within the project


Groups tasks by the following criteria: one-time start-up, which performers can perform tasks, quality control,
price for TaskSuite's, overlap.
Tasks, golden tasks and assignments are related to a pool.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`project_id`|**Optional\[str\]**|<p>ID of the project that the pool was created for.</p>
`private_name`|**Optional\[str\]**|<p>Name of the pool (only visible to the requester).</p>
`may_contain_adult_content`|**Optional\[bool\]**|<p>Whether the tasks contain adult content.</p>
`reward_per_assignment`|**Optional\[float\]**|<p>Payment per task suite in U.S. dollars. For cents, use the dot (&quot;.&quot;) as the separator. The minimum payment is $0.01. Only training and control tasks can be uploaded to zero-price pools.</p>
`assignment_max_duration_seconds`|**Optional\[int\]**|<p>The time allowed for completing a task suite, in seconds. Tasks not completed within this time are reassigned to other users. We recommend allowing no more than 60 seconds per task suite (including the time for page loading and sending responses).</p>
`defaults`|**Optional\[[Defaults](toloka.client.pool.Pool.Defaults.md)\]**|<p>Settings that are applied by default when uploading new task suites to a pool.</p>
`will_expire`|**Optional\[datetime\]**|<p>The date and time in UTC when the pool should be closed (even if all the task suites haven&#x27;t been completed).</p>
`private_comment`|**Optional\[str\]**|<p>Comments on the pool (only visible to the requester).</p>
`public_description`|**Optional\[str\]**|<p>Description for users. If it is filled in, the text will be displayed instead of the project&#x27;s public_description in the list of tasks for performers.</p>
`public_instructions`|**Optional\[str\]**|<p>Optional[str]</p>
`auto_close_after_complete_delay_seconds`|**Optional\[int\]**|<p>Waiting time (in seconds) before automatic closure of the pool after all tasks are completed. Minimum — 0, maximum — 259200 seconds (three days). Use it if:     * Your data processing is close to real time.     * You need an open pool where you upload tasks.     * Dynamic overlap is enabled in the pool (dynamic_overlap_config).</p>
`dynamic_pricing_config`|**Optional\[[DynamicPricingConfig](toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig.md)\]**|<p>The dynamic pricing settings.</p>
`auto_accept_solutions`|**Optional\[bool\]**|<p>Whether tasks must be checked manually:<ul><li>True - Automatic task acceptance (manual checking isn&#x27;t necessary).</li><li>False - The requester will check the tasks.</li></ul></p>
`auto_accept_period_day`|**Optional\[int\]**|<p>Optional[int]</p>
`assignments_issuing_config`|**Optional\[[AssignmentsIssuingConfig](toloka.client.pool.Pool.AssignmentsIssuingConfig.md)\]**|<p>Settings for assigning tasks in the pool.</p>
`priority`|**Optional\[int\]**|<p>The priority of the pool in relation to other pools in the project with the same task price and set of filters. Users are assigned tasks with a higher priority first. Possible values: from -100 to 100. If the project has multiple pools, the order for completing them depends on the parameters:<ul><li>Pools with identical filter settings and price per task are assigned to users in the order     in which they were started. The pool that was started earlier will be completed sooner.     You can change the order for completing the pools.</li><li>Pools with different filter settings and/or a different price per task are sent out for completion     when the pool opens.</li></ul></p>
`filter`|**Optional\[[FilterCondition](toloka.client.filter.FilterCondition.md)\]**|<p>Settings for user selection filters.</p>
`quality_control`|**Optional\[[QualityControl](toloka.client.quality_control.QualityControl.md)\]**|<p>Settings for quality control rules and the ID of the pool with training tasks.</p>
`dynamic_overlap_config`|**Optional\[[DynamicOverlapConfig](toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig.md)\]**|<p>Dynamic overlap setting. Allows you to change the overlap depending on how well the performers handle the task.</p>
`mixer_config`|**Optional\[[MixerConfig](toloka.client.pool.mixer_config.MixerConfig.md)\]**|<p>Parameters for automatically creating a task suite (“smart mixing”).</p>
`training_config`|**Optional\[[TrainingConfig](toloka.client.pool.Pool.TrainingConfig.md)\]**|<p>Optional[TrainingConfig]</p>
`metadata`|**Optional\[Dict\[str, List\[str\]\]\]**|<p>Optional[Dict[str, List[str]]]</p>
`owner`|**Optional\[[Owner](toloka.client.owner.Owner.md)\]**|<p>Optional[Owner]</p>
`id`|**Optional\[str\]**|<p>Pool ID. Read only field.</p>
`status`|**Optional\[[Status](toloka.client.pool.Pool.Status.md)\]**|<p>Status of the pool. Read only field.</p>
`last_close_reason`|**Optional\[[CloseReason](toloka.client.pool.Pool.CloseReason.md)\]**|<p>The reason for closing the pool the last time. Read only field.</p>
`created`|**Optional\[datetime\]**|<p>When this pool was created. Read only field.</p>
`last_started`|**Optional\[datetime\]**|<p>The date and time when the pool was last started. Read only field.</p>
`last_stopped`|**Optional\[datetime\]**|<p>The date and time when the pool was last stopped. Read only field.</p>
`type`|**Optional\[[Type](toloka.client.pool.Pool.Type.md)\]**|<p>Types of pool. Read only field.</p>

**Examples:**

How to create a new pool in a project.

```python
toloka_client = toloka.TolokaClient(your_token, 'PRODUCTION')
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
new_pool.set_mixer_config(real_tasks_count=10)
new_pool.quality_control.add_action(...)
new_pool = toloka_client.create_pool(new_pool)
print(new_pool.id)
```
## Methods summary

| Method | Description |
| :------| :-----------|
[is_archived](toloka.client.pool.Pool.is_archived.md)| None
[is_closed](toloka.client.pool.Pool.is_closed.md)| None
[is_locked](toloka.client.pool.Pool.is_locked.md)| None
[is_open](toloka.client.pool.Pool.is_open.md)| None
[set_assignments_issuing_config](toloka.client.pool.codegen_setter_for_assignments_issuing_config.md)| A shortcut setter for assignments_issuing_config
[set_captcha_frequency](toloka.client.pool.codegen_setter_for_quality_control_captcha_frequency.md)| A shortcut setter for quality_control.captcha_frequency
[set_checkpoints_config](toloka.client.pool.codegen_setter_for_quality_control_checkpoints_config.md)| A shortcut setter for quality_control.checkpoints_config
[set_defaults](toloka.client.pool.codegen_setter_for_defaults.md)| A shortcut setter for defaults
[set_dynamic_overlap_config](toloka.client.pool.codegen_setter_for_dynamic_overlap_config.md)| A shortcut setter for dynamic_overlap_config
[set_dynamic_pricing_config](toloka.client.pool.codegen_setter_for_dynamic_pricing_config.md)| A shortcut setter for dynamic_pricing_config
[set_filter](toloka.client.pool.codegen_setter_for_filter.md)| A shortcut setter for filter
[set_mixer_config](toloka.client.pool.codegen_setter_for_mixer_config.md)| A shortcut setter for mixer_config
[set_owner](toloka.client.pool.codegen_setter_for_owner.md)| A shortcut setter for owner
[set_quality_control](toloka.client.pool.codegen_setter_for_quality_control.md)| A shortcut setter for quality_control
[set_quality_control_configs](toloka.client.pool.codegen_setter_for_quality_control_configs.md)| A shortcut method for setting 
[set_training_config](toloka.client.pool.codegen_setter_for_training_config.md)| A shortcut setter for training_config
[set_training_requirement](toloka.client.pool.codegen_setter_for_quality_control_training_requirement.md)| A shortcut setter for quality_control.training_requirement
