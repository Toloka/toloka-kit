# reject_assignment
`toloka.client.TolokaClient.reject_assignment` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/__init__.py#L44)

```python
reject_assignment(
    self,
    assignment_id: str,
    public_comment: str
)
```

Marks one assignment as rejected


Used then your pool created with auto_accept_solutions=False parametr.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`assignment_id`|**str**|<p>What assignment will be rejected.</p>
`public_comment`|**str**|<p>Message to the performer.</p>

* **Returns:**

  Object with new status.

* **Return type:**

  [Assignment](toloka.client.assignment.Assignment.md)

**Examples:**

Reject an assignment that was completed too fast.

```python
toloka_client.reject_assignment(assignment_id='1', 'Assignment was completed too fast.')
```
