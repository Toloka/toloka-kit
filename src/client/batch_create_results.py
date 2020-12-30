from typing import Any, Dict, List, Optional, Type

from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass
from .task import Task
from .task_suite import TaskSuite
from .user_bonus import UserBonus


class FieldValidationError(BaseTolokaObject):
    code: str
    message: str
    params: List[Any]


def _create_batch_create_result_class_for(type_: Type):
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
    return cls


TaskBatchCreateResult = _create_batch_create_result_class_for(Task)
TaskSuiteBatchCreateResult = _create_batch_create_result_class_for(TaskSuite)
UserBonusBatchCreateResult = _create_batch_create_result_class_for(UserBonus)
