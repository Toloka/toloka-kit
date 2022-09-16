__all__ = [
    'UserBonus',
    'UserBonusCreateRequestParameters'
]
from attr.validators import optional, instance_of
import datetime
from decimal import Decimal
from typing import Dict

from .primitives.base import BaseTolokaObject
from .primitives.parameter import Parameters
from ..util._codegen import attribute


class UserBonus(BaseTolokaObject):
    """Issuing a bonus to a specific Toloker.

    It's addition to payment for completed tasks.

    Attributes:
        user_id: Toloker's ID to whom the bonus will be issued.
        amount: The bonus amount in dollars. Can be from 0.01 to 100 dollars per Toloker per time.
        private_comment: Comments that are only visible to the requester.
        public_title: Message header for the Toloker. You can provide a title in several languages
            (the message will come in the Toloker's language). Format {'language': 'title', ... }.
            The language can be RU/EN/TR/ID/FR.
        public_message: Message text for the Toloker. You can provide text in several languages
            (the message will come in the Toloker's language). Format {'language': 'message', ... }.
            The language can be RU/EN/TR/ID/FR.
        without_message: Do not send a bonus message to the Toloker. To award a bonus without a message, specify null
            for public_title and public_message and True for without_message.
        assignment_id: ID of the Toloker's response to the task a reward is issued for.
        id: Internal ID of the issued bonus. Read only.
        created: Date the bonus was awarded, in UTC. Read only.

    Example:
        How to create bonus with message for specific assignment.

        >>> new_bonus = toloka_client.create_user_bonus(
        >>>     UserBonus(
        >>>         user_id='1',
        >>>         amount='0.50',
        >>>         public_title={
        >>>             'EN': 'Perfect job!',
        >>>         },
        >>>         public_message={
        >>>             'EN': 'You are the best Toloker',
        >>>         },
        >>>         assignment_id='012345'
        >>>     )
        >>> )
        ...

        How to create bonus with message in several languages.

        >>> new_bonus = toloka_client.create_user_bonus(
        >>>     UserBonus(
        >>>         user_id='1',
        >>>         amount='0.10',
        >>>         public_title={
        >>>             'EN': 'Good Job!',
        >>>             'RU': 'Молодец!',
        >>>         },
        >>>         public_message={
        >>>             'EN': 'Ten tasks completed',
        >>>             'RU': 'Выполнено 10 заданий',
        >>>         }
        >>>     )
        >>> )
        ...
    """

    user_id: str
    amount: Decimal = attribute(validator=optional(instance_of(Decimal)))

    private_comment: str
    public_title: Dict[str, str]
    public_message: Dict[str, str]
    without_message: bool
    assignment_id: str

    # Readonly
    id: str = attribute(readonly=True)
    created: datetime.datetime = attribute(readonly=True)


class UserBonusCreateRequestParameters(Parameters):
    """Parameters for creating bonuses for Tolokers.

    Used in methods 'create_user_bonus', 'create_user_bonuses' и 'create_user_bonuses_async' of the class TolokaClient,
    to clarify the behavior when creating bonuses.

    Attributes:
        operation_id: Operation ID. If asynchronous creation is used, by this identifier you can later get
            results of creating bonuses.
        skip_invalid_items: Validation parameters of objects:
            * True - Award a bonus if the object with bonus information passed validation. Otherwise, skip the bonus.
            * False - Default behavior. Stop the operation and don't award bonuses if at least one object didn't pass validation.
    """

    operation_id: str
    skip_invalid_items: bool
