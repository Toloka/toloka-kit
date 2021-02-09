from typing import Any, Dict, Optional

from .base import BaseComponent


class BaseData(BaseComponent):
    """Components used for working with data: input, output, or intermediate.

    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        path: Optional[Any] = ...,
        default: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    path: Optional[Any]
    default: Optional[Any]

class InputData(BaseData):
    """The input data.

    For example, links to images that will be shown to users. In the Template Builder sandbox, you can
    set an example of input data.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        path: Optional[Any] = ...,
        default: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    path: Optional[Any]
    default: Optional[Any]

class InternalData(BaseData):
    """The data available only from within the task.

    This data is not saved to the results. Use this data to calculate or store intermediate values.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        path: Optional[Any] = ...,
        default: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    path: Optional[Any]
    default: Optional[Any]

class LocalData(BaseData):
    """The local data available only from inside the component.

    This data is used in some auxiliary components, such as helper.transform.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        path: Optional[Any] = ...,
        default: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    path: Optional[Any]
    default: Optional[Any]

class OutputData(BaseData):
    """The output data.

    This is what you get when you click the Send button.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        path: Optional[Any] = ...,
        default: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    path: Optional[Any]
    default: Optional[Any]

class RelativeData(BaseData):
    """A special component for saving data.

    It's only available in the field.list component.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        path: Optional[Any] = ...,
        default: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    path: Optional[Any]
    default: Optional[Any]
