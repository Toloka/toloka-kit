# accept_assignment
`toloka.client.TolokaClient.accept_assignment` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/__init__.py#L44)

```python
accept_assignment(
    self,
    assignment_id: str,
    public_comment: str
)
```

Marks one assignment as accepted


Used then your pool created with auto_accept_solutions=False parametr.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`assignment_id`|**str**|<p>What assignment will be accepted.</p>
`public_comment`|**str**|<p>Message to the performer.</p>

* **Returns:**

  Object with new status.

* **Return type:**

  [Assignment](toloka.client.assignment.Assignment.md)

**Examples:**

How to accept one assignment.

```python
toloka_client.accept_assignment(assignment_id, 'Well done!')
```
