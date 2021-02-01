from attr.validators import optional, instance_of
import datetime
from decimal import Decimal
from typing import Any

from .primitives.base import attribute, BaseTolokaObject
from .primitives.parameter import Parameters


class UserBonus(BaseTolokaObject):
    user_id: str
    amount: Decimal = attribute(validator=optional(instance_of(Decimal)))

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
