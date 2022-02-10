# register
`toloka.streaming.pipeline.Pipeline.register`

```python
register(self, observer: BaseObserver)
```

Register given observer.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`observer`|**[BaseObserver](toloka.streaming.observer.BaseObserver.md)**|<p>Observer object.</p>

* **Returns:**

  The same observer object. It's usable to write one-liners.

* **Return type:**

  [BaseObserver](toloka.streaming.observer.BaseObserver.md)

**Examples:**

Register observer.

```python
observer = SomeObserver(pool_id='123')
observer.do_some_preparations(...)
toloka_loop.register(observer)
```

One-line version.

```python
toloka_loop.register(SomeObserver(pool_id='123')).do_some_preparations(...)
```
