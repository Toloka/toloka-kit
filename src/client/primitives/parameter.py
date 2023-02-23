__all__ = [
    'Parameters',
    'IdempotentOperationParameters',
]
import uuid

from .base import BaseTolokaObject
from ...util._codegen import attribute


class Parameters(BaseTolokaObject, kw_only=False):

    def unstructure(self) -> dict:
        return super().unstructure() or {}


class IdempotentOperationParameters(Parameters):
    """Parameters for idempotent operations such as tasks, task_suites and user bonuses creation.

    Works only with async_mode = True

    Attributes:
        operation_id: The ID of the operation conforming to the [RFC4122 standard](https://tools.ietf.org/html/rfc4122).
        async_mode: Request processing mode:
            * `True` — Asynchronous operation is started internally and `create_tasks` waits for the completion of it. It is recommended to create no more than 10,000 tasks per request in this mode.
            * `False` — The request is processed synchronously. A maximum of 5000 tasks can be added in a single request in this mode.

            Default value: `True`.
    """
    operation_id: uuid.UUID = attribute(factory=uuid.uuid4)
    async_mode: bool = attribute(default=True)
