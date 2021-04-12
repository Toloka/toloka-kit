__all__ = ['OperationLogItem']
from typing import Any, Dict

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

    type: str
    success: bool

    input: Dict[str, Any]
    output: Dict[str, Any]
