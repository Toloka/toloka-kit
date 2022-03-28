# CursorFetchContext
`toloka.streaming.cursor.BaseCursor.CursorFetchContext` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/streaming/cursor.py#L83)

```python
CursorFetchContext(self, cursor: BaseCursor)
```

Context manager to return from `BaseCursor.try_fetch_all method`.


Commit cursor state only if no error occured.

