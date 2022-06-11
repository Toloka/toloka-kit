# S3Storage
`toloka.streaming.storage.S3Storage` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/streaming/storage.py#L141)

```python
S3Storage(
    self,
    bucket: Type,
    *,
    locker: Optional[BaseLocker] = None
)
```

Storage that save to AWS S3 using given boto3 client.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`bucket`|**Type**|<p>Boto3 bucket object.</p>
`locker`|**Optional\[[BaseLocker](toloka.streaming.locker.BaseLocker.md)\]**|<p>Optional locker object. By default, no locker is used.</p>

**Examples:**

Create new instance.

```python
!pip install boto3
import boto3
import os
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
resource = session.resource('s3', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-2'))
bucket = resource.Bucket('my-bucket')
storage = S3Storage(bucket)
```

Use with pipelines.

```python
storage = S3Storage(bucket=bucket, locker=ZooKeeperLocker(kazoo_client, '/lock-dir'))
pipeline = Pipeline(storage=storage)
...
await pipeline.run()  # Will load from storage at the start and save after each iteration.
```
## Methods Summary

| Method | Description |
| :------| :-----------|
[cleanup](toloka.streaming.storage.S3Storage.cleanup.md)| None
[load](toloka.streaming.storage.S3Storage.load.md)| None
[save](toloka.streaming.storage.S3Storage.save.md)| None
