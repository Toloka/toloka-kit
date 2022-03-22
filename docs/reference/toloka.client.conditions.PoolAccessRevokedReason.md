# PoolAccessRevokedReason
`toloka.client.conditions.PoolAccessRevokedReason` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/conditions.py#L220)

```python
PoolAccessRevokedReason(
    self,
    operator: IdentityOperator,
    value: Union[Type, str, None] = None
)
```

Reason for loss of access of the performer to the current pool

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`value`|**Optional\[[Type](toloka.client.conditions.PoolAccessRevokedReason.Type.md)\]**|<p>exact reason<ul><li>SKILL_CHANGE - The performer no longer meets one or more filters.</li><li>RESTRICTION - The performer&#x27;s access to tasks is blocked by a quality control rule (such as control tasks,     majority vote, fast answers, skipped assignments, or captcha).</li></ul></p>
