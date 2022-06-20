# AssignmentsIssuingConfig
`toloka.client.pool.Pool.AssignmentsIssuingConfig` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/pool/__init__.py#L120)

```python
AssignmentsIssuingConfig(self, issue_task_suites_in_creation_order: Optional[bool] = None)
```

Settings for assigning tasks in the pool.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`issue_task_suites_in_creation_order`|**Optional\[bool\]**|<p>For pools that don&#x27;t use “smart mixing”. Assign task suites in the order in which they were uploaded. For example, for a pool with an overlap of 5, the first task suite is assigned to five users, then the second task suite, and so on. This parameter is available when the project has &quot;assignments_issuing_type&quot;: &quot;AUTOMATED&quot;.</p>
