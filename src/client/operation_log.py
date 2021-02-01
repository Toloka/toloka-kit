from typing import Any, Dict

from .primitives.base import BaseTolokaObject


class OperationLogItem(BaseTolokaObject):
    type: str
    success: bool

    input: Dict[str, Any]
    output: Dict[str, Any]
