# wait_operation
`toloka.client.TolokaClient.wait_operation`

```python
wait_operation(
    self,
    op: Operation,
    timeout: timedelta = ...
)
```

Waits for the operation to complete, and return it

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`op`|**[Operation](toloka.client.operations.Operation.md)**|<p>ID of the operation.</p>
`timeout`|**timedelta**|<p>How long to wait. Defaults to 10 minutes.</p>

* **Returns:**

  Completed operation.

* **Return type:**

  [Operation](toloka.client.operations.Operation.md)

**Examples:**

Waiting for the pool to close can be running in the background.

```python
pool = toloka_client.get_pool(pool_id)
while not pool.is_closed():
    op = toloka_client.get_analytics([toloka.analytics_request.CompletionPercentagePoolAnalytics(subject_id=pool.id)])
    op = toloka_client.wait_operation(op)
    percentage = op.details['value'][0]['result']['value']
    print(
        f'   {datetime.datetime.now().strftime("%H:%M:%S")}     '
        f'Pool {pool.id} - {percentage}%'
        )
    time.sleep(60 * minutes_to_wait)
    pool = toloka_client.get_pool(pool.id)
print('Pool was closed.')
```
