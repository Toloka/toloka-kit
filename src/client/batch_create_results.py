__all__ = [
    'FieldValidationError',
    'TaskBatchCreateResult',
    'TaskSuiteBatchCreateResult',
    'UserBonusBatchCreateResult',
    'WebhookSubscriptionBatchCreateResult'
]
from typing import Any, Dict, List, Optional, Type

from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass
from .task import Task
from .task_suite import TaskSuite
from .user_bonus import UserBonus
from .webhook_subscription import WebhookSubscription


class FieldValidationError(BaseTolokaObject):
    """Error that contains information about an invalid field.

    Attributes:
        code: An error code.
        message: An error message.
        params: Additional parameters describing the error.
    """

    code: str
    message: str
    params: List[Any]


def _create_batch_create_result_class_for(type_: Type, docstring: Optional[str] = None):
    cls = BaseTolokaObjectMetaclass(
        f'{type_.__name__}BatchCreateResult',
        (BaseTolokaObject,),
        {
            'validation_errors': None,
            '__annotations__': {
                'items': Dict[str, type_],
                'validation_errors': Optional[Dict[str, Dict[str, FieldValidationError]]],
            }
        },
    )
    cls.__module__ = __name__
    cls.__doc__ = docstring
    return cls


TaskBatchCreateResult = _create_batch_create_result_class_for(
    Task,
    """The results of the tasks creation operation.

    Attributes:
        items: A list of created tasks.
        validation_errors: A list with validation errors in input tasks. The list is filled if the request parameter `skip_invalid_items` is `True`.
    """
)
TaskSuiteBatchCreateResult = _create_batch_create_result_class_for(
    TaskSuite,
    """The results of the task suites creation operation.

    Attributes:
        items: A list of created task suites.
        validation_errors: A list with validation errors in input task suites. The list is filled if the request parameter `skip_invalid_items` is `True`.
    """
)
UserBonusBatchCreateResult = _create_batch_create_result_class_for(
    UserBonus,
    """The results of the creating rewards for Tolokers.

    Attributes:
        items: A list of created rewards.
        validation_errors: A list with validation errors. The list is filled if the request parameter `skip_invalid_items` is `True`.
    """
)
WebhookSubscriptionBatchCreateResult = _create_batch_create_result_class_for(
    WebhookSubscription,
    """A list with the results of the webhook-subscriptions creation operation.

    Attributes:
        items: Object with created webhook-subscriptions.
        validation_errors: Object with validation errors.
    """
)
