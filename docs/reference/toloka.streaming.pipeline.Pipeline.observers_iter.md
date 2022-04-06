# observers_iter
`toloka.streaming.pipeline.Pipeline.observers_iter`

```python
observers_iter(self)
```

Iterate over registered observers.


* **Returns:**

  An iterator over all registered observers except deleted ones.
May contain observers sheduled to deletion and not deleted yet.

* **Return type:**

  Iterator\[[BaseObserver](toloka.streaming.observer.BaseObserver.md)\]
