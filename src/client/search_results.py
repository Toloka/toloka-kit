from typing import Type, List

from .aggregation import AggregatedSolution
from .assignment import Assignment
from .attachment import Attachment
from .message_thread import MessageThread
from .pool import Pool
from .primitives.base import BaseTolokaObject, BaseTolokaObjectMetaclass
from .project import Project
from .training import Training
from .skill import Skill
from .task import Task
from .task_suite import TaskSuite
from .user_bonus import UserBonus
from .user_restriction import UserRestriction
from .user_skill import UserSkill


def _create_search_result_class_for(type_: Type):
    cls = BaseTolokaObjectMetaclass(
        f'{type_.__name__}SearchResult',
        (BaseTolokaObject,),
        {'__annotations__': {'items': List[type_], 'has_more': bool}},
    )
    cls.__module__ = __name__
    return cls


AggregatedSolutionSearchResult = _create_search_result_class_for(AggregatedSolution)
AssignmentSearchResult = _create_search_result_class_for(Assignment)
AttachmentSearchResult = _create_search_result_class_for(Attachment)
MessageThreadSearchResult = _create_search_result_class_for(MessageThread)
ProjectSearchResult = _create_search_result_class_for(Project)
PoolSearchResult = _create_search_result_class_for(Pool)
SkillSearchResult = _create_search_result_class_for(Skill)
TaskSearchResult = _create_search_result_class_for(Task)
TaskSuiteSearchResult = _create_search_result_class_for(TaskSuite)
TrainingSearchResult = _create_search_result_class_for(Training)
UserBonusSearchResult = _create_search_result_class_for(UserBonus)
UserRestrictionSearchResult = _create_search_result_class_for(UserRestriction)
UserSkillSearchResult = _create_search_result_class_for(UserSkill)
