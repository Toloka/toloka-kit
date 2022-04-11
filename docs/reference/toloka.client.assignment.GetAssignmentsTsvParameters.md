# GetAssignmentsTsvParameters
`toloka.client.assignment.GetAssignmentsTsvParameters` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/assignment.py#L110)

```python
GetAssignmentsTsvParameters(
    self,
    *,
    status: Optional[List[Status]] = ...,
    start_time_from: Optional[datetime] = None,
    start_time_to: Optional[datetime] = None,
    exclude_banned: Optional[bool] = None,
    field: Optional[List[Field]] = ...
)
```

Allows you to downloads assignments as pandas.DataFrame


Used in "TolokaClient.get_assignments_df" method.
Implements the same behavior as if you download results in web-interface and then read it by pandas.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status`|**Optional\[List\[[Status](toloka.client.assignment.GetAssignmentsTsvParameters.Status.md)\]\]**|<p>Assignments in which statuses will be downloaded.</p>
`start_time_from`|**Optional\[datetime\]**|<p>Upload assignments submitted after the specified date and time.</p>
`start_time_to`|**Optional\[datetime\]**|<p>Upload assignments submitted before the specified date and time.</p>
`exclude_banned`|**Optional\[bool\]**|<p>Exclude answers from banned performers, even if assignments in suitable status &quot;ACCEPTED&quot;.</p>
`field`|**Optional\[List\[[Field](toloka.client.assignment.GetAssignmentsTsvParameters.Field.md)\]\]**|<p>The names of the fields to be unloaded. Only the field names from the Assignment class, all other fields are added by default.</p>
