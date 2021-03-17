from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class OperationLogItem(BaseTolokaObject):
    """Objects of which the operation log consists

    Contains information about the validation errors and what sets of objects were created.

    Attributes:
        type: Type of action in the operation step.
        success: Result of the step (true or false).
        input: Input data at the operation step.
        output: Operation step output. Depends on the type.
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
        type: Optional[str] = ...,
        success: Optional[bool] = ...,
        input: Optional[Dict[str, Any]] = ...,
        output: Optional[Dict[str, Any]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    type: Optional[str]
    success: Optional[bool]
    input: Optional[Dict[str, Any]]
    output: Optional[Dict[str, Any]]
