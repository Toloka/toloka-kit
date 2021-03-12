from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject
from .primitives.parameter import Parameters


class UserBonus(BaseTolokaObject):
    """Issuing a bonus to a specific performer

    It's addition to payment for completed tasks.

    Attributes:
        user_id: Performer ID to whom the bonus will be issued.
        amount: The bonus amount in dollars. Can be from 0.01 to 100 dollars per user per time.
        private_comment: Comments that are only visible to the requester.
        public_title: Message header for the user. You can provide a title in several languages
            (the message will come in the user's language).
        public_message: Message text for the user. You can provide text in several languages
            (the message will come in the user's language).
        without_message: Do not send a bonus message to the user. To award a bonus without a message, specify null
            for public_title and public_message and True for without_message.
        assignment_id: The answer to the task for which this bonus was issued.
        id: Internal ID of the issued bonus. Read only.
        created: Date the bonus was awarded, in UTC. Read only.

    Example:
        How to create bonus with message for specific assignment.

        >>> new_bonus = toloka_client.create_user_bonus(
        >>>     UserBonus(
        >>>         user_id='1',
        >>>         amount='0.50',
        >>>         public_title='Perfect job!',
        >>>         public_message='You are the best performer EVER!'
        >>>         assignment_id='012345'
        >>>     )
        >>> )
        ...

        Hoiw to create bonus with message in several languages.

        >>> new_bonus = toloka_client.create_user_bonus(
        >>>     UserBonus(
        >>>         user_id='1',
        >>>         amount='0.10',
        >>>         public_title= {
        >>>             'EN': 'Good Job!',
        >>>             'RU': 'Молодец!',
        >>>         },
        >>>         public_message: {
        >>>             'EN': 'Ten tasks completed',
        >>>             'RU': 'Выполнено 10 заданий',
        >>>         },
        >>>     )
        >>> )
        ...
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
    """Parameters for creating performer bonuses

    Used in methods 'create_user_bonus', 'create_user_bonuses' и 'create_user_bonuses_async' of the class TolokaClient,
    to clarify the behavior when creating bonuses.

    Attributes:
        operation_id: Operation ID. If asynchronous creation is used, by this identifier you can later get
            results of creating bonuses.
        skip_invalid_items: Validation parameters of objects:
            * True - Award a bonus if the object with bonus information passed validation. Otherwise, skip the bonus.
            * False - Default behaviour. Stop the operation and don't award bonuses if at least one object didn't pass validation.
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
