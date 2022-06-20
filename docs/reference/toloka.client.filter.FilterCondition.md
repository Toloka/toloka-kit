# FilterCondition
`toloka.client.filter.FilterCondition` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/filter.py#L50)

```python
FilterCondition(self)
```

You can select users to access pool tasks.


For example, you can select users by region, skill, or browser type (desktop or mobile).


**Examples:**

How to setup filter for selecting users.

```python
filter = (
   (toloka.filter.Languages.in_('EN')) &
   (toloka.client.filter.DeviceCategory.in_(toloka.client.filter.DeviceCategory.SMARTPHONE))
)
```
