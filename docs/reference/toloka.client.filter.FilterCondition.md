# FilterCondition
`toloka.client.filter.FilterCondition`

```
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
