from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject
from .primitives.parameter import Parameters


class UserBonus(BaseTolokaObject):
    """UserBonus

    You can award bonuses to one or more users (in addition to payment for completed tasks).
    The bonus amount can be from 0.01 to 100 dollars per user per time.
    Attributes:
        user_id: User ID.
        amount: The dollar amount of the bonus.
        private_comment: Comments that are only visible to the requester.
        public_title: Optional[Any]
        public_message: Optional[Any]
        without_message: Do not send a bonus message to the user. To award a bonus without a message, specify null
            for public_title and public_message and True for without_message.
        assignment_id: Optional[str]
        id: Bonus ID.
        created: Date the bonus was awarded, in UTC.
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
        user_id: Optional[str] = ...,
        amount: Optional[Decimal] = ...,
        private_comment: Optional[str] = ...,
        public_title: Optional[Any] = ...,
        public_message: Optional[Any] = ...,
        without_message: Optional[bool] = ...,
        assignment_id: Optional[str] = ...,
        id: Optional[str] = ...,
        created: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    user_id: Optional[str]
    amount: Optional[Decimal]
    private_comment: Optional[str]
    public_title: Optional[Any]
    public_message: Optional[Any]
    without_message: Optional[bool]
    assignment_id: Optional[str]
    id: Optional[str]
    created: Optional[datetime]

class UserBonusCreateRequestParameters(Parameters):
    """UserBonusCreateRequestParameters

    Attributes:
        operation_id: Operation ID. Can be used for any method of request processing.
        skip_invalid_items: Validation parameters of objects:
            * True — Award a bonus if the object with bonus information passed validation. Otherwise, skip the bonus.
            * False — Stop the operation and don't award bonuses if at least one object didn't pass validation.
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
        operation_id: Optional[str] = ...,
        skip_invalid_items: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operation_id: Optional[str]
    skip_invalid_items: Optional[bool]
