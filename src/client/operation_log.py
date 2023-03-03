__all__ = ['OperationLogItem']
from typing import Any, Dict

from .primitives.base import BaseTolokaObject


# TODO: Add children through spec_field type and success.
#  Add simple way of getting different objects of interest for every child.
#  e.g. user_bonus_id for type=USER_BONUS_PERSIST, success=True (https://toloka.ai/docs/api/get-operation-log/)
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
