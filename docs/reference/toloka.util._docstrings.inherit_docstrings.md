# inherit_docstrings
`toloka.util._docstrings.inherit_docstrings`

```
inherit_docstrings(cls: Type[TypeVar('T')])
```

Modifies docstring parameters list of class and nested members updating it with docstring parameters from parent


classes and parent classes members.

All args and attributes from all parent classes are added to applied class docstring. If any parameter present in
more than a one class it is updated by the most recent version (according to mro order). The same applies to all
nested members: nested member is considered to be a parent of other nested member if and only if corresponding outer
classes have the same relationship and nested members have the same name.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`cls`|**Type\[TypeVar('T')\]**|<p>target class.</p>
