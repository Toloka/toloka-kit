import datetime
from typing import Any

from .primitives.base import BaseTolokaObject
from .primitives.parameter import Parameters


class UserBonus(BaseTolokaObject):
    user_id: str
    amount: float

    private_comment: str
    public_title: Any
    public_message: Any
    without_message: bool
    assignment_id: str

    # Readonly
    id: str
    created: datetime.datetime


class UserBonusCreateRequestParameters(Parameters):
    operation_id: str
    skip_invalid_items: bool
