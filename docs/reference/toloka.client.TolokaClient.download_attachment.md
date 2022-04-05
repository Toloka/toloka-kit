# download_attachment
`toloka.client.TolokaClient.download_attachment` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/__init__.py#L44)

```python
download_attachment(
    self,
    attachment_id: str,
    out: BinaryIO
)
```

Downloads specific attachment

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`attachment_id`|**str**|<p>ID of attachment.</p>
`out`|**BinaryIO**|<p>File object where to put downloaded file.</p>

**Examples:**

How to download an attachment.

```python
with open('my_new_file.txt', 'wb') as out_f:
    toloka_client.download_attachment(attachment_id='1', out=out_f)
```
