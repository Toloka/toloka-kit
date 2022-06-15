# TaskSuite
`toloka.client.task_suite.TaskSuite` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/task_suite.py#L19)

```python
TaskSuite(
    self,
    *,
    infinite_overlap=None,
    overlap=None,
    pool_id: Optional[str] = None,
    tasks: Optional[List[BaseTask]] = ...,
    reserved_for: Optional[List[str]] = None,
    unavailable_for: Optional[List[str]] = None,
    issuing_order_override: Optional[float] = None,
    mixed: Optional[bool] = None,
    traits_all_of: Optional[List[str]] = None,
    traits_any_of: Optional[List[str]] = None,
    traits_none_of_any: Optional[List[str]] = None,
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
    id: Optional[str] = None,
    remaining_overlap: Optional[int] = None,
    automerged: Optional[bool] = None,
    created: Optional[datetime] = None
)
```

A set of tasks issued to the performer at a time


TaskSuite can contain one or more tasks. The execution price is charged for one TaskSuite.
Performers receive exactly one TaskSuite when they take on your task.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**Optional\[str\]**|<p>The ID of the pool that task suite are uploaded to.</p>
`tasks`|**Optional\[List\[[BaseTask](toloka.client.task.BaseTask.md)\]\]**|<p>Data for the tasks.</p>
`reserved_for`|**Optional\[List\[str\]\]**|<p>IDs of users who will have access to the task suite.</p>
`unavailable_for`|**Optional\[List\[str\]\]**|<p>IDs of users who shouldn&#x27;t have access to the task suite.</p>
`issuing_order_override`|**Optional\[float\]**|<p>The priority of a task suite among other sets in the pool. Defines the order in which task suites are assigned to performers. The larger the parameter value, the higher the priority. This parameter can be used if the pool has issue_task_suites_in_creation_order: true. Allowed values: from -99999.99999 to 99999.99999.</p>
`mixed`|**Optional\[bool\]**|<p>Type of operation for creating a task suite:<ul><li>True - Automatically with the &quot;smart mixing&quot; option (for details, see Yandex.Toloka requester&#x27;s guide).</li><li>False - Manually.</li></ul></p>
`traits_all_of`|**Optional\[List\[str\]\]**|<p></p>
`traits_any_of`|**Optional\[List\[str\]\]**|<p></p>
`traits_none_of_any`|**Optional\[List\[str\]\]**|<p></p>
`longitude`|**Optional\[float\]**|<p>The longitude of the point on the map for the task suite.</p>
`latitude`|**Optional\[float\]**|<p>The latitude of the point on the map for the task suite.</p>
`id`|**Optional\[str\]**|<p>ID of a task suite. Read only field.</p>
`remaining_overlap`|**Optional\[int\]**|<p>How many times will this Task Suite be issued to performers. Read only field.</p>
`automerged`|**Optional\[bool\]**|<p>The task suite flag is created after task merging. Read Only field. Value:<ul><li>True - The task suite is generated as a result of merging identical tasks.</li><li>False - A standard task suite created by &quot;smart mixing&quot; or by the requester.</li></ul></p>
`created`|**Optional\[datetime\]**|<p>The UTC date and time when the task suite was created. Read Only field.</p>
## Methods Summary

| Method | Description |
| :------| :-----------|
[add_base_task](toloka.client.task_suite.TaskSuite.add_base_task.md)| None
