# clone_project
`toloka.client.TolokaClient.clone_project` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/__init__.py#L40)

```python
clone_project(
    self,
    project_id: str,
    reuse_controllers: bool = True
)
```

Synchronously clones the project, all pools and trainings


Emulates cloning behaviour via Toloka interface:
- the same skills will be used
- the same quality control collectors will be used (could be changed by reuse_controllers=False)
- the expiration date will not be changed in the new project
- etc.

Doesn't have transaction - can clone project, and then raise on cloning pool.
Doesn't copy tasks/golden tasks/training tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`project_id`|**str**|<p>ID of the project to be cloned.</p>
`reuse_controllers`|**bool**|<p>Use same quality controllers in cloned and created projects. Defaults to True. This means that all quality control rules will be applied to both projects. For example, if you have rule &quot;fast_submitted_count&quot;, fast responses counts across both projects.</p>

* **Returns:**

  All created objects project, pools and trainings.

* **Return type:**

  [CloneResults](toloka.client.clone_results.CloneResults.md)

**Examples:**

```python
project, pools, trainings = toloka_client.clone_project('123')
```
